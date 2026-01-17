#!/usr/bin/env python3
"""
Deployment helper script for Vercel
"""

import os
import subprocess
import sys

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'vercel.json',
        'api/index.py', 
        'requirements.txt',
        'app/__init__.py',
        'config.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Vercel CLI not found")
    print("Install with: npm i -g vercel")
    return False

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("\n🚀 Deploying to Vercel...")
    
    try:
        # Run vercel deploy
        result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(f"Output: {result.stdout}")
            
            # Extract URL from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and 'vercel.app' in line:
                    print(f"\n🌐 Your app is live at: {line.strip()}")
                    break
        else:
            print("❌ Deployment failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False
    
    return True

def main():
    """Main deployment process"""
    print("🔧 Vercel Deployment Helper")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please ensure all required files are present")
        sys.exit(1)
    
    # Check Vercel CLI
    if not check_vercel_cli():
        print("\n❌ Please install Vercel CLI first")
        sys.exit(1)
    
    # Deploy
    if deploy_to_vercel():
        print("\n🎉 Deployment completed successfully!")
        print("\n📋 Next steps:")
        print("1. Set up your database (PostgreSQL)")
        print("2. Configure environment variables in Vercel dashboard")
        print("3. Test your live application")
    else:
        print("\n❌ Deployment failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()