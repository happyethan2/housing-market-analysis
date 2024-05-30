import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def print_summary_statistics(filepath):
    """
    Prints aggregate statistics and top 10 suburbs by mean price with mean percentage change.
    Produces a histogram of house prices.
    """
    # Load CSV
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    
    # Group by suburb and calculate statistics
    summary = df.groupby('suburb').agg(
        min_price=('price', 'min'),
        max_price=('price', 'max'),
        mean_price=('price', 'mean'),
        median_price=('price', 'median'),
        mean_pct_change=('pct_change', 'mean')
    ).reset_index()

    # Print aggregate statistics
    print("Aggregate Statistics:")
    print(f"Min: {summary['min_price'].min():.2f}")
    print(f"Max: {summary['max_price'].max():.2f}")
    print(f"Mean: {summary['mean_price'].mean():.2f}")
    print(f"Median: {summary['median_price'].median():.2f}\n")

    # Top 10 suburbs by mean price
    top_10_suburbs = summary.sort_values(by='mean_price', ascending=False).head(10)
    print("Top 10 Suburbs by Mean Price:")
    top_10_suburbs[['suburb', 'mean_price', 'mean_pct_change']].to_string(index=False, header=True)

    # Format mean_pct_change with signs and percentage
    top_10_suburbs['mean_pct_change'] = top_10_suburbs['mean_pct_change'].apply(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
    print(top_10_suburbs[['suburb', 'mean_price', 'mean_pct_change']])

def plot_price_histogram(filepath):
    """
    Plots a histogram of house prices.
    """
    df = pd.read_csv(filepath)
    plt.figure(figsize=(10, 6), num='house_price_distribution')
    plt.hist(df['price'], bins=30, color='skyblue', edgecolor='black', weights=np.ones(len(df['price'])) / len(df['price']))
    plt.title('Distribution of House Prices')
    plt.xlabel('Price')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.show()

# Example usage
data_filepath = 'data/realestatedata_24May2024.csv'
print_summary_statistics(data_filepath)
plot_price_histogram(data_filepath)