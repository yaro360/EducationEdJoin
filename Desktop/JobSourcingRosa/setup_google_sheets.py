"""
Setup script for Google Sheets integration
This script helps you set up Google Sheets API credentials
"""

import os
import json
from google.oauth2.service_account import Credentials
import gspread

def create_service_account_instructions():
    """Print instructions for creating Google service account"""
    print("=" * 60)
    print("GOOGLE SHEETS API SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one")
    print("3. Enable the Google Sheets API:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Google Sheets API'")
    print("   - Click 'Enable'")
    print()
    print("4. Create Service Account credentials:")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'Service Account'")
    print("   - Fill in the service account details")
    print("   - Click 'Create and Continue'")
    print("   - Skip role assignment for now")
    print("   - Click 'Done'")
    print()
    print("5. Create and download the key:")
    print("   - Click on the created service account")
    print("   - Go to 'Keys' tab")
    print("   - Click 'Add Key' > 'Create new key'")
    print("   - Choose 'JSON' format")
    print("   - Download the JSON file")
    print("   - Rename it to 'service_account.json'")
    print("   - Place it in this project directory")
    print()
    print("6. Create a Google Sheet:")
    print("   - Go to https://sheets.google.com")
    print("   - Create a new sheet")
    print("   - Name it 'EdJoin Education Jobs' (or your preferred name)")
    print("   - Share it with the service account email")
    print("   - Give 'Editor' permissions")
    print()
    print("7. Update the sheet name in config.py if different")
    print()
    print("=" * 60)

def test_google_sheets_connection():
    """Test the Google Sheets connection"""
    service_account_file = "service_account.json"
    
    if not os.path.exists(service_account_file):
        print("❌ service_account.json not found!")
        print("Please follow the setup instructions above.")
        return False
    
    try:
        # Test credentials
        creds = Credentials.from_service_account_file(service_account_file)
        client = gspread.authorize(creds)
        
        # Try to open the sheet
        sheet_name = "EdJoin Education Jobs"
        try:
            sheet = client.open(sheet_name).sheet1
            print(f"✅ Successfully connected to Google Sheet: {sheet_name}")
            return True
        except gspread.SpreadsheetNotFound:
            print(f"❌ Google Sheet '{sheet_name}' not found!")
            print("Please create the sheet and share it with the service account email.")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
        return False

def create_sample_sheet():
    """Create a sample sheet with headers"""
    try:
        creds = Credentials.from_service_account_file("service_account.json")
        client = gspread.authorize(creds)
        
        # Create or open the sheet
        try:
            sheet = client.open("EdJoin Education Jobs").sheet1
        except gspread.SpreadsheetNotFound:
            sheet = client.create("EdJoin Education Jobs").sheet1
        
        # Add headers
        headers = ["Role", "Title", "Location", "District", "Date Posted", "URL", "Scraped At"]
        sheet.clear()
        sheet.append_row(headers)
        
        print("✅ Sample sheet created with headers")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample sheet: {e}")
        return False

def main():
    """Main setup function"""
    print("Google Sheets Setup for Education Jobs Tool")
    print()
    
    # Show instructions
    create_service_account_instructions()
    
    # Test connection
    if test_google_sheets_connection():
        print()
        print("🎉 Google Sheets setup complete!")
        print("You can now run the scraper with: python edjoin_scraper.py")
        
        # Ask if user wants to create sample sheet
        response = input("\nWould you like to create a sample sheet with headers? (y/n): ")
        if response.lower() == 'y':
            create_sample_sheet()
    else:
        print()
        print("❌ Setup incomplete. Please follow the instructions above.")

if __name__ == "__main__":
    main()
