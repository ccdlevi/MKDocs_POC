#!/usr/bin/env python3
"""
Confluence Publisher Helper Script

This script helps build the MkDocs site and publish it to Confluence.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import mkdocs
        import mkdocs_confluence_publisher
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def build_site():
    """Build the MkDocs site."""
    print("Building MkDocs site...")
    result = subprocess.run(["mkdocs", "build"], check=False)
    if result.returncode != 0:
        print("Error building MkDocs site.")
        return False
    return True

def publish_to_confluence():
    """Publish the site to Confluence."""
    print("Publishing to Confluence...")
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = [
        "https://dlevi93.atlassian.net", 
        "MKDocs", 
        "327683",
        "dlevi93@outlook.com",
        "ATATT3xFfGF03MLW8JRWKyUkrE5GgIC02ZNEPNXtrYPqYCtuyL9Tk-b-KWHpk2BJtTCGu0YRgSxfsBwPLluKz2CL5FVaWH8dIEKLZElCPHeKF6d68C0NaxLU2ekqVhCtuuIbt56zQLpkjrQC0GjbFFpqSMJOz_UVnTAmEaa3YMQAj9nI-mbLdtQ=CB666DF7"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required variables.")
        print("You can use .env.example as a template.")
        return False
    
    # Run the Confluence publisher
    result = subprocess.run(["python", "-m", "mkdocs_confluence_publisher"], check=False)
    if result.returncode != 0:
        print("Error publishing to Confluence.")
        return False
    
    print("Successfully published to Confluence!")
    return True

def main():
    """Main function."""
    if not check_dependencies():
        return 1
    
    if not build_site():
        return 1
    
    if len(sys.argv) > 1 and sys.argv[1] == "--publish":
        if not publish_to_confluence():
            return 1
    else:
        print("\nTo publish to Confluence, run: python publish.py --publish")
        print("Make sure to set up your .env file first.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
