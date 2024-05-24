import csv
import boto3
from datetime import datetime
import pytz
import os
import pandas as pd
import numpy as np

# Importing API Keys
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

table = dynamodb.Table('realestatedata')

response = table.scan()
sorted_items = sorted(response['Items'], key=lambda x: (x['suburb'].lower(), x['timestamp']))

# Create a DataFrame from the sorted items
data = []
for item in sorted_items:
    data.append({
        'suburb': item['suburb'],
        'price': float(item['price']),
        'timestamp': datetime.strptime(item['timestamp'], '%Y-%m-%d')
    })
df = pd.DataFrame(data)

# Extract month and year from timestamp
df['year_month'] = df['timestamp'].dt.to_period('M')

# Calculate the percentage change
df['pct_change'] = df.groupby('suburb')['price'].pct_change().fillna(np.nan) * 100

# Format the current date in the desired format
adelaide_tz = pytz.timezone('Australia/Adelaide')
formatted_date = datetime.now(adelaide_tz).strftime('%d%b%Y').upper()

csv_file_path = f'data/realestatedata_{formatted_date}.csv'

# Open the CSV file in write mode
with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(['suburb', 'price', 'timestamp', 'pct_change'])

    # Write the data rows
    for _, row in df.iterrows():
        writer.writerow([row['suburb'], row['price'], row['timestamp'].strftime('%Y-%m-%d'), f"{row['pct_change']:.4f}"])

print(f"Data successfully written to {csv_file_path}")