#!/usr/bin/env python3
"""
Script to update API_URL in all web files for Railway deployment
Usage: python update_api_url.py <your-railway-backend-url>
Example: python update_api_url.py https://ai-platform-backend.up.railway.app
"""

import sys
import os
from pathlib import Path

def update_api_url(new_url):
    """Update API_URL in all web HTML files"""
    
    web_files = [
        'web/chat.html',
        'web/goals.html',
        'web/capabilities.html',
        'web/index.html',
        'web/login.html'
    ]
    
    old_pattern = "const API_URL = 'http://localhost:8000';"
    new_pattern = f"const API_URL = '{new_url}';"
    
    updated_files = []
    
    for file_path in web_files:
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_pattern in content:
            new_content = content.replace(old_pattern, new_pattern)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            updated_files.append(file_path)
            print(f"✅ Updated: {file_path}")
        else:
            print(f"ℹ️  No change needed: {file_path}")
    
    if updated_files:
        print(f"\n✅ Successfully updated {len(updated_files)} file(s)")
        print(f"📝 New API URL: {new_url}")
        print("\n🚀 Next steps:")
        print("   1. Commit and push changes to GitHub")
        print("   2. Railway will auto-deploy the updated frontend")
        print("   3. Test the live application")
    else:
        print("\n⚠️  No files were updated")

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_api_url.py <railway-backend-url>")
        print("Example: python update_api_url.py https://ai-platform-backend.up.railway.app")
        sys.exit(1)
    
    new_url = sys.argv[1].rstrip('/')
    
    # Validate URL
    if not new_url.startswith('https://'):
        print("❌ Error: URL must start with https://")
        print(f"   Got: {new_url}")
        sys.exit(1)
    
    print(f"🔄 Updating API_URL to: {new_url}\n")
    update_api_url(new_url)

if __name__ == "__main__":
    main()
