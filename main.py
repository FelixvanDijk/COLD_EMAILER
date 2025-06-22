#!/usr/bin/env python3
"""
Cold Email Outreach System - Main Entry Point with Advanced Sending Logic
"""

import os
import sys
import random
import datetime
from lead_loader import LeadLoader
from email_sender import EmailSender  
from template_engine import TemplateEngine
from warmup_sender import WarmupSender

# Daily limits
DAILY_COLD_EMAIL_LIMIT = 15
DAILY_WARMUP_EMAIL_LIMIT = 5

def load_env_file():
    """Load environment variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8-sig') as f:  # Handle BOM
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    except FileNotFoundError:
        print("❌ Error: .env file not found. Please create one based on .env.example")
        sys.exit(1)
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    return env_vars

def validate_env_vars():
    """Validate required environment variables are present"""
    required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all variables are set.")
        sys.exit(1)

def get_today_sent_count():
    """Get count of emails sent today from log"""
    today = datetime.date.today().isoformat()
    cold_count = 0
    warmup_count = 0
    
    try:
        with open('sent_log.csv', 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                if line.strip() and today in line and 'sent' in line:
                    if 'warmup' in line.lower():
                        warmup_count += 1
                    else:
                        cold_count += 1
    except FileNotFoundError:
        # Log file doesn't exist yet, no emails sent today
        pass
    
    return cold_count, warmup_count

def send_warmup_batch(email_sender, warmup_sender, count):
    """Send a batch of warmup emails with random delays"""
    print(f"🔥 Sending {count} warmup emails...")
    
    success_count = 0
    for i in range(count):
        try:
            # Get warmup email details
            warmup_email = warmup_sender.get_random_warmup_email()
            subject = warmup_sender.get_warmup_subject()
            body = warmup_sender.get_warmup_body()
            
            print(f"📧 Warmup email {i+1}/{count} to {warmup_email}...")
            
            # Send warmup email
            if email_sender.send_email(warmup_email, subject, body, 
                                     email_type='warmup'):
                success_count += 1
                print(f"✅ Warmup email sent successfully")
            else:
                print(f"❌ Failed to send warmup email")
            
            # Add random delay between warmup emails (except for last one)
            if i < count - 1:
                email_sender.add_random_delay('warmup')
                
        except Exception as e:
            print(f"❌ Error sending warmup email: {str(e)}")
            continue
    
    return success_count

def send_cold_batch(email_sender, template_engine, leads, count):
    """Send a batch of cold emails with random delays and rotating templates"""
    print(f"📧 Sending {count} cold emails...")
    
    success_count = 0
    for i in range(min(count, len(leads))):
        try:
            lead = leads[i]
            print(f"📤 Cold email {i+1}/{count} to {lead['first_name']} at {lead['organization']}...")
            
            # Get personalized email with rotating template
            subject, body = template_engine.get_template_pair(lead)
            
            # Send cold email
            if email_sender.send_email(lead['email'], subject, body, lead, 
                                     email_type='cold'):
                success_count += 1
                print(f"✅ Successfully sent to {lead['email']}")
            else:
                print(f"❌ Failed to send to {lead['email']}")
            
            # Add random delay between cold emails (except for last one)
            if i < count - 1:
                email_sender.add_random_delay('cold')
                
        except Exception as e:
            print(f"❌ Error processing lead {lead.get('email', 'unknown')}: {str(e)}")
            continue
    
    return success_count

def main():
    print("🚀 Starting Advanced Cold Email Outreach System...")
    print("=" * 60)
    print("📋 Features: Rotating Templates | Random Delays | Smart Alternating")
    print("=" * 60)
    
    # Load and validate environment
    load_env_file()
    validate_env_vars()
    
    # Check today's sent count
    cold_sent_today, warmup_sent_today = get_today_sent_count()
    print(f"📊 Today's Progress:")
    print(f"   Cold emails sent: {cold_sent_today}/{DAILY_COLD_EMAIL_LIMIT}")
    print(f"   Warmup emails sent: {warmup_sent_today}/{DAILY_WARMUP_EMAIL_LIMIT}")
    
    # Check if daily limits already reached
    if cold_sent_today >= DAILY_COLD_EMAIL_LIMIT and warmup_sent_today >= DAILY_WARMUP_EMAIL_LIMIT:
        print(f"\n✅ All daily limits reached!")
        return
    
    # Initialize components
    try:
        lead_loader = LeadLoader('apollo-contacts-export.csv')
        email_sender = EmailSender()
        template_engine = TemplateEngine()
        warmup_sender = WarmupSender()
        
        print(f"\n🎯 Template Engine loaded with {template_engine.get_template_count()} rotating templates")
        
        # Test SMTP connection first
        print(f"\n🔗 Testing SMTP connection...")
        if not email_sender.test_connection():
            print("❌ SMTP connection failed. Please check your credentials.")
            sys.exit(1)
        
        # Load leads for cold emails
        remaining_cold = DAILY_COLD_EMAIL_LIMIT - cold_sent_today
        leads = []
        
        if remaining_cold > 0:
            print(f"\n📋 Loading leads for {remaining_cold} cold emails...")
            leads = lead_loader.load_leads()
            
            if not leads:
                print("✅ No new leads to process. All leads have been contacted.")
                remaining_cold = 0
            else:
                print(f"📋 Found {len(leads)} uncontacted leads")
        
        # PHASE 1: Send initial warmup batch (5 emails)
        remaining_warmup = DAILY_WARMUP_EMAIL_LIMIT - warmup_sent_today
        if remaining_warmup > 0:
            initial_warmup_count = min(5, remaining_warmup)
            print(f"\n🔥 PHASE 1: Initial warmup batch ({initial_warmup_count} emails)")
            
            warmup_success = send_warmup_batch(email_sender, warmup_sender, initial_warmup_count)
            warmup_sent_today += warmup_success
            remaining_warmup -= warmup_success
            
            print(f"✅ Phase 1 complete: {warmup_success}/{initial_warmup_count} warmup emails sent")
        
        # PHASE 2: Alternating pattern (1 warmup → 3 cold → 1 warmup → 3 cold...)
        if remaining_cold > 0 or remaining_warmup > 0:
            print(f"\n📧 PHASE 2: Alternating send pattern")
            print(f"   Pattern: 1 warmup → 3 cold → 1 warmup → 3 cold...")
            
            cold_sent_phase2 = 0
            warmup_sent_phase2 = 0
            leads_index = 0
            
            while (cold_sent_phase2 < remaining_cold or warmup_sent_phase2 < remaining_warmup) and leads_index < len(leads):
                
                # Send 1 warmup email (if quota available)
                if warmup_sent_phase2 < remaining_warmup:
                    print(f"\n🔄 Alternating: Sending 1 warmup email...")
                    warmup_batch_success = send_warmup_batch(email_sender, warmup_sender, 1)
                    warmup_sent_phase2 += warmup_batch_success
                    warmup_sent_today += warmup_batch_success
                
                # Send 3 cold emails (if quota and leads available)
                if cold_sent_phase2 < remaining_cold and leads_index < len(leads):
                    cold_batch_size = min(3, remaining_cold - cold_sent_phase2, len(leads) - leads_index)
                    print(f"\n🔄 Alternating: Sending {cold_batch_size} cold emails...")
                    cold_batch_leads = leads[leads_index:leads_index + cold_batch_size]
                    
                    cold_batch_success = send_cold_batch(email_sender, template_engine, 
                                                       cold_batch_leads, cold_batch_size)
                    cold_sent_phase2 += cold_batch_success
                    cold_sent_today += cold_batch_success
                    leads_index += cold_batch_size
                
                # Break if we've reached all limits
                if (cold_sent_today >= DAILY_COLD_EMAIL_LIMIT and 
                    warmup_sent_today >= DAILY_WARMUP_EMAIL_LIMIT):
                    break
            
            print(f"\n✅ Phase 2 complete:")
            print(f"   Cold emails: {cold_sent_phase2} sent")
            print(f"   Warmup emails: {warmup_sent_phase2} sent")
        
        # Final status
        print(f"\n🎉 Campaign completed!")
        print(f"📊 Final Daily Status:")
        print(f"   Cold emails: {cold_sent_today}/{DAILY_COLD_EMAIL_LIMIT}")
        print(f"   Warmup emails: {warmup_sent_today}/{DAILY_WARMUP_EMAIL_LIMIT}")
        
        # Show statistics
        stats = email_sender.get_send_statistics()
        if stats['total_sent'] > 0:
            print(f"\n📈 System Statistics:")
            print(f"   Total emails sent: {stats['total_sent']}")
            print(f"   Success rate: {stats['success_rate']:.1f}%")
            print(f"   Cold emails: {stats['cold_emails']}")
            print(f"   Warmup emails: {stats['warmup_emails']}")
        
        print(f"\n✨ Advanced cold email system completed successfully!")
        print(f"🎯 Templates rotated randomly | 📡 Smart delays applied | 🔄 Alternating pattern used")
        
    except FileNotFoundError as e:
        print(f"❌ Error: Required file not found - {str(e)}")
        print("Please ensure 'apollo-contacts-export.csv' exists in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 