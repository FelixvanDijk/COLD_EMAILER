#!/usr/bin/env python3
"""
Email Sender Module - Handles SMTP email sending with HTML support and logging
"""

import smtplib
import ssl
import os
import csv
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional

class EmailSender:
    def __init__(self, sent_log_file: str = 'sent_log.csv'):
        self.sent_log_file = sent_log_file
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.zoho.eu')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.email_address = os.environ.get('EMAIL_ADDRESS')
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
        # Initialize sent log file
        self._initialize_sent_log()
    
    def _initialize_sent_log(self):
        """Initialize the sent log CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.sent_log_file):
            with open(self.sent_log_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'timestamp', 'email', 'subject', 'status', 'type', 
                    'first_name', 'last_name', 'organization', 'template_used', 'followup_sequence'
                ])
    
    def send_email(self, to_email: str, subject: str, body: str, lead_data: Dict = None, 
                   email_type: str = 'cold', template_index: int = None, followup_sequence: int = None) -> bool:
        """
        Send an email with HTML formatting and logging
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body (HTML format)
            lead_data (Dict): Lead information for logging
            email_type (str): Type of email ('cold', 'warmup', 'followup')
            template_index (int): Template index used (for logging)
            followup_sequence (int): Follow-up sequence number (for follow-up emails)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.email_address or not self.email_password:
            print("❌ Email credentials not configured")
            return False
            
        for attempt in range(self.max_retries):
            try:
                # Create message
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = self.email_address
                message["To"] = to_email
                
                # Create both plain text and HTML versions
                text_body = self._html_to_text(body)
                html_body = body
                
                # Add both versions to message
                text_part = MIMEText(text_body, "plain")
                html_part = MIMEText(html_body, "html")
                
                message.attach(text_part)
                message.attach(html_part)
                
                # Create secure SSL context and send
                context = ssl.create_default_context()
                
                # Try STARTTLS first (port 587), then SSL (port 465)
                if self.smtp_port == 587:
                    # STARTTLS connection
                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls(context=context)
                        server.login(self.email_address, self.email_password)
                        text = message.as_string()
                        server.sendmail(self.email_address, to_email, text)
                elif self.smtp_port == 465:
                    # SSL connection
                    with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                        server.login(self.email_address, self.email_password)
                        text = message.as_string()
                        server.sendmail(self.email_address, to_email, text)
                else:
                    # Fallback: try STARTTLS first, then SSL
                    try:
                        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                            server.starttls(context=context)
                            server.login(self.email_address, self.email_password)
                            text = message.as_string()
                            server.sendmail(self.email_address, to_email, text)
                    except:
                        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                            server.login(self.email_address, self.email_password)
                            text = message.as_string()
                            server.sendmail(self.email_address, to_email, text)
                
                # Log successful send
                self._log_email(to_email, subject, 'sent', email_type, lead_data, template_index, followup_sequence)
                return True
                
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    print(f"🔄 Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"❌ Failed to send email to {to_email} after {self.max_retries} attempts")
                    self._log_email(to_email, subject, 'failed', email_type, lead_data, template_index, followup_sequence)
                    return False
        
        return False
    
    def _html_to_text(self, html_body: str) -> str:
        """
        Convert HTML email body to plain text version
        
        Args:
            html_body (str): HTML formatted email body
            
        Returns:
            str: Plain text version
        """
        # Simple HTML to text conversion
        text = html_body
        
        # Replace HTML paragraph tags with double newlines
        text = text.replace('<p>', '')
        text = text.replace('</p>', '\n\n')
        
        # Replace HTML line breaks
        text = text.replace('<br>', '\n')
        text = text.replace('<br/>', '\n')
        text = text.replace('<br />', '\n')
        
        # Remove any remaining HTML tags
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def _log_email(self, to_email: str, subject: str, status: str, email_type: str, 
                   lead_data: Dict = None, template_index: int = None, followup_sequence: int = None):
        """
        Log email send attempt to CSV file
        
        Args:
            to_email (str): Recipient email
            subject (str): Email subject
            status (str): Send status ('sent', 'failed')
            email_type (str): Type of email
            lead_data (Dict): Lead information
            template_index (int): Template index used
            followup_sequence (int): Follow-up sequence number
        """
        try:
            with open(self.sent_log_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                timestamp = datetime.now().isoformat()
                first_name = lead_data.get('first_name', '') if lead_data else ''
                last_name = lead_data.get('last_name', '') if lead_data else ''
                organization = lead_data.get('organization', '') if lead_data else ''
                
                # Generate template_used description
                if email_type == 'followup' and followup_sequence:
                    template_used = f"Follow-up {followup_sequence}"
                elif template_index:
                    template_used = f"Template {template_index}"
                else:
                    template_used = ''
                
                writer.writerow([
                    timestamp, to_email, subject, status, email_type,
                    first_name, last_name, organization, template_used, followup_sequence or ''
                ])
                
        except Exception as e:
            print(f"⚠️ Warning: Could not log email: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test SMTP connection without sending email
        Try both STARTTLS (587) and SSL (465) connection methods
        
        Returns:
            bool: True if connection successful
        """
        try:
            # First try STARTTLS (port 587)
            if self.smtp_port == 587:
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.email_address, self.email_password)
                    print("✅ SMTP connection test successful (STARTTLS)")
                    return True
            
            # Try SSL connection (port 465)
            elif self.smtp_port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.email_address, self.email_password)
                    print("✅ SMTP connection test successful (SSL)")
                    return True
            
            # Fallback: try both methods
            else:
                # Try STARTTLS first
                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls(context=context)
                        server.login(self.email_address, self.email_password)
                        print("✅ SMTP connection test successful (STARTTLS fallback)")
                        return True
                except:
                    # Try SSL
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                        server.login(self.email_address, self.email_password)
                        print("✅ SMTP connection test successful (SSL fallback)")
                        return True
                        
        except Exception as e:
            print(f"❌ SMTP connection test failed: {str(e)}")
            print("💡 Try updating your .env file with:")
            print("   SMTP_SERVER=smtp.zoho.eu")
            print("   SMTP_PORT=465")
            return False
    
    def get_send_statistics(self) -> Dict:
        """
        Get email sending statistics from log
        
        Returns:
            Dict: Statistics about sent emails
        """
        stats = {
            'total_sent': 0,
            'cold_emails': 0,
            'warmup_emails': 0,
            'failed_emails': 0,
            'success_rate': 0.0
        }
        
        if not os.path.exists(self.sent_log_file):
            return stats
            
        try:
            with open(self.sent_log_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                total_attempts = 0
                for row in reader:
                    total_attempts += 1
                    
                    if row.get('status') == 'sent':
                        stats['total_sent'] += 1
                        if row.get('type') == 'warmup':
                            stats['warmup_emails'] += 1
                        else:
                            stats['cold_emails'] += 1
                    else:
                        stats['failed_emails'] += 1
                
                if total_attempts > 0:
                    stats['success_rate'] = (stats['total_sent'] / total_attempts) * 100
                    
        except Exception as e:
            print(f"⚠️ Warning: Could not read email statistics: {str(e)}")
            
        return stats
    
    def add_random_delay(self, delay_type: str = 'cold'):
        """
        Add random delay between emails to avoid spam detection
        
        Args:
            delay_type (str): Type of delay ('cold' or 'warmup')
        """
        if delay_type == 'warmup':
            delay = random.randint(60, 180)  # 1-3 minutes for warmup
        else:
            delay = random.randint(30, 120)  # 30 seconds to 2 minutes for cold emails
            
        print(f"⏱️  Adding random delay: {delay} seconds...")
        time.sleep(delay)
    
    def validate_email_address(self, email: str) -> bool:
        """
        Basic email address validation
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email appears valid
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def get_daily_send_count(self, date: str = None) -> Dict:
        """
        Get count of emails sent on a specific date
        
        Args:
            date (str): Date in YYYY-MM-DD format (defaults to today)
            
        Returns:
            Dict: Send counts by type
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        counts = {'cold': 0, 'warmup': 0, 'total': 0}
        
        if not os.path.exists(self.sent_log_file):
            return counts
            
        try:
            with open(self.sent_log_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    if row.get('status') == 'sent' and date in row.get('timestamp', ''):
                        email_type = row.get('type', 'cold')
                        counts[email_type] += 1
                        counts['total'] += 1
                        
        except Exception as e:
            print(f"⚠️ Warning: Could not read daily send count: {str(e)}")
            
        return counts 