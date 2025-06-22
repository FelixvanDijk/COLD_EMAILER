#!/usr/bin/env python3
"""
Warmup Sender Module - Handles sending warmup emails to improve deliverability
"""

import random
from typing import List

class WarmupSender:
    def __init__(self):
        # Warmup email addresses (various services to improve deliverability)
        self.warmup_addresses = [
            'test@gmail.com',
            'warmup@outlook.com', 
            'hello@yahoo.com',
            'info@protonmail.com',
            'contact@icloud.com',
            'support@mail.com',
            'admin@tutanota.com',
            'noreply@zoho.com'
        ]
        
        # Simple warmup subject lines
        self.warmup_subjects = [
            "System Test",
            "Connection Check",
            "Delivery Test",
            "Mail System Verification",
            "SMTP Test Message"
        ]
        
        # Simple warmup body template
        self.warmup_body = """<p>This is an automated system test email.</p>

<p>This message is sent to verify email delivery and maintain sender reputation.</p>

<p>Please disregard this message.</p>

<p>Best regards,<br>
Email System</p>"""
    
    def get_random_warmup_email(self) -> str:
        """Get a random warmup email address"""
        return random.choice(self.warmup_addresses)
    
    def get_warmup_subject(self) -> str:
        """Get a random warmup subject line"""
        return random.choice(self.warmup_subjects)
    
    def get_warmup_body(self) -> str:
        """Get the warmup email body"""
        return self.warmup_body
    
    def get_warmup_addresses(self) -> List[str]:
        """Get all warmup email addresses"""
        return self.warmup_addresses.copy()
    
    def validate_warmup_setup(self) -> bool:
        """Validate warmup configuration"""
        if not self.warmup_addresses:
            return False
        if not self.warmup_subjects:
            return False
        if not self.warmup_body:
            return False
        return True
    
    def add_warmup_address(self, email: str):
        """Add a new warmup email address"""
        if email and email not in self.warmup_addresses:
            self.warmup_addresses.append(email)
    
    def remove_warmup_address(self, email: str):
        """Remove a warmup email address"""
        if email in self.warmup_addresses:
            self.warmup_addresses.remove(email) 