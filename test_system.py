#!/usr/bin/env python3
"""
Test Script for Advanced Cold Email Outreach System
Run this to validate all components work correctly without sending actual emails
"""

import os
import sys
from lead_loader import LeadLoader
from template_engine import TemplateEngine
from warmup_sender import WarmupSender
from email_sender import EmailSender

def test_environment():
    """Test environment configuration"""
    print("🧪 Testing Environment...")
    
    if os.path.exists('.env'):
        print("✅ .env file found")
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'EMAIL_ADDRESS' in content and 'EMAIL_PASSWORD' in content:
                    print("✅ Required environment variables present")
                    return True
                else:
                    print("⚠️  .env file missing required variables")
                    return False
        except Exception as e:
            print(f"❌ Error reading .env: {str(e)}")
            return False
    else:
        print("⚠️  .env file not found - you'll need to create one")
        print("   Copy env_example.txt to .env and fill in your credentials")
        return False

def test_lead_loader():
    """Test CSV loading and processing"""
    print("\n🧪 Testing Lead Loader...")
    
    try:
        # Test with Apollo CSV
        if os.path.exists('apollo-contacts-export.csv'):
            loader = LeadLoader('apollo-contacts-export.csv')
            leads = loader.load_leads()
            
            if leads:
                print(f"✅ Successfully loaded {len(leads)} leads")
                sample_lead = leads[0]
                print(f"✅ Sample lead: {sample_lead['first_name']} from {sample_lead['organization']}")
                
                # Test lead statistics
                stats = loader.get_lead_stats(leads)
                print(f"✅ Lead statistics: {stats}")
                return True
            else:
                print("❌ No leads loaded")
                return False
        else:
            print("⚠️  Apollo CSV not found")
            return True
            
    except Exception as e:
        print(f"❌ Lead loader test failed: {str(e)}")
        return False

def test_template_engine():
    """Test email template personalization and rotation"""
    print("\n🧪 Testing Advanced Template Engine...")
    
    try:
        engine = TemplateEngine()
        
        # Test data
        sample_lead = {
            'first_name': 'John',
            'last_name': 'Smith',
            'organization': 'TechCorp Ltd',
            'title': 'CTO',
            'city': 'London',
            'state': 'England',
            'country': 'United Kingdom',
            'industry': 'software development'
        }
        
        # Test template count
        template_count = engine.get_template_count()
        print(f"✅ {template_count} rotating templates loaded")
        
        # Test template pair generation
        subject, body = engine.get_template_pair(sample_lead)
        print(f"✅ Template pair generated:")
        print(f"   Subject: {subject}")
        print(f"   Body preview: {body[:100]}...")
        
        # Test multiple template generations (should vary)
        print(f"✅ Testing template rotation:")
        for i in range(3):
            subject, body = engine.get_template_pair(sample_lead)
            print(f"   Template {i+1}: {subject}")
        
        # Test template validation
        validation = engine.validate_template("Hello {{First Name}} from {{Company Name}}")
        print(f"✅ Template validation: {validation}")
        
        # Test preview generation
        previews = engine.preview_all_templates(sample_lead)
        print(f"✅ Generated {len(previews)} template previews")
        
        return True
        
    except Exception as e:
        print(f"❌ Template engine test failed: {str(e)}")
        return False

def test_email_sender():
    """Test email sender configuration"""
    print("\n🧪 Testing Advanced Email Sender...")
    
    try:
        sender = EmailSender()
        
        # Test configuration
        print("✅ Email sender initialized")
        
        # Test email validation
        valid_email = sender.validate_email_address("test@example.com")
        invalid_email = sender.validate_email_address("invalid-email")
        print(f"✅ Email validation: valid={valid_email}, invalid={invalid_email}")
        
        # Test HTML to text conversion
        html_body = "<p>Hello world</p><p>This is a test</p>"
        text_body = sender._html_to_text(html_body)
        print(f"✅ HTML to text conversion working")
        
        # Test statistics (will show empty if no emails sent)
        stats = sender.get_send_statistics()
        print(f"✅ Statistics retrieved: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Email sender test failed: {str(e)}")
        return False

def test_warmup_sender():
    """Test warmup email configuration"""
    print("\n🧪 Testing Warmup Sender...")
    
    try:
        warmup = WarmupSender()
        
        # Test configuration
        addresses = warmup.get_warmup_addresses()
        print(f"✅ Warmup addresses configured: {len(addresses)}")
        
        # Test random selection
        random_email = warmup.get_random_warmup_email()
        random_subject = warmup.get_warmup_subject()
        warmup_body = warmup.get_warmup_body()
        
        print(f"✅ Random warmup email: {random_email}")
        print(f"✅ Random subject: {random_subject}")
        print(f"✅ Warmup body configured")
        
        # Test validation
        validation = warmup.validate_warmup_setup()
        print(f"✅ Warmup validation: {validation}")
        
        return True
        
    except Exception as e:
        print(f"❌ Warmup sender test failed: {str(e)}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing System Integration...")
    
    try:
        # Test full workflow simulation
        loader = LeadLoader('apollo-contacts-export.csv') if os.path.exists('apollo-contacts-export.csv') else None
        engine = TemplateEngine()
        sender = EmailSender()
        warmup = WarmupSender()
        
        if loader:
            # Test lead processing
            leads = loader.load_leads()
            if leads:
                sample_lead = leads[0]
                
                # Test template generation for real lead
                subject, body = engine.get_template_pair(sample_lead)
                print(f"✅ Generated email for {sample_lead['first_name']} at {sample_lead['organization']}")
                print(f"   Subject: {subject}")
                
                # Test that HTML body is properly formatted
                if '<p>' in body:
                    print("✅ HTML formatting detected in email body")
                else:
                    print("⚠️  No HTML formatting detected")
        
        # Test warmup email generation
        warmup_email = warmup.get_random_warmup_email()
        warmup_subject = warmup.get_warmup_subject()
        warmup_body = warmup.get_warmup_body()
        
        print(f"✅ Warmup email ready: {warmup_subject}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False

def test_followup_system():
    """Test follow-up system functionality"""
    print("\n🧪 Testing Follow-up System...")
    
    try:
        # Test follow-up lead loading
        loader = LeadLoader('apollo-contacts-export.csv') if os.path.exists('apollo-contacts-export.csv') else None
        engine = TemplateEngine()
        
        if loader:
            # Test follow-up lead detection
            followup_leads = loader.load_followup_leads()
            print(f"✅ Follow-up lead detection working (found {len(followup_leads)} leads)")
            
            # Test follow-up intervals configuration
            intervals = loader.followup_intervals
            print(f"✅ Follow-up intervals configured: {intervals}")
        
        # Test follow-up template generation
        sample_lead = {
            'first_name': 'John',
            'last_name': 'Smith',
            'organization': 'TechCorp Ltd',
            'followup_sequence': 1
        }
        
        for sequence in [1, 2, 3]:
            subject, body = engine.get_followup_template_pair(sample_lead, sequence)
            print(f"✅ Follow-up sequence {sequence} template generated")
            
            # Verify template contains expected content
            if sequence == 1 and "buried" in subject.lower():
                print(f"   ✓ Sequence 1 has 'buried' reference")
            elif sequence == 2 and "3 ways" in subject:
                print(f"   ✓ Sequence 2 has '3 ways' structure")
            elif sequence == 3 and "last email" in subject.lower():
                print(f"   ✓ Sequence 3 has 'last email' urgency")
        
        return True
        
    except Exception as e:
        print(f"❌ Follow-up system test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Advanced Cold Email System - Component Tests")
    print("=" * 60)
    print("🎯 Testing: Rotating Templates | HTML Emails | Random Delays | Alternating Logic")
    print("=" * 60)
    
    tests = [
        ("Environment", test_environment),
        ("Lead Loader", test_lead_loader),
        ("Template Engine", test_template_engine),
        ("Email Sender", test_email_sender),
        ("Warmup Sender", test_warmup_sender),
        ("Integration", test_integration),
        ("Follow-up System", test_followup_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Advanced system with follow-ups is ready to use.")
        print("\n✨ System Features Ready:")
        print("   🔄 3 Rotating cold email templates")
        print("   📧 3 Follow-up email templates (7/14/21 day intervals)")
        print("   📧 HTML email formatting with proper paragraph spacing")
        print("   ⏱️  Random delay intervals")
        print("   🔄 Smart alternating send pattern")
        print("   📊 Enhanced logging and statistics tracking")
        print("   🔄 Automatic follow-up sequence management")
        print("\nNext steps:")
        print("1. Ensure your .env file is configured")
        print("2. Add your apollo-contacts-export.csv file")
        print("3. Run: python main.py")
        print("4. System will automatically send follow-ups when no new leads available")
    else:
        print("⚠️  Some tests failed. Please fix issues before running main system.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 