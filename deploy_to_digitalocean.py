#!/usr/bin/env python3
"""
DigitalOcean App Platform Deployment Script
Deploys the Education Jobs Dashboard to DigitalOcean App Platform
"""

import subprocess
import sys
import os
import json
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_doctl():
    """Check if doctl CLI is installed"""
    print("🔍 Checking DigitalOcean CLI (doctl)...")
    result = subprocess.run("doctl version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ doctl is installed")
        return True
    else:
        print("❌ doctl is not installed")
        print("📥 Please install doctl first:")
        print("   brew install doctl")
        print("   or visit: https://docs.digitalocean.com/reference/doctl/how-to/install/")
        return False

def check_authentication():
    """Check if user is authenticated with DigitalOcean"""
    print("🔍 Checking DigitalOcean authentication...")
    result = subprocess.run("doctl account get", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Authenticated with DigitalOcean")
        return True
    else:
        print("❌ Not authenticated with DigitalOcean")
        print("🔐 Please authenticate first:")
        print("   doctl auth init")
        return False

def create_app_spec():
    """Create DigitalOcean App Platform specification file"""
    print("📝 Creating App Platform specification...")
    
    app_spec = {
        "name": "education-jobs-dashboard",
        "services": [
            {
                "name": "web",
                "source_dir": "/",
                "github": {
                    "repo": "yaro360/EducationEdJoin",
                    "branch": "main",
                    "deploy_on_push": True
                },
                "run_command": "gunicorn app:app",
                "environment_slug": "python",
                "instance_count": 1,
                "instance_size_slug": "basic-xxs",
                "http_port": 8080,
                "routes": [
                    {
                        "path": "/"
                    }
                ],
                "envs": [
                    {
                        "key": "FLASK_ENV",
                        "value": "production"
                    },
                    {
                        "key": "SECRET_KEY",
                        "value": "your-super-secret-key-change-this-in-production"
                    }
                ]
            }
        ],
        "static_sites": [],
        "workers": [],
        "jobs": [
            {
                "name": "scraper",
                "source_dir": "/",
                "github": {
                    "repo": "yaro360/EducationEdJoin",
                    "branch": "main"
                },
                "run_command": "python3 production_scraper.py",
                "environment_slug": "python",
                "instance_count": 1,
                "instance_size_slug": "basic-xxs",
                "envs": [
                    {
                        "key": "FLASK_ENV",
                        "value": "production"
                    }
                ]
            }
        ]
    }
    
    with open("app.yaml", "w") as f:
        json.dump(app_spec, f, indent=2)
    
    print("✅ App specification created (app.yaml)")
    return True

def deploy_to_digitalocean():
    """Deploy the application to DigitalOcean App Platform"""
    print("🚀 Deploying to DigitalOcean App Platform...")
    
    # Create app specification
    if not create_app_spec():
        return False
    
    # Deploy using doctl
    deploy_command = "doctl apps create --spec app.yaml"
    if not run_command(deploy_command, "Creating DigitalOcean app"):
        return False
    
    print("✅ Deployment initiated!")
    print("📊 Check your DigitalOcean dashboard for deployment status")
    print("🌐 Your app will be available at: https://your-app-name.ondigitalocean.app")
    
    return True

def main():
    """Main deployment function"""
    print("🚀 DigitalOcean App Platform Deployment")
    print("=" * 50)
    
    # Check prerequisites
    if not check_doctl():
        return False
    
    if not check_authentication():
        return False
    
    # Deploy
    if deploy_to_digitalocean():
        print("\n🎉 Deployment completed successfully!")
        print("\n📋 Next steps:")
        print("1. Check your DigitalOcean dashboard")
        print("2. Wait for deployment to complete (5-10 minutes)")
        print("3. Your app will be available at the provided URL")
        print("4. Set up environment variables in the DigitalOcean dashboard")
        print("5. Configure Google Forms integration")
        return True
    else:
        print("\n❌ Deployment failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
