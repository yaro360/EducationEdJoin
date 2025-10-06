#!/usr/bin/env python3
"""
Heroku Deployment Script for Education Jobs Sourcing Tool
Automates the deployment process
"""

import subprocess
import sys
import os
import json
from pathlib import Path

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

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git"):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Check if Heroku CLI is installed
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("❌ Heroku CLI is not installed.")
        print("📥 Please install from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    return True

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """uploads/
*.log
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore file")

def create_procfile():
    """Create Procfile for Heroku"""
    procfile_content = """web: gunicorn app:app
release: python3 production_scraper.py
"""
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    print("✅ Created Procfile")

def create_runtime_file():
    """Create runtime.txt for Python version"""
    runtime_content = "python-3.11.0"
    
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    print("✅ Created runtime.txt")

def update_requirements():
    """Update requirements.txt for production"""
    requirements = """requests==2.31.0
beautifulsoup4==4.12.2
gspread==5.12.4
google-auth==2.23.4
flask==3.0.0
selenium==4.15.2
webdriver-manager==4.0.1
schedule==1.2.0
python-dotenv==1.0.0
gunicorn==21.2.0
boto3==1.34.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Updated requirements.txt")

def initialize_git():
    """Initialize Git repository"""
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
    
    run_command("git add .", "Adding files to Git")
    run_command('git commit -m "Initial commit - Education Jobs Sourcing Tool"', "Creating initial commit")

def create_heroku_app(app_name):
    """Create Heroku app"""
    print(f"🚀 Creating Heroku app: {app_name}")
    
    # Check if app already exists
    result = run_command(f"heroku apps:info {app_name}", f"Checking if app {app_name} exists")
    if result is not None:
        print(f"✅ App {app_name} already exists")
        return True
    
    # Create new app
    result = run_command(f"heroku create {app_name}", f"Creating Heroku app {app_name}")
    return result is not None

def configure_heroku():
    """Configure Heroku environment variables"""
    print("⚙️ Configuring Heroku environment variables...")
    
    config_vars = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': 'your-super-secret-key-change-this-in-production',
        'PORT': '5000'
    }
    
    for key, value in config_vars.items():
        run_command(f"heroku config:set {key}={value}", f"Setting {key}")

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    # Push to Heroku
    result = run_command("git push heroku main", "Deploying to Heroku")
    if result is None:
        return False
    
    # Run initial scraper
    run_command("heroku run python3 production_scraper.py", "Running initial job scraper")
    
    return True

def setup_heroku_scheduler():
    """Set up Heroku Scheduler addon"""
    print("⏰ Setting up Heroku Scheduler...")
    
    # Add scheduler addon
    run_command("heroku addons:create scheduler:standard", "Adding Scheduler addon")
    
    print("📝 Manual setup required:")
    print("1. Go to: https://dashboard.heroku.com/apps/your-app-name/scheduler")
    print("2. Add job:")
    print("   Command: python3 production_scraper.py")
    print("   Frequency: Daily at 06:00 UTC")
    print("3. Save the job")

def get_app_url():
    """Get the deployed app URL"""
    result = run_command("heroku apps:info --json", "Getting app info")
    if result:
        try:
            app_info = json.loads(result)
            return app_info['app']['web_url']
        except:
            pass
    return None

def main():
    """Main deployment function"""
    print("🚀 Education Jobs Sourcing Tool - Heroku Deployment")
    print("=" * 60)
    
    # Get app name from user
    app_name = input("Enter your Heroku app name (or press Enter for 'education-jobs-rosa'): ").strip()
    if not app_name:
        app_name = "education-jobs-rosa"
    
    print(f"📱 App name: {app_name}")
    print()
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements not met. Please install missing tools.")
        return
    
    # Prepare files
    create_gitignore()
    create_procfile()
    create_runtime_file()
    update_requirements()
    
    # Initialize Git
    initialize_git()
    
    # Create Heroku app
    if not create_heroku_app(app_name):
        print("❌ Failed to create Heroku app")
        return
    
    # Configure Heroku
    configure_heroku()
    
    # Deploy
    if not deploy_to_heroku():
        print("❌ Deployment failed")
        return
    
    # Get app URL
    app_url = get_app_url()
    if app_url:
        print(f"🎉 Deployment successful!")
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
    else:
        print("✅ Deployment completed, but couldn't get app URL")
        print("Check your Heroku dashboard for the app URL")
    
    # Set up scheduler
    setup_heroku_scheduler()
    
    print()
    print("🎯 Next Steps:")
    print("1. Copy the embed code above to your Squarespace site")
    print("2. Set up Heroku Scheduler for auto-refresh")
    print("3. Test the job board functionality")
    print("4. Customize the styling to match your brand")
    print()
    print("🚀 Your Education Jobs Sourcing Tool is now live!")

if __name__ == "__main__":
    main()
