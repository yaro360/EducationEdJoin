#!/usr/bin/env python3
"""
Simple Heroku Deployment Script
Handles the deployment process step by step
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error {description}: {e.stderr}")
        return None

def main():
    """Main deployment function"""
    print("🚀 Simple Heroku Deployment for Education Jobs Sourcing Tool")
    print("=" * 60)
    
    app_name = "education-jobs-rosa"
    print(f"📱 App name: {app_name}")
    print()
    
    # Step 1: Check if logged in to Heroku
    print("🔍 Checking Heroku login status...")
    result = run_command("heroku auth:whoami", "Checking Heroku login")
    if result is None:
        print("❌ Not logged in to Heroku. Please run: heroku login")
        print("   Then run this script again.")
        return
    
    print(f"✅ Logged in as: {result.strip()}")
    
    # Step 2: Create Heroku app
    print(f"\n🚀 Creating Heroku app: {app_name}")
    result = run_command(f"heroku create {app_name}", f"Creating Heroku app {app_name}")
    if result is None:
        print("⚠️ App might already exist, continuing...")
    
    # Step 3: Set environment variables
    print("\n⚙️ Setting environment variables...")
    run_command(f"heroku config:set FLASK_ENV=production --app {app_name}", "Setting FLASK_ENV")
    run_command(f"heroku config:set SECRET_KEY=your-super-secret-key-change-this-in-production --app {app_name}", "Setting SECRET_KEY")
    
    # Step 4: Deploy to Heroku
    print("\n🚀 Deploying to Heroku...")
    result = run_command(f"git push heroku main", "Deploying to Heroku")
    if result is None:
        print("❌ Deployment failed")
        return
    
    # Step 5: Run initial scraper
    print("\n🔄 Running initial job scraper...")
    run_command(f"heroku run python3 production_scraper.py --app {app_name}", "Running initial scraper")
    
    # Step 6: Get app URL
    print("\n🌐 Getting app URL...")
    result = run_command(f"heroku apps:info --app {app_name}", "Getting app info")
    if result:
        # Extract URL from the output
        lines = result.split('\n')
        for line in lines:
            if 'Web URL:' in line:
                app_url = line.split('Web URL:')[1].strip()
                break
        else:
            app_url = f"https://{app_name}.herokuapp.com"
    else:
        app_url = f"https://{app_name}.herokuapp.com"
    
    print(f"\n🎉 Deployment successful!")
    print(f"🌐 Your app is live at: {app_url}")
    print()
    print("📋 Available URLs:")
    print(f"   Main Dashboard: {app_url}")
    print(f"   Embed Widget: {app_url}/embed-enhanced")
    print(f"   Admin Panel: {app_url}/admin/applications")
    print()
    print("🔗 Squarespace Embed Code:")
    print(f"""
<div id="education-jobs-widget">
    <iframe 
        src="{app_url}/embed-enhanced" 
        width="100%" 
        height="800" 
        frameborder="0"
        style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    </iframe>
</div>
    """)
    print()
    print("🎯 Next Steps:")
    print("1. Copy the embed code above to your Squarespace site")
    print("2. Test the job board functionality")
    print("3. Set up Heroku Scheduler for auto-refresh:")
    print(f"   heroku addons:create scheduler:standard --app {app_name}")
    print("4. Add scheduled job:")
    print("   Command: python3 production_scraper.py")
    print("   Frequency: Daily at 06:00 UTC")
    print()
    print("🚀 Your Education Jobs Sourcing Tool is now live!")

if __name__ == "__main__":
    main()
