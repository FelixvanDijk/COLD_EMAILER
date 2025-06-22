#!/usr/bin/env python3
"""
Setup Script for Cold Email Outreach System
Helps initialize the system and create necessary files
"""

import os
import shutil

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('env_example.txt'):
        try:
            shutil.copy('env_example.txt', '.env')
            print("✅ Created .env file from template")
            print("📝 Please edit .env with your email credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {str(e)}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def create_sample_csv():
    """Create sample Apollo CSV if it doesn't exist"""
    csv_filename = 'apollo-contacts-export.csv'
    
    if os.path.exists(csv_filename):
        print(f"✅ {csv_filename} already exists")
        return True
    
    if os.path.exists('sample_apollo_contacts.csv'):
        try:
            shutil.copy('sample_apollo_contacts.csv', csv_filename)
            print(f"✅ Created {csv_filename} from sample")
            print("📝 Replace with your actual Apollo export data")
            return True
        except Exception as e:
            print(f"❌ Failed to create {csv_filename}: {str(e)}")
            return False
    else:
        # Create basic CSV structure
        csv_content = """First Name,Last Name,Email,Organization Name,Title,City,State,Country
John,Smith,john.smith@example.com,TechCorp Inc,Software Engineer,San Francisco,CA,USA
Jane,Doe,jane.doe@demo.com,Marketing Solutions,Marketing Manager,New York,NY,USA"""
        
        try:
            with open(csv_filename, 'w') as f:
                f.write(csv_content)
            print(f"✅ Created basic {csv_filename}")
            print("📝 Replace with your actual Apollo export data")
            return True
        except Exception as e:
            print(f"❌ Failed to create {csv_filename}: {str(e)}")
            return False

def check_python_version():
    """Check if Python version is compatible"""
    import sys
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 6:
        print(f"✅ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.6+")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'email_sender.py',
        'lead_loader.py',
        'template_engine.py',
        'warmup_sender.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required system files present")
        return True

def show_next_steps():
    """Show user what to do next"""
    print("\n" + "=" * 50)
    print("🎉 Setup Complete! Next Steps:")
    print("=" * 50)
    
    print("\n1. 📧 Configure Email Credentials:")
    print("   - Edit .env file with your email settings")
    print("   - Use app-specific passwords, not your main password")
    print("   - For Zoho: smtp.zoho.com:465")
    print("   - For Gmail: smtp.gmail.com:465")
    
    print("\n2. 📋 Prepare Your Leads:")
    print("   - Export leads from Apollo as CSV")
    print("   - Replace apollo-contacts-export.csv with your data")
    print("   - Ensure columns match required format")
    
    print("\n3. 🧪 Test the System:")
    print("   python test_system.py")
    
    print("\n4. 🚀 Run the System:")
    print("   python main.py")
    
    print("\n📚 Need Help?")
    print("   - Read README.md for detailed instructions")
    print("   - Check troubleshooting section for common issues")

def main():
    """Run setup process"""
    print("🛠️  Cold Email System Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check required files
    if not check_required_files():
        print("❌ System files missing. Please download complete system.")
        return False
    
    # Create configuration files
    print("\n📝 Creating configuration files...")
    create_env_file()
    create_sample_csv()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check errors above.")
        exit(1)
    else:
        print("\n✨ Setup completed successfully!")
        exit(0) 