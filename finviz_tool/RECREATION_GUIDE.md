# Project: Finviz Data Scraper & Google Sheets Sync

## Overview

This project automates the extraction of financial data (P/E, Market Cap, EPS, etc.) from Finviz.com and uploads it directly to a Google Sheet. It is built to be robust, bypassing anti-bot protections using browser automation.

## How to Recreate This Project

### 1. Prerequisites

- **Python Installed**: You need Python (3.7+) on your computer.
- **Google Account**: To access Google Sheets API.

### 2. Google Cloud Setup (The "Hard" Part)

To let a script write to a Google Sheet, you need a "Service Account" (a robot identity).

1.  **Go to Google Cloud Console**: [console.cloud.google.com](https://console.cloud.google.com/).
2.  **Create a New Project**: Name it "Finviz Scraper".
3.  **Enable APIs**:
    - Search for **"Google Sheets API"** -> Click **Enable**.
    - Search for **"Google Drive API"** -> Click **Enable**.
4.  **Create Credentials**:
    - Go to **APIs & Services > Credentials**.
    - Click **Create Credentials** -> **Service Account**.
    - Name it (e.g., `bot-editor`). Click **Create & Continue**. (Skip role assignment).
5.  **Get the Key**:
    - Click on the email address of the Service Account you just made.
    - Go to the **Keys** tab -> **Add Key** -> **Create new key** -> **JSON**.
    - This will download a file. **Rename it to `credentials.json`**.
    - **Move this file** into your project folder.

### 3. Google Sheet Setup

1.  **Create a blank Google Sheet**.
2.  **Open `credentials.json`** with a text editor and copy the `"client_email"` address (it looks like `bot-editor@project-name.iam.gserviceaccount.com`).
3.  **Share the Sheet**: Click the "Share" button in your Google Sheet and paste that email address as an **Editor**.
4.  **Get the Sheet ID**: Copy the long string from your URL (between `/d/` and `/edit`).
    - Example: `https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit`

### 4. Code Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/dleake14/jemini.git
    cd jemini/finviz_tool
    ```
2.  **Install Dependencies**:
    ```bash
    pip install pandas gspread oauth2client playwright lxml html5lib
    playwright install chromium
    ```

### 5. Configuration

Create a file named `config.json` in the `finviz_tool` folder with your details:

```json
{
  "symbol": "XOM",
  "sheet_id": "PASTE_YOUR_SHEET_ID_HERE",
  "target_tab_name": "Finviz_Data",
  "credentials_file": "credentials.json"
}
```

### 6. Run It

Run the main script to grab data for a single stock defined in your config:

```bash
python main.py
```

### Advanced: Batch Scraping

To scrape a custom list of stocks (like the Top 25 Healthcare), you can modify the script's loop or create a new script iterating over a list of tickers, calling the same `get_data_for_ticker` function.
