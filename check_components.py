#!/usr/bin/env python3
"""
Check DigitalOcean App Components
Helps identify and manage multiple components in a single app
"""

import subprocess
import json
import sys

def run_doctl_command(command):
    """Run a doctl command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_app_components():
    """Check components in the app"""
    print("🔍 Checking DigitalOcean App Components")
    print("=" * 50)
    
    # Get app list
    success, output, error = run_doctl_command("doctl apps list")
    if not success:
        print(f"❌ Error listing apps: {error}")
        return
    
    print("📱 Your DigitalOcean Apps:")
    print(output)
    
    # Get detailed app info
    app_id = "179fb823-46e7-49e7-bfc6-d6f54e969a72"
    success, output, error = run_doctl_command(f"doctl apps get {app_id}")
    if not success:
        print(f"❌ Error getting app details: {error}")
        return
    
    print(f"\n📊 App Details for {app_id}:")
    print(output)
    
    # Check if there are multiple components by looking at the app spec
    print("\n🔍 Checking for multiple components...")
    print("If you see 2 components at $24 each, it might be:")
    print("1. Multiple services in the same app")
    print("2. Multiple apps with similar names")
    print("3. App Platform pricing structure")
    
    print("\n💡 To reduce costs:")
    print("1. Check your DigitalOcean dashboard for detailed component breakdown")
    print("2. Look for any duplicate services or unnecessary components")
    print("3. Consider using a smaller droplet size if possible")

def check_billing():
    """Check billing information"""
    print("\n💰 Billing Information:")
    print("=" * 30)
    
    # This would require billing API access
    print("To check detailed billing:")
    print("1. Go to DigitalOcean Dashboard")
    print("2. Navigate to Billing section")
    print("3. Look for 'App Platform' charges")
    print("4. Check for multiple components or services")

def main():
    check_app_components()
    check_billing()
    
    print("\n🛠️  Next Steps:")
    print("1. Check your DigitalOcean dashboard")
    print("2. Look for duplicate components")
    print("3. If you find duplicates, we can help delete them")

if __name__ == "__main__":
    main()

