# Finviz Auto-Scraper for Google Sheets

This tool scrapes financial snapshot data (P/E, Market Cap, EPS, etc.) from Finviz.com for a specific stock ticker and automatically uploads it to a Google Sheet of your choice.

## Features

- **Bypasses Protection**: Uses a smart browser automation (Playwright) to load Finviz just like a real user.
- **Auto-Cleaning**: Extracts only the relevant data table, removing ads and news.
- **Direct Upload**: Pushes data directly to a specified Google Sheet tab.
- **Configurable**: Easily change the stock symbol or destination sheet via a config file.

## Installation

1. **Install Python**: Make sure you have Python installed.
2. **Install Dependencies**:
   Open a terminal/command prompt in this folder and run:
   ```bash
   pip install pandas playwright gspread oauth2client lxml html5lib
   playwright install chromium
   ```

## Setup Guide

### 1. Google Cloud Credentials

To let the script write to your Google Sheet, you need a "Robot Key" (Service Account).
Follow the **[Google Sheets Setup Guide](GSHEETS_SETUP.md)** included in this folder to generate your `credentials.json` file.
**Place `credentials.json` in this folder.**

### 2. Configuration

Open the `config.json` file in a text editor (Notepad, VS Code, etc.) and update the settings:

```json
{
  "symbol": "XOM",
  "sheet_id": "YOUR_LONG_GOOGLE_SHEET_ID_HERE",
  "target_tab_name": "Finviz_Data",
  "credentials_file": "credentials.json"
}
```

- **symbol**: The stock ticker you want to scrape (e.g., "AAPL", "TSLA", "XOM").
- **sheet_id**: The long string of characters in your Google Sheet URL (between `/d/` and `/edit`).
- **target_tab_name**: The name of the tab/sheet where data will be written.

### 3. Share Your Sheet

Don't forget to **Share** your Google Sheet (Editor access) with the `client_email` address found inside your `credentials.json` file.

## Usage

Run the script:

```bash
python main.py
```

The script will:

1. Launch a browser window (don't close it, it will close automatically).
2. Go to Finviz for your chosen symbol.
3. Extract the data.
4. Update your Google Sheet.

## Troubleshooting

- **Browser Error**: If the browser doesn't open, run `playwright install chromium` again.
- **Sheet Error**: If you get a permission error, check that the separate `client_email` has been invited to edit your Sheet.
