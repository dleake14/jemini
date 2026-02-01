# Google Sheets Setup Guide

To let the script write directly to your Google Sheet, we need to set up a "Service Account" (a robot account) that has permission to edit your specific sheet.

## Step 1: Get the Credentials (JSON file)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **New Project** (name it something like "Finviz Scraper").
3. In the search bar at the top, search for "**Google Sheets API**" and click **Enable**.
4. Search for "**Google Drive API**" and click **Enable**.
5. Go to **APIs & Services > Credentials**.
6. Click **Create Credentials** > **Service Account**.
7. Give it a name (e.g., "bot-editor") and click **Create & Continue** (you can skip the role assignment steps).
8. Once created, click on the new Service Account (it looks like an email address).
9. Go to the **Keys** tab -> **Add Key** -> **Create new key** -> **JSON**.
10. This will download a file to your computer. **Rename it to `credentials.json`** and place it in this folder:
    `g:\My Drive\Personal\MISC\CODE\jemini\finviz_tool\`

## Step 2: Share your Google Sheet

1. Open your `credentials.json` file (you can open it with Notepad) and find the `"client_email"` field. It will look like `bot-editor@project-name.iam.gserviceaccount.com`.
2. Copy that email address.
3. Open the Google Sheet you want to write to.
4. Click **Share** (top right) and paste the email address.
5. Make sure it has **Editor** permissions.
6. Click **Send** (uncheck "Notify people" if you want).

## Step 3: Get the Sheet ID

1. Look at the URL of your Google Sheet. It looks like this:
   `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`
2. The long string of random characters between `/d/` and `/edit` is your **Sheet ID**.
   (In this example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`)
3. Provide this ID to me (or paste it into the script when I update it).

## Step 4: Install Python Library

I will need to install the library to talk to Google Sheets:

```bash
pip install gspread oauth2client
```

(I can run this for you).
