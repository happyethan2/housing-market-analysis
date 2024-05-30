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

### `scrape_data.py` - Data Collection and Storage Script

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