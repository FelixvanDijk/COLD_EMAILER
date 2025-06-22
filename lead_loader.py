"""
Lead Loader Module - Handles CSV reading, cleaning, and deduplication
"""

import csv
import os
from typing import List, Dict, Optional

class LeadLoader:
    def __init__(self, csv_file: str, sent_log_file: str = 'sent_log.csv'):
        self.csv_file = csv_file
        self.sent_log_file = sent_log_file
        # Updated required columns for new Apollo format
        self.required_columns = ['First Name', 'Last Name', 'Email', 'Company', 'Title', 'City', 'State', 'Country']
        
    def load_leads(self) -> List[Dict]:
        """Load and validate leads from CSV file"""
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
            
        leads = []
        sent_emails = self._load_sent_emails()
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8', newline='') as file:
                # Try to detect if file has BOM
                first_char = file.read(1)
                if first_char != '\ufeff':
                    file.seek(0)
                
                reader = csv.DictReader(file)
                
                # Validate required columns exist
                if not reader.fieldnames:
                    raise ValueError("CSV file appears to be empty or invalid")
                
                missing_columns = [col for col in self.required_columns if col not in reader.fieldnames]
                if missing_columns:
                    available_cols = ', '.join(reader.fieldnames) if reader.fieldnames else 'None'
                    raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}. Available columns: {available_cols}")
                
                print(f"📋 Available columns: {','.join(reader.fieldnames)}")
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 since row 1 is headers
                    try:
                        lead = self._process_row(row, row_num)
                        if lead and lead['email'].lower() not in sent_emails:
                            leads.append(lead)
                        elif lead:
                            print(f"⏭️ Skipping {lead['email']} - already contacted")
                    except Exception as e:
                        print(f"⚠️ Error processing row {row_num}: {e}")
                        continue
                        
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")
            
        print(f"✅ Loaded {len(leads)} new leads (excluding already contacted)")
        return leads
    
    def _process_row(self, row: Dict, row_num: int) -> Optional[Dict]:
        """Process and validate a single CSV row"""
        # Clean and validate email
        email = str(row.get('Email', '')).strip().lower()
        if not email or '@' not in email:
            print(f"⚠️ Row {row_num}: Invalid or missing email")
            return None
            
        # Extract and clean data - updated mapping for new Apollo format
        lead = {
            'first_name': str(row.get('First Name', '')).strip(),
            'last_name': str(row.get('Last Name', '')).strip(),
            'email': email,
            'organization': str(row.get('Company', '')).strip(),  # Updated to use 'Company'
            'title': str(row.get('Title', '')).strip(),
            'city': str(row.get('City', '')).strip(),
            'state': str(row.get('State', '')).strip(),
            'country': str(row.get('Country', '')).strip(),
            'website': str(row.get('Website', '')).strip(),
            'industry': str(row.get('Industry', '')).strip(),
        }
        
        # Validate required fields
        if not lead['first_name'] or not lead['last_name']:
            print(f"⚠️ Row {row_num}: Missing first name or last name")
            return None
            
        if not lead['organization']:
            print(f"⚠️ Row {row_num}: Missing organization name")
            return None
            
        return lead
    
    def _load_sent_emails(self) -> set:
        """Load previously sent email addresses from log file"""
        sent_emails = set()
        if os.path.exists(self.sent_log_file):
            try:
                with open(self.sent_log_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if 'email' in row and row['email']:
                            sent_emails.add(row['email'].lower())
            except Exception as e:
                print(f"⚠️ Warning: Could not load sent emails log: {e}")
        return sent_emails
    
    def get_lead_count(self) -> int:
        """Get total number of leads in CSV (for progress tracking)"""
        if not os.path.exists(self.csv_file):
            return 0
            
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                # Handle BOM
                first_char = file.read(1)
                if first_char != '\ufeff':
                    file.seek(0)
                
                reader = csv.reader(file)
                next(reader)  # Skip header
                return sum(1 for row in reader)
        except:
            return 0
    
    def get_lead_stats(self, leads: List[Dict]) -> Dict:
        """
        Get statistics about the loaded leads
        
        Args:
            leads (List[Dict]): List of leads
            
        Returns:
            Dict: Statistics about leads
        """
        if not leads:
            return {
                'total_leads': 0,
                'organizations': 0,
                'countries': 0,
                'with_titles': 0
            }
        
        organizations = set()
        countries = set()
        with_titles = 0
        
        for lead in leads:
            if lead.get('organization'):
                organizations.add(lead['organization'])
            if lead.get('country'):
                countries.add(lead['country'])
            if lead.get('title'):
                with_titles += 1
        
        return {
            'total_leads': len(leads),
            'organizations': len(organizations),
            'countries': len(countries),
            'with_titles': with_titles
        } 