# housing-market-analysis
Tool showcasing various scripts used to search for, store and generate analytics on housing market data particularly in South Australia.

## Chromedriver Installation and Version Checking

### Installing Chromedriver

1. **Download Chromedriver:**
   - Visit the [Chromedriver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads) and download the version that matches your installed Chrome browser.
   - Extract the downloaded file and place it in a directory within your repository, e.g., `D:\Git Repositories\real-estate-scraper\drivers\chromedriver.exe`.

2. **Add Chromedriver to Path in Script:**
   - Ensure the `driver_path` in your script points to the location of `chromedriver.exe`.

### Checking Chrome Version

1. **Verify Chrome Version:**
   - Open Chrome.
   - Go to the menu (three dots in the upper right corner) > Help > About Google Chrome.
   - Note the version number and ensure it matches the downloaded Chromedriver version.

### Saving DataFrame to CSV

- Ensure the `Data` directory exists at the same level as your script.
- Modify your script to save the DataFrame to a CSV, e.g., within the `Data` directory.

## Script Descriptions

### `src/scrape_data.py` - Data Collection and Storage Script

#### Overview
The `scrape_data.py` script is designed to automatically scrape, process, and upload housing market data for South Australia. It leverages both Selenium and BeautifulSoup for web scraping, manages data with pandas, and utilizes AWS DynamoDB for data storage.

#### Functionality
1. **Web Scraping**:
   - Uses Selenium with a headless Chrome browser to navigate through specified URLs.
   - Extracts suburb names and associated property prices from the HTML content using BeautifulSoup.

2. **Data Processing**:
   - Creates a pandas DataFrame to organize the suburb names and prices.
   - Cleans and converts price data from strings to floating-point numbers for numerical operations.

3. **Data Storage**:
   - Connects to AWS DynamoDB using credentials from a configuration file.
   - Checks the last data upload timestamp and ensures a minimum interval of six days between uploads.
   - Uploads new data entries to the DynamoDB table, ensuring data is up-to-date.

#### Usage
Ensure all dependencies are installed and AWS credentials are correctly configured before running the script. Use this script to maintain a regular and automated update of the housing market dataset.


### `src/utils/export_data.py` - Data Export and Transformation Script

#### Overview
This script is designed to fetch, transform, and export real estate data stored in AWS DynamoDB. It uses boto3 to interact with DynamoDB and pandas for data manipulation.

#### Functionality
1. **Data Retrieval**:
   - Retrieves all entries from the 'realestatedata' DynamoDB table.
   - Sorts the data by suburb and timestamp to prepare for further analysis.

2. **Data Transformation**:
   - Converts the retrieved data into a pandas DataFrame and calculates percentage changes either monthly or for a specified date range.
   - Offers flexibility to calculate changes over the entire available data range if required.

3. **Data Export**:
   - Formats the final dataset to either include detailed monthly changes or aggregated changes over a custom range.
   - Saves the processed data to a CSV file, ensuring it is readily available for analysis or reporting.

### `hmap_relative.py` - Heatmap Visualization Script

#### Overview
This script generates a heatmap visualization of the percentage change in housing prices for Adelaide suburbs over specified date ranges, using geopandas and matplotlib.

#### Functionality
1. **Data Loading and Processing**:
   - Reads processed data from a CSV file.
   - Optionally filters extreme values to focus on more typical changes.

2. **Geographic Data Integration**:
   - Integrates suburb boundary data from a shapefile to map the percentage changes geographically.

3. **Visualization**:
   - Plots a color-coded heatmap based on the percentage change of housing prices, with color intensity reflecting the magnitude of change.
   - Customizes plot aesthetics, including setting a dynamic window title based on the date range of the data being visualized.

4. **Interactive Features**:
   - Provides a color bar to interpret the percentage changes and labels selected suburbs directly on the map for better locality referencing.

#### Usage
Ensure all dependencies are installed, and data files are correctly formatted and located. The script is designed to be flexible, allowing for modifications in the selection of suburbs to label or the range of data to visualize.