#!/usr/bin/env python3
"""
Setup script for UFRGS Vestibular Test LLM Processor
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


def install_requirements():
    """Install required packages."""
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False


def setup_env_file():
    """Set up the .env file from .env.example."""
    if os.path.exists('.env'):
        print("\n✓ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        print("\nSetting up .env file...")
        try:
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            print("✓ .env file created from .env.example")
            print("\n" + "="*60)
            print("IMPORTANT: Edit the .env file and add your OpenAI API key!")
            print("="*60)
            return True
        except Exception as e:
            print(f"✗ Error creating .env file: {e}")
            return False
    else:
        print("\n✗ .env.example file not found")
        return False


def main():
    """Main setup function."""
    print("="*60)
    print("UFRGS Vestibular Test LLM Processor - Setup")
    print("="*60)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    if not install_requirements():
        print("\nSetup failed. Please fix the errors and try again.")
        sys.exit(1)
    
    # Setup .env file
    setup_env_file()
    
    print("\n" + "="*60)
    print("✓ Setup completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Get your API key from: https://platform.openai.com/api-keys")
    print("3. Run the application: python src/main.py")
    print("\nFor more information, see README.md")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error during setup: {e}")
        sys.exit(1)
