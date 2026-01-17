#!/usr/bin/env python3
"""
Simple test script to verify the CollabPlatform application works correctly
"""

import requests
import time
import sys

def test_application():
    """Test basic functionality of the application"""
    base_url = "http://localhost:5000"
    
    print("🚀 Testing CollabPlatform Application...")
    print("=" * 50)
    
    try:
        # Test 1: Homepage
        print("1. Testing homepage...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Homepage loads successfully")
        else:
            print(f"   ❌ Homepage failed with status {response.status_code}")
            return False
        
        # Test 2: Registration page
        print("2. Testing registration page...")
        response = requests.get(f"{base_url}/auth/register", timeout=5)
        if response.status_code == 200:
            print("   ✅ Registration page loads successfully")
        else:
            print(f"   ❌ Registration page failed with status {response.status_code}")
            return False
        
        # Test 3: Login page
        print("3. Testing login page...")
        response = requests.get(f"{base_url}/auth/login", timeout=5)
        if response.status_code == 200:
            print("   ✅ Login page loads successfully")
        else:
            print(f"   ❌ Login page failed with status {response.status_code}")
            return False
        
        # Test 4: Projects page
        print("4. Testing projects page...")
        response = requests.get(f"{base_url}/projects", timeout=5)
        if response.status_code == 200:
            print("   ✅ Projects page loads successfully")
        else:
            print(f"   ❌ Projects page failed with status {response.status_code}")
            return False
        
        print("\n🎉 All tests passed! The application is working correctly.")
        print("\n📋 Next Steps:")
        print("   1. Visit http://localhost:5000 to see the application")
        print("   2. Register as a company or developer")
        print("   3. Create projects or apply to existing ones")
        print("   4. Test the full workflow")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application.")
        print("   Make sure the Flask app is running on http://localhost:5000")
        print("   Run: python run.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1)