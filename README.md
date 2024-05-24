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
- Modify your script to save the DataFrame to a CSV file within the `Data` directory.
