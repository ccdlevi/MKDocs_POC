#!/usr/bin/env python3
"""
Documentation Version Manager

This script helps manage multiple versions of documentation using the mike tool.
Mike allows you to deploy multiple versions of your documentation to GitHub Pages.

Requirements:
- mike (pip install mike)

Usage:
python version_docs.py --version 1.0.0 --alias latest
"""

import argparse
import subprocess
import re
import sys
import os

def validate_version(version):
    """Validate that the version is in the correct format."""
    pattern = r'^\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        raise ValueError(f"Version must be in format X.Y.Z, got {version}")
    return version

def validate_alias(alias):
    """Validate that the alias is valid."""
    pattern = r'^[a-z0-9\-_]+$'
    if not re.match(pattern, alias):
        raise ValueError(f"Alias must only contain lowercase letters, numbers, hyphens, and underscores. Got {alias}")
    return alias

def build_docs():
    """Build the documentation."""
    print("Building documentation...")
    result = subprocess.run(["mkdocs", "build", "--clean"], check=False)
    if result.returncode != 0:
        print("Error building the documentation.")
        sys.exit(1)

def deploy_version(version, alias=None, update_alias=False):
    """Deploy a specific version of the documentation."""
    build_docs()
    
    print(f"Deploying version {version}...")
    cmd = ["mike", "deploy", "--push", version]
    
    if alias:
        cmd.append(alias)
        
    if update_alias:
        cmd.append("--update-aliases")
    
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"Error deploying version {version}.")
        sys.exit(1)
    
    print(f"Version {version} deployed successfully!")
    
    # Set the default version if this is the latest version
    if alias == "latest":
        print("Setting as default version...")
        result = subprocess.run(["mike", "set-default", "--push", alias], check=False)
        if result.returncode != 0:
            print("Error setting the default version.")
            sys.exit(1)

def list_versions():
    """List all deployed versions."""
    print("Listing deployed versions...")
    subprocess.run(["mike", "list"], check=False)

def delete_version(version):
    """Delete a specific version."""
    print(f"Deleting version {version}...")
    result = subprocess.run(["mike", "delete", "--push", version], check=False)
    if result.returncode != 0:
        print(f"Error deleting version {version}.")
        sys.exit(1)
    print(f"Version {version} deleted successfully!")

def main():
    parser = argparse.ArgumentParser(description='Manage documentation versions with mike')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a documentation version')
    deploy_parser.add_argument('--version', required=True, type=validate_version, help='Version number (X.Y.Z)')
    deploy_parser.add_argument('--alias', type=validate_alias, help='Alias for the version (e.g., latest, stable)')
    deploy_parser.add_argument('--update-alias', action='store_true', help='Update existing aliases')
    
    # List command
    subparsers.add_parser('list', help='List all deployed versions')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a documentation version')
    delete_parser.add_argument('--version', required=True, help='Version or alias to delete')
    
    args = parser.parse_args()
    
    # Configure mkdocs.yml for versioning if not already configured
    mkdocs_file = 'mkdocs.yml'
    if os.path.exists(mkdocs_file):
        with open(mkdocs_file, 'r') as f:
            content = f.read()
            
        if 'version:' not in content and 'mike' not in content:
            print("Adding versioning configuration to mkdocs.yml...")
            with open(mkdocs_file, 'a') as f:
                f.write("\n\n# Version provider\nextra:\n  version:\n    provider: mike\n")
    
    # Execute the requested command
    if args.command == 'deploy':
        deploy_version(args.version, args.alias, args.update_alias)
    elif args.command == 'list':
        list_versions()
    elif args.command == 'delete':
        delete_version(args.version)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
