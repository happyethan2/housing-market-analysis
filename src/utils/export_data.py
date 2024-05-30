import csv
import boto3
from datetime import datetime
import pytz
import pandas as pd
import numpy as np

# Importing API Keys
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def process_real_estate_data(monthly_change=True, lower_index=0, upper_index=None, max_range=False):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    table = dynamodb.Table('realestatedata')
    response = table.scan()
    sorted_items = sorted(response['Items'], key=lambda x: (x['suburb'].lower(), x['timestamp']))

    # Create a DataFrame from sorted items
    data = []
    for item in sorted_items:
        data.append({
            'suburb': item['suburb'],
            'price': float(item['price']),
            'timestamp': datetime.strptime(item['timestamp'], '%Y-%m-%d')
        })
    df = pd.DataFrame(data)
    df['year_month'] = df['timestamp'].dt.to_period('M')

    if monthly_change:
        df['pct_change'] = df.groupby('suburb')['price'].pct_change().fillna(np.nan) * 100
        output_columns = ['suburb', 'price', 'timestamp', 'pct_change']
    else:
        output_columns = ['suburb', 'lower_date', 'upper_date', 'pct_change']
        df = df.groupby('suburb').apply(lambda x: calculate_range_pct_change(x, lower_index, upper_index, max_range))
        df.reset_index(drop=True, inplace=True)

    # Format the current date
    adelaide_tz = pytz.timezone('Australia/Adelaide')
    formatted_date = datetime.now(adelaide_tz).strftime('%d%b%Y').upper()
    csv_file_path = f'data/realestatedata_{formatted_date}.csv'

    # Write to CSV
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(output_columns)
        for _, row in df.iterrows():
            writer.writerow(row[output_columns])
    print(f"Data successfully written to {csv_file_path}")

def calculate_range_pct_change(group, lower_index, upper_index, max_range):
    if max_range:
        lower_index = 0
        upper_index = -1
    if upper_index is None:
        upper_index = -1
    try:
        price_initial = group.iloc[lower_index]['price']
        price_final = group.iloc[upper_index]['price']
        pct_change = ((price_final - price_initial) / price_initial) * 100
        result = pd.Series({
            'suburb': group.name,
            'lower_date': group.iloc[lower_index]['timestamp'].strftime('%Y-%m-%d'),
            'upper_date': group.iloc[upper_index]['timestamp'].strftime('%Y-%m-%d'),
            'pct_change': pct_change
        })
    except IndexError:
        result = pd.Series({
            'suburb': group.name,
            'lower_date': None,
            'upper_date': None,
            'pct_change': None
        })
    return result

# process data
process_real_estate_data(monthly_change=False, lower_index=0, max_range=True)