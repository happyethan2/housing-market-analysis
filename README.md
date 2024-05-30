# housing-market-analysis
Tool showcasing various scripts used to search for, store and generate analytics on housing market data particularly in South Australia.

## Chromedriver Installation and Version Checking

### Installing Chromedriver

1. **Download Chromedriver:**
   - Visit the [chromedriver download page](https://developer.chrome.com/docs/chromedriver/downloads) and download the version that matches your installed Chrome browser.
   - Extract the downloaded file and place it in a directory within your repository, e.g., `C:\housing-market-analysis\drivers\chromedriver.exe`.

2. **Add Chromedriver to Path in Script:**
   - Ensure the `driver_path` in your script points to the location of `chromedriver.exe`.

### Checking Chrome Version

1. **Verify Chrome Version:**
   - Open Chrome.
   - Go to the menu (three dots in the upper right corner) > Help > About Google Chrome.
   - Note the version number and ensure it matches the downloaded Chromedriver version.

### Saving DataFrame to CSV

- Ensure the `data` directory exists at the same level as your script.
- Modify your script to save the DataFrame to a CSV, e.g., within the `data` directory.

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


## Handling Shapefiles

### Extracting `shapefiles.zip`

The repository includes a zipped archive of geographic shapefiles needed for the heatmap visualizations. To properly use these shapefiles, you need to extract them into the specific directory required by the scripts.

1. **Locate the Archive**:
   - Find the `shapefiles.zip` file at the root level of this repository.

2. **Extract the Archive**:
   - You need to extract the contents of this zip file into the `/src/shapefiles/` directory within this repository.

### Extraction Steps

Depending on your operating system, you can extract the archive using built-in tools or third-party applications:

#### Windows
- Right-click the `shapefiles.zip` file.
- Choose "Extract All...".
- In the dialog that opens, enter or browse to the path for `/src/shapefiles/` within your local copy of the repository.
- Click 'Extract'.

#### macOS
- Double-click the `shapefiles.zip` file.
- Files will automatically extract to the same location as the zip file.
- Move the extracted folder to `/src/shapeholes/` within your repository.

#### Linux
- You can use the command line:
  ```bash
  unzip shapefiles.zip -d /path/to/repository/src/shapefiles/