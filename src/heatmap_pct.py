import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import PowerNorm
from datetime import datetime

def plot_heatmap(filter_extreme_values=False):
    """
    This function plots a heatmap of the percentage change in housing prices for Adelaide suburbs.
    The data is read from a CSV file and merged with a GeoDataFrame containing the suburb shapes.
    The heatmap is color-coded based on the percentage change values, with a colorbar showing the range of values.
    Suburbs with extreme percentage change values can be filtered out using the filter_extreme_values parameter.
    
    Args:
        filter_extreme_values (bool, optional): _description_. Defaults to False.
    """
    # load csv into df
    data_filepath = 'realestatedata_24May2024.csv'
    df = pd.read_csv(data_filepath, parse_dates=['timestamp'])

    # get data with most recent date for each suburb
    df_latest = df.sort_values('timestamp').groupby('suburb', as_index=False).last()

    # clip bottom and top 10%
    if filter_extreme_values:
        lower_bound = df_latest['pct_change'].quantile(0.10)
        upper_bound = df_latest['pct_change'].quantile(0.90)
        df_latest = df_latest[(df_latest['pct_change'] >= lower_bound) & 
                              (df_latest['pct_change'] <= upper_bound)]

    # locate and read shapefile
    shapefile_path = 'shapefiles\Suburbs_GDA2020.shp'
    gdf = gpd.read_file(shapefile_path)
    gdf['suburb'] = gdf['suburb'].str.lower()
    df_latest['suburb'] = df_latest['suburb'].str.lower()

    # merge rows with geodataframe and remove NaN pctchg values
    gdf_merged = gdf.merge(df_latest, left_on='suburb', right_on='suburb', how='left')
    gdf_merged = gdf_merged.dropna(subset=['percentage_change'])

    # setup plot
    fig, ax = plt.subplots(1, figsize=(12, 12))
    fig.canvas.manager.set_window_title(f'adelaide_house_prices_{datetime.now().strftime("%d%b%Y")}')
    ax.set_title('Adelaide Median Housing Price % Change')

    plt.xlim(138.4, 139.0)
    plt.ylim(-35.3, -34.6)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Define the colormap and normalization
    cmap = plt.get_cmap('YlOrRd')
    norm = PowerNorm(gamma=0.8, vmin=gdf_merged['percentage_change'].min(), vmax=gdf_merged['percentage_change'].max())

    # Plot the heatmap using the colormap and normalization
    gdf_merged.plot(column='percentage_change', cmap=cmap, linewidth=0.8, edgecolor='0.8', ax=ax, legend=False, norm=norm)

    
    # Add colorbar with percentage values
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, format=FuncFormatter(lambda x, pos: f"{x:.2f}%"))

    # List of suburbs to label (same as your previous script)
    suburbs_to_label = ['unley', 'glenelg', 'woodville', 'elizabeth', 'noarlunga',
                        'salisbury', 'kilburn', 'adelaide', 'athelstone', 'plympton', 
                        'morphett vale', 'belair', 'henley beach', 'brighton', 'north haven', 
                        'bowden', 'angle vale', 'stirling', 'gepps cross', 'banksia park',
                        'klemzig', 'pooraka', 'magil', 'happy valley', 'hallet cove',
                        'semaphore', 'mawson lakes', 'seaford', 'aldinga', 'tennyson',
                        'oakbank', 'mount barker', 'woodside', 'flagstaff hill',
                        'glenelg', 'cheltenham', 'modbury']

    # Loop through the GeoDataFrame and add labels for the selected suburbs
    for index, row in gdf_merged.iterrows():
        if row['suburb'] in suburbs_to_label:
            x = row['geometry'].centroid.x
            y = row['geometry'].centroid.y
            plt.text(x, y, row['suburb'], fontsize=9)
            plt.scatter(x, y, color='black', s=2)  # Add dots next to labels

    plt.show()

# Call the function with filter_extreme_values parameter
plot_heatmap(filter_extreme_values=True)