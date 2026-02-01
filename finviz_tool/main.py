import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright
import time
import os
import sys
import json

# --- Configuration Loading ---
def load_config():
    config_path = 'config.json'
    if not os.path.exists(config_path):
        print("Error: config.json not found.")
        sys.exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

CONFIG = load_config()

SYMBOL = CONFIG.get('symbol', 'XOM')
URL = f'https://finviz.com/quote.ashx?t={SYMBOL}'
SHEET_ID = CONFIG.get('sheet_id')
CREDENTIALS_FILE = CONFIG.get('credentials_file', 'credentials.json')
TARGET_TAB_NAME = CONFIG.get('target_tab_name', 'Finviz_Data')

def get_finviz_data():
    """Scrapes the financial snapshot table from Finviz."""
    print(f"Launching browser for {URL}...")
    data_frames = []
    
    with sync_playwright() as p:
        # Headless=False is often required to bypass bot detection on financial sites
        # We start mostly maximized to look human
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={ 'width': 1280, 'height': 1024 }
        )
        page = context.new_page()

        try:
            print("Navigating to page...")
            # Wait only for DOM content (faster, ignores ads/analytics)
            page.goto(URL, timeout=60000, wait_until='domcontentloaded') 
            print("Page loaded (DOM). Waiting for table content...")
            
            # Wait for specific element to be sure
            try:
                page.wait_for_selector('table.snapshot-table2', timeout=10000)
            except:
                print("Specific selector not found, proceeding with raw content...")
            
            content = page.content()
            data_frames = pd.read_html(content)
            
        except Exception as e:
            print(f"Error scraping: {e}")
            return None
        finally:
            browser.close()

    print("Processing tables...")
    snapshot_df = None
    
    for df in data_frames:
        # Heuristic: looks for 'Market Cap' and 'P/E' which are standard Finviz keys
        flat_str = df.to_string()
        if 'Market Cap' in flat_str and 'P/E' in flat_str:
            snapshot_df = df
            break
            
    if snapshot_df is None:
        print("Could not find the snapshot table.")
        return None

    # Clean/Flatten the table
    raw_data = [] # List of (key, val)
    for index, row in snapshot_df.iterrows():
        for i in range(0, len(row), 2):
            if i+1 < len(row):
                key = str(row[i]).strip()
                val = str(row[i+1]).strip()
                if key and key.lower() != 'nan' and key.lower() != 'none':
                    raw_data.append((key, val))
    
    # Filter for the actual snapshot block
    start_found = False
    final_data = []
    
    for key, val in raw_data:
        if key == 'Index':
            start_found = True
        
        if start_found:
            final_data.append([key, val])
            
        if start_found and key == 'Change':
             break
             
    if not final_data:
        return raw_data
        
    return final_data

def upload_to_sheet(data, sheet_id):
    """Uploads list of [key, value] to Google Sheets."""
    print(f"Connecting to Google Sheet ({sheet_id})...")
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: {CREDENTIALS_FILE} not found. Please place it in this folder.")
        return

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(sheet_id)
        
        # Select or Create the Worksheet
        try:
            worksheet = sheet.worksheet(TARGET_TAB_NAME)
        except gspread.WorksheetNotFound:
            print(f"Creating new tab: {TARGET_TAB_NAME}")
            worksheet = sheet.add_worksheet(title=TARGET_TAB_NAME, rows=100, cols=10)

        # Clear existing content
        worksheet.clear()
        
        # Prepare data for upload (add headers)
        rows_to_write = [['Metric', 'Value']] + data
        
        # Write to sheet
        # Update using list of lists
        worksheet.update(range_name='A1', values=rows_to_write)
        print("SUCCESS: Data written to Google Sheet.")
        print(f"View it here: https://docs.google.com/spreadsheets/d/{sheet_id}")

    except Exception as e:
        print(f"Google Sheets Error: {e}")

def main():
    if not SHEET_ID or SHEET_ID == "YOUR_GOOGLE_SHEET_ID_HERE":
        print("Please configure your 'sheet_id' in config.json first.")
        return

    data = get_finviz_data()
    if data:
        print(f"Extracted {len(data)} data points for {SYMBOL}.")
        upload_to_sheet(data, SHEET_ID)
    else:
        print("Failed to get data.")

if __name__ == "__main__":
    main()
