#!/usr/bin/env python3
import os

def load_env_file():
    """Load environment variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
                    print(f"Loaded: {key.strip()} = {value.strip()}")
    except FileNotFoundError:
        print("❌ Error: .env file not found")
        return False
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    return True

def validate_env_vars():
    """Validate required environment variables are present"""
    required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {value if var != 'EMAIL_PASSWORD' else '***'}")
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All environment variables are set correctly")
    return True

if __name__ == "__main__":
    print("Testing environment variables...")
    if load_env_file():
        validate_env_vars() 