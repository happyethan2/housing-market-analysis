import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import PowerNorm
from datetime import datetime

def plot_heatmap(filter_extreme_values=False):
    """
    plot a heatmap of percentage change in housing prices for adelaide suburbs over specified date ranges
    data is read from a csv file and merged with a geodataframe containing the suburb shapes
    the heatmap is color-coded based on percentage change values, with a colorbar showing the range of values
    """
    # load csv
    data_filepath = 'data/realestatedata_30May2024.csv'
    df = pd.read_csv(data_filepath)

    lower_date, upper_date = df['lower_date'].iloc[0], df['upper_date'].iloc[0]
    
    # clip bottom and top 10% if needed
    if filter_extreme_values:
        lower_bound = df['pct_change'].quantile(0.10)
        upper_bound = df['pct_change'].quantile(0.90)
        df = df[(df['pct_change'] >= lower_bound) & (df['pct_change'] <= upper_bound)]

    # read shapefile
    shapefile_path = 'shapefiles/Suburbs_GDA2020.shp'
    gdf = gpd.read_file(shapefile_path)
    gdf['suburb'] = gdf['suburb'].str.lower()
    df['suburb'] = df['suburb'].str.lower()

    # merge with geodataframe and drop nan
    gdf_merged = gdf.merge(df, left_on='suburb', right_on='suburb', how='left')
    gdf_merged = gdf_merged.dropna(subset=['pct_change'])

    # setup plot
    fig, ax = plt.subplots(1, figsize=(12, 12))
    current_date = datetime.now().strftime("%d%b%Y")
    fig.canvas.manager.set_window_title(f'adelaide_house_prices_{lower_date}_{upper_date}')
    ax.set_title(f"Adelaide Housing Price % Change: {lower_date} to {upper_date}")

    plt.xlim(138.4, 139.0)
    plt.ylim(-35.3, -34.6)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # define colormap and normalization
    cmap = plt.get_cmap('YlOrRd')
    norm = PowerNorm(gamma=0.8, vmin=gdf_merged['pct_change'].min(), vmax=gdf_merged['pct_change'].max())

    # plot the heatmap
    gdf_merged.plot(column='pct_change', cmap=cmap, linewidth=0.8, edgecolor='0.8', ax=ax, legend=False, norm=norm)

    # add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, format=FuncFormatter(lambda x, pos: f"{x:.2f}%"))
    cbar.set_label('Percentage Change')
    
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

# call the function with filter_extreme_values parameter
plot_heatmap(filter_extreme_values=True)