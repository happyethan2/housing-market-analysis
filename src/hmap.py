# Importing API Keys
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Analysis libraries
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime

# Heatmap colouring
from matplotlib.colors import PowerNorm

# Database libraries
import boto3

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

table = dynamodb.Table('realestatedata')

# Scan the table
response = table.scan()
items = response['Items']

# Create a DataFrame from the items
df = pd.DataFrame(items)
df['price'] = df['price'].astype(float)
df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert the 'timestamp' column to datetime format

# Get the most recent date's data for each suburb
df_latest = df.sort_values('timestamp').groupby('suburb', as_index=False).last()

# Locate the suburb shape file and read it
shapefile_path = 'shapefiles\Suburbs_GDA2020.shp'
gdf = gpd.read_file(shapefile_path)
gdf['suburb'] = gdf['suburb'].str.lower()
df_latest['suburb'] = df_latest['suburb'].str.lower()

# Merge the data with the GeoDataFrame
gdf_merged = gdf.merge(df_latest, left_on='suburb', right_on='suburb')

# Set up plot
fig, ax = plt.subplots(1, figsize=(12, 12))
fig.canvas.manager.set_window_title(f'adelaide_house_prices_{datetime.now().strftime("%d%b%Y")}')
ax.set_title(f'Adelaide Median Housing Prices {datetime.now().strftime("%d %b %Y")}')

plt.xlim(138.4, 139.0)
plt.ylim(-35.3, -34.6)

plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Define the colormap
cmap = plt.get_cmap('coolwarm')

# define the normalization. The gamma parameter controls the emphasis.
# a value less than 1 will emphasize the higher values (more yellow).
norm = PowerNorm(gamma=0.8, vmin=gdf_merged['price'].min(), vmax=gdf_merged['price'].max())

# plot the heatmap using the colormap and normalization
gdf_merged.plot(column='price', cmap=cmap, linewidth=0.8, edgecolor='0.8', ax=ax, legend=False, norm=norm)

# add colorbar with dollar values
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []
cbar = fig.colorbar(sm, ax=ax, format=FuncFormatter(lambda x, pos: f"${x:,.0f}"))


# list of suburbs to label (same as your previous script)
suburbs_to_label = ['unley', 'glenelg', 'woodville', 'elizabeth', 'noarlunga',
                    'salisbury', 'kilburn', 'adelaide', 'athelstone', 'plympton', 
                    'morphett vale', 'belair', 'henley beach', 'brighton', 'north haven', 
                    'bowden', 'angle vale', 'stirling', 'gepps cross', 'banksia park',
                    'klemzig', 'pooraka', 'magil', 'happy valley', 'hallet cove',
                    'semaphore', 'mawson lakes', 'seaford', 'aldinga', 'tennyson',
                    'oakbank', 'mount barker', 'woodside', 'flagstaff hill',
                    'glenelg', 'cheltenham', 'modbury', 'hallett cove', 'crafers', 'blackwood', 
                    'seaview downs', 'salisbury', 'salisbury park',
                    'elizabeth', 'elizabeth park', 'elizabeth downs', 'edinburgh', 'largs bay',
                    'ferredyn park', 'findon', 'fulham', 'glenelg', 'grange', 'glanville', 'glenelg north',
                    'mile end', 'millswood', 'north adelaide', 'norwood',
                    'medindie', 'walkerville', 'prospect', 'burnside', 'glenside', 'glenunga',]

# Loop through the GeoDataFrame and add labels for the selected suburbs
for index, row in gdf_merged.iterrows():
    if row['suburb'] in suburbs_to_label:
        x = row['geometry'].centroid.x
        y = row['geometry'].centroid.y
        plt.text(x, y, row['suburb'], fontsize=9)
        plt.scatter(x, y, color='black', s=2)  # Add dots next to labels

plt.show()