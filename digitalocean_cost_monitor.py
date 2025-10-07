#!/usr/bin/env python3
"""
DigitalOcean Cost Monitor
Helps monitor and manage DigitalOcean resources to avoid unnecessary costs
"""

import subprocess
import json
import sys

def check_doctl_installed():
    """Check if doctl is installed"""
    try:
        result = subprocess.run(['doctl', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ DigitalOcean CLI (doctl) is installed")
            return True
        else:
            print("❌ DigitalOcean CLI (doctl) not found")
            return False
    except FileNotFoundError:
        print("❌ DigitalOcean CLI (doctl) not found")
        return False

def list_apps():
    """List all DigitalOcean apps"""
    try:
        result = subprocess.run(['doctl', 'apps', 'list', '--format', 'json'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            apps = json.loads(result.stdout)
            print(f"\n📱 DigitalOcean Apps ({len(apps)} total):")
            print("-" * 50)
            for app in apps:
                print(f"Name: {app['spec']['name']}")
                print(f"ID: {app['id']}")
                print(f"State: {app['last_deployment_active_at']}")
                print(f"URL: {app.get('live_url', 'N/A')}")
                print("-" * 30)
            return apps
        else:
            print(f"❌ Error listing apps: {result.stderr}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def get_app_cost_estimate(app_id):
    """Get cost estimate for an app"""
    try:
        result = subprocess.run(['doctl', 'apps', 'get', app_id, '--format', 'json'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            app_data = json.loads(result.stdout)
            # This is a simplified cost estimate
            # DigitalOcean provides more detailed cost info in their dashboard
            print(f"💰 Cost estimate for app {app_id}: Check DigitalOcean dashboard for detailed costs")
            return True
        else:
            print(f"❌ Error getting app details: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def delete_app(app_id, app_name):
    """Delete a DigitalOcean app"""
    try:
        confirm = input(f"⚠️  Are you sure you want to delete app '{app_name}' (ID: {app_id})? This cannot be undone! (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            result = subprocess.run(['doctl', 'apps', 'delete', app_id, '--force'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Successfully deleted app '{app_name}'")
                return True
            else:
                print(f"❌ Error deleting app: {result.stderr}")
                return False
        else:
            print("❌ Deletion cancelled")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔍 DigitalOcean Cost Monitor")
    print("=" * 40)
    
    if not check_doctl_installed():
        print("\n📥 To install doctl:")
        print("   brew install doctl")
        print("   doctl auth init")
        return
    
    apps = list_apps()
    
    if not apps:
        print("No apps found or error occurred")
        return
    
    print(f"\n💡 Cost Management Tips:")
    print("1. Keep only the apps you need")
    print("2. Monitor usage in DigitalOcean dashboard")
    print("3. Set up billing alerts")
    print("4. Consider using smaller droplet sizes if possible")
    
    print(f"\n🛠️  Management Options:")
    print("1. Delete unused apps")
    print("2. View app details")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🗑️  Delete Apps:")
        for i, app in enumerate(apps):
            print(f"{i+1}. {app['spec']['name']} (ID: {app['id']})")
        
        try:
            app_choice = int(input("\nEnter app number to delete (0 to cancel): ")) - 1
            if 0 <= app_choice < len(apps):
                app = apps[app_choice]
                delete_app(app['id'], app['spec']['name'])
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
    
    elif choice == "2":
        print("\n📊 App Details:")
        for i, app in enumerate(apps):
            print(f"{i+1}. {app['spec']['name']} (ID: {app['id']})")
        
        try:
            app_choice = int(input("\nEnter app number to view details (0 to cancel): ")) - 1
            if 0 <= app_choice < len(apps):
                app = apps[app_choice]
                get_app_cost_estimate(app['id'])
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
    
    elif choice == "3":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()

