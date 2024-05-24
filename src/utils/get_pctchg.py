import pandas as pd
import matplotlib.pyplot as plt
import boto3
from datetime import datetime
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def calculate_pctchg():
    """
    This function calculates the percentage change in housing prices for the top 10 suburbs by mean price.
    It retrieves the data from the DynamoDB table 'realestatedata', calculates the percentage change between two dates,
    and plots the percentage change for the top 10 suburbs.
    
    It inputs aws data and outputs a csv file with the percentage change data.
    """
    
    # setup dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    table = dynamodb.Table('realestatedata')

    # Step 1: Retrieve Data and Create DataFrame
    response = table.scan()
    items = response['Items']

    # Create a DataFrame from the items
    df = pd.DataFrame(items)
    df['price'] = df['price'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Step 2: Calculate Percentage Change
    df_grouped = df.groupby(['suburb', 'timestamp'])['price'].mean().reset_index()

    # Create a pivot table with suburbs as index, timestamps as columns, and prices as values
    pivot_df = df_grouped.pivot_table(index='suburb', columns='timestamp', values='price').reset_index()

    # Find the suburbs that have data for both dates
    suburbs_with_data_for_both_dates = pivot_df.dropna()


    date1 = pd.to_datetime('2023-08-22')
    date2 = pd.to_datetime('2023-09-19')

    suburbs_with_data_for_both_dates['percentage_change'] = ((suburbs_with_data_for_both_dates[date2] - suburbs_with_data_for_both_dates[date1]) / suburbs_with_data_for_both_dates[date1]) * 100

    # Reset the multi-level index in suburbs_with_data_for_both_dates
    suburbs_with_data_for_both_dates.reset_index(inplace=True)

    # Merge to add the percentage_change column to df_grouped
    df_grouped = pd.merge(df_grouped, suburbs_with_data_for_both_dates[['suburb', 'percentage_change']], on='suburb', how='left')


    # Print the number of suburbs with data for both dates and the number of percentage change values calculated
    print(f"Number of suburbs with data for both dates: {len(suburbs_with_data_for_both_dates)}")
    print(f"Number of percentage change values calculated: {suburbs_with_data_for_both_dates['percentage_change'].notnull().sum()}")

    # Get top 10 suburbs by mean price
    top_suburbs = df_grouped.groupby('suburb')['price'].mean().nlargest(10).index.tolist()

    # Filter data for top 10 suburbs
    df_top_suburbs = df_grouped[df_grouped['suburb'].isin(top_suburbs)]

    print(df_top_suburbs)
    print(df_top_suburbs.columns)

    unique_dates_count = df_top_suburbs.groupby('suburb')['timestamp'].nunique().reset_index()
    print(unique_dates_count)

    print(df_top_suburbs.columns)

    # Plotting the percentage change for top 10 suburbs
    for suburb in top_suburbs:
        suburb_data = df_top_suburbs[df_top_suburbs['suburb'] == suburb]
        plt.plot(suburb_data['timestamp'], suburb_data['percentage_change'], label=suburb)

    plt.xlabel('Timestamp')
    plt.ylabel('Percentage Change')
    plt.title('Percentage Change for Top 10 Suburbs')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    # plt.show()

    # Step 2.1: Create a Pivot Table
    pivot_df = df.pivot_table(index='suburb', columns='timestamp', values='price', aggfunc='mean').reset_index()

    # Step 2.2: Check Identical Prices for Two Specific Dates (e.g., '2023-08-22' and '2023-09-19')
    date1 = pd.to_datetime('2023-08-22')
    date2 = pd.to_datetime('2023-09-19')

    # Step 2.3: Find Rows Where Prices Are Identical on the Two Dates
    identical_prices_mask = pivot_df[date1] == pivot_df[date2]

    # Step 2.4: Display Suburbs with Identical Prices on the Two Dates
    identical_prices_suburbs = pivot_df[identical_prices_mask]
    print(identical_prices_suburbs)

    # Step 2.5: Display the Number of Suburbs with Identical Prices
    num_identical_prices_suburbs = identical_prices_suburbs.shape[0]
    print(f"Number of suburbs with identical prices on {date1} and {date2}: {num_identical_prices_suburbs}")

    # Get the count of dates available for each suburb
    date_counts = df_grouped.groupby('suburb')['timestamp'].count().reset_index()

    # Get suburbs with data for both dates
    suburbs_with_data_for_both_dates = date_counts[date_counts['timestamp'] == 2]['suburb']

    # Get the percentage change values for the suburbs with data for both dates
    percentage_changes = df_grouped[df_grouped['suburb'].isin(suburbs_with_data_for_both_dates)]

    # save and timestamp data to csv
    curr_date = datetime.now().strftime('%d%b%Y')
    df_grouped.to_csv(f'pctchg_by_suburb_{curr_date}.csv', index=False)

    # Print the number of suburbs with data for both dates and the number of percentage change values calculated
    print(f"Number of suburbs with data for both dates: {len(suburbs_with_data_for_both_dates)}")
    print(f"Number of percentage change values calculated: {percentage_changes['percentage_change'].notna().sum()}")

    # Check the unique dates present in the dataset and the number of records for each date
    unique_dates = df['timestamp'].unique()
    records_per_date = df.groupby('timestamp').size()

    print(f"Unique dates in the dataset: {unique_dates}")
    print(f"Number of records per date: {records_per_date}")

    # Inspect a few records to verify the data
    print(df.head())

calculate_pctchg()