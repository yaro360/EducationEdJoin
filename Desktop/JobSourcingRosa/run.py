#!/usr/bin/env python3
"""
Main startup script for the Education Jobs Sourcing Tool
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        import bs4
        import flask
        import gspread
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'templates']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def run_scraper():
    """Run the EdJoin scraper"""
    print("🔄 Running EdJoin scraper...")
    try:
        result = subprocess.run([sys.executable, 'edjoin_scraper.py'], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Scraper completed successfully")
            return True
        else:
            print(f"⚠️ Scraper completed with warnings: {result.stderr}")
            return True
    except subprocess.TimeoutExpired:
        print("⚠️ Scraper timed out, but continuing...")
        return True
    except Exception as e:
        print(f"⚠️ Scraper error: {e}, but continuing...")
        return True

def start_web_app():
    """Start the Flask web application"""
    print("🚀 Starting web application...")
    print("Visit: http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def main():
    """Main function"""
    print("=" * 60)
    print("🎓 EDUCATION JOBS SOURCING TOOL")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create directories
    create_directories()
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Run scraper only")
    print("2. Start web app only")
    print("3. Run scraper + start web app")
    print("4. Setup Google Sheets integration")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        run_scraper()
    elif choice == "2":
        start_web_app()
    elif choice == "3":
        run_scraper()
        print("\n" + "="*40)
        start_web_app()
    elif choice == "4":
        print("Running Google Sheets setup...")
        subprocess.run([sys.executable, 'setup_google_sheets.py'])
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
