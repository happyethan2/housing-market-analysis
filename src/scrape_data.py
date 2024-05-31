# importing API keys
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# web scraping libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# analysis libraries
import pandas as pd
from datetime import datetime
import pytz

# database libraries
from decimal import Decimal
import boto3

base_url = "http://house.speakingsame.com/suburbtop.php?sta=sa&cat=HomePrice&name=&page="
suburb_names = []
prices = []

# setup selenium with a headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# configure chromedriver using path to executable
driver_path = 'drivers/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

# navigate through all the URLs
for i in range(15):
    url = base_url + str(i)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tbody_list = soup.find_all("tbody")
    rows = tbody_list[7].find_all("tr")

    for row in rows[1:]:
        suburb_name = row.find_all("td")[1].find("a").text
        suburb_names.append(suburb_name)
        price = row.find_all("td")[2].text
        prices.append(price)

driver.quit()

# create a DataFrame
data = {'suburb_name': suburb_names, 'price': prices}
df = pd.DataFrame(data)
df['price'] = df['price'].str.replace(',', '', regex=False).str.replace('$', '', regex=False).astype(float)

# dynamodb setup
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
table = dynamodb.Table('realestatedata')

# define the timezone
adelaide_tz = pytz.timezone('Australia/Adelaide')

# get the current date in UTC+9:30 (without time)
current_timestamp = datetime.now(adelaide_tz).strftime('%Y-%m-%d')

# scan the dynamodb table to get all timestamps
response = table.scan(
    ProjectionExpression="#ts",
    ExpressionAttributeNames={'#ts': 'timestamp'}
)

# extract all timestamps, convert to datetime objects, and sort them
all_timestamps = [datetime.strptime(item['timestamp'], '%Y-%m-%d') for item in response['Items']]
all_timestamps.sort()

# get the most recent timestamp
most_recent_timestamp = all_timestamps[-1] if all_timestamps else None

# calculate the number of days since the last upload
if most_recent_timestamp:
    most_recent_date = most_recent_timestamp.replace(tzinfo=adelaide_tz)
    current_date = datetime.now(adelaide_tz)
    days_since_last_upload = (current_date - most_recent_date).days

    # check if it's been at least 6 days since the last upload
    if days_since_last_upload >= 6:
        print("It's been at least 6 days since the last upload. Proceeding with the upload.")
    else:
        print(f"Only {days_since_last_upload} days since the last upload. Cannot upload data yet.")
        exit(0)  # exit the script if the condition is not met
else:
    print("No previous data found. Proceeding with the upload.")

# upload data to dynamodb
try:
    length = len(df)
    for index, row in df.iterrows():
        suburb = row['suburb_name']
        price = Decimal(str(row['price']))
        
        # create an item with suburb as the partition key and timestamp as the sort key
        item = {
            'suburb': suburb,
            'timestamp': current_timestamp,
            'price': price
        }
        
        # put the item into the dynamodb table
        table.put_item(Item=item)
        
        print(f"successfully uploaded item {index}/{length}")
except Exception as e:
    print(f"An error occurred while uploading data to DynamoDB: {str(e)}")
