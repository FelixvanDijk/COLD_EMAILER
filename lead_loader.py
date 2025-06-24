"""
Lead Loader Module - Handles CSV reading, cleaning, deduplication, and follow-up tracking
"""

import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class LeadLoader:
    def __init__(self, csv_file: str, sent_log_file: str = 'sent_log.csv'):
        self.csv_file = csv_file
        self.sent_log_file = sent_log_file
        # Updated required columns for new Apollo format
        self.required_columns = ['First Name', 'Last Name', 'Email', 'Company', 'Title', 'City', 'State', 'Country']
        
        # Follow-up configuration
        self.followup_intervals = {
            1: 7,   # First follow-up after 7 days
            2: 14,  # Second follow-up after 14 days  
            3: 21   # Third follow-up after 21 days
        }
        self.max_followups = 3
        
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
    
    def load_followup_leads(self) -> List[Dict]:
        """
        Load leads that are ready for follow-up emails
        
        Returns:
            List[Dict]: List of leads ready for follow-up with sequence info
        """
        if not os.path.exists(self.csv_file):
            return []
        
        # Get email history with timestamps and sequences
        email_history = self._get_email_history()
        
        # Load all leads from CSV
        all_leads = self._load_all_leads_from_csv()
        
        followup_leads = []
        current_time = datetime.now()
        
        for lead in all_leads:
            email = lead['email'].lower()
            
            if email in email_history:
                history = email_history[email]
                
                # Determine next follow-up sequence
                next_sequence = self._get_next_followup_sequence(history)
                
                if next_sequence and next_sequence <= self.max_followups:
                    # Check if enough time has passed for this follow-up
                    last_sent_time = history['last_sent']
                    days_since_last = (current_time - last_sent_time).days
                    required_days = self.followup_intervals.get(next_sequence, 7)
                    
                    if days_since_last >= required_days:
                        lead['followup_sequence'] = next_sequence
                        lead['days_since_last'] = days_since_last
                        lead['last_sent'] = history['last_sent'].isoformat()
                        followup_leads.append(lead)
        
        print(f"📋 Found {len(followup_leads)} leads ready for follow-up")
        return followup_leads
    
    def _get_email_history(self) -> Dict:
        """
        Get email sending history with timestamps and sequences
        
        Returns:
            Dict: Email history with timestamps and sequence tracking
        """
        history = {}
        
        if not os.path.exists(self.sent_log_file):
            return history
            
        try:
            with open(self.sent_log_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    if row.get('status') == 'sent' and row.get('email'):
                        email = row['email'].lower()
                        timestamp_str = row.get('timestamp', '')
                        email_type = row.get('type', 'cold')
                        
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00').replace('+00:00', ''))
                        except:
                            continue
                        
                        if email not in history:
                            history[email] = {
                                'first_sent': timestamp,
                                'last_sent': timestamp,
                                'send_count': 0,
                                'cold_count': 0,
                                'followup_count': 0,
                                'sequences': []
                            }
                        
                        history[email]['last_sent'] = max(history[email]['last_sent'], timestamp)
                        history[email]['send_count'] += 1
                        
                        if email_type == 'cold':
                            history[email]['cold_count'] += 1
                        elif email_type == 'followup':
                            history[email]['followup_count'] += 1
                            
                        # Track sequence if it's a follow-up
                        if 'followup' in email_type.lower():
                            # Try to extract sequence number from template_used field
                            template_used = row.get('template_used', '')
                            if 'Follow-up' in template_used:
                                try:
                                    seq = int(template_used.split()[-1])
                                    history[email]['sequences'].append(seq)
                                except:
                                    pass
                        
        except Exception as e:
            print(f"⚠️ Warning: Could not read email history: {e}")
            
        return history
    
    def _get_next_followup_sequence(self, history: Dict) -> Optional[int]:
        """
        Determine the next follow-up sequence number for a lead
        
        Args:
            history (Dict): Email history for the lead
            
        Returns:
            Optional[int]: Next follow-up sequence (1-3) or None if done
        """
        # If no follow-ups sent yet, start with sequence 1
        if history['followup_count'] == 0:
            return 1
        
        # Find the highest follow-up sequence sent
        sequences = history.get('sequences', [])
        if not sequences:
            # Fallback: use followup_count
            return min(history['followup_count'] + 1, self.max_followups + 1)
        
        max_sequence = max(sequences)
        next_sequence = max_sequence + 1
        
        return next_sequence if next_sequence <= self.max_followups else None
    
    def _load_all_leads_from_csv(self) -> List[Dict]:
        """Load all leads from CSV without filtering by sent status"""
        leads = []
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8', newline='') as file:
                # Try to detect if file has BOM
                first_char = file.read(1)
                if first_char != '\ufeff':
                    file.seek(0)
                
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        lead = self._process_row(row, row_num)
                        if lead:
                            leads.append(lead)
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Warning: Error loading leads for follow-up: {e}")
            
        return leads 