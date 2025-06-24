# Advanced Cold Email Outreach System with Follow-ups

A comprehensive Python cold email outreach system that reads leads from Apollo-exported CSV files and sends personalized cold emails with intelligent follow-up sequences via SMTP. Features rotating templates, HTML formatting, smart delays, and automatic follow-up management.

## 🚀 Features

### Core Email System
- **CSV Lead Import**: Load leads from Apollo CSV exports with data cleaning and validation
- **Daily Limits**: Send maximum 15 cold emails + 5 warm-up emails per day with automatic reset at midnight
- **Smart Deduplication**: Prevents sending duplicate emails using comprehensive logging
- **Retry Mechanism**: Automatic retry for failed email sends with exponential backoff
- **SSL Security**: Secure SMTP connection with SSL/TLS encryption

### Advanced Template System
- **3 Rotating Cold Email Templates**: Randomized templates to avoid spam detection
- **3 Follow-up Email Templates**: Strategic follow-up sequences with different approaches
- **HTML Email Formatting**: Professional emails with proper paragraph spacing and styling
- **Template Personalization**: Customize emails with merge fields ({{Company Name}}, {{First Name}}, etc.)
- **Professional Signature**: Consistent branding across all emails

### Follow-up Management
- **Automatic Follow-up Sequences**: 3-stage follow-up system (7, 14, 21 days)
- **Time-based Triggering**: Intelligent timing based on last contact date
- **Sequence Tracking**: Comprehensive tracking of follow-up stages per lead
- **Smart Lead Processing**: When no new leads available, automatically sends follow-ups

### Deliverability & Anti-Spam
- **Email Warm-up**: Automatic warm-up emails to improve sender reputation
- **Random Delays**: Anti-spam delays between emails (30-120s cold, 60-180s warmup)
- **Smart Alternating Pattern**: 1 warmup → 3 cold/follow-up → repeat
- **Daily Limit Enforcement**: Respects daily quotas to maintain good sender reputation

### Logging & Analytics
- **Comprehensive Logging**: Track all emails with timestamps, templates used, and follow-up sequences
- **Send Statistics**: Success rates, email counts, and performance metrics
- **Follow-up Tracking**: Monitor which leads are in which follow-up stage

## 📋 Requirements

- Python 3.6+
- SMTP email account (Zoho, Gmail, Outlook)
- Apollo CSV export file

## 🛠 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/FelixvanDijk/COLD_EMAILER.git
   cd COLD_EMAILER
   ```

2. **Setup Environment Variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your email credentials
   nano .env
   ```

3. **Configure Your .env File**
   ```
   EMAIL_ADDRESS=your-email@zoho.com
   EMAIL_PASSWORD=your-app-password
   SMTP_SERVER=smtp.zoho.eu
   SMTP_PORT=465
   ```

   **Important**: Use app-specific passwords, not your main email password!

4. **Prepare Your CSV File**
   - Export your leads from Apollo
   - Save as `apollo-contacts-export.csv` in the project directory
   - Ensure it has these columns: `First Name`, `Last Name`, `Email`, `Company`, `Title`, `City`, `State`, `Country`

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### Test System
```bash
python test_system.py
```

### What Happens When You Run It:

#### Phase 1: Initial Warmup
1. **Environment Check**: Validates .env configuration and SMTP connection
2. **Daily Progress Check**: Shows today's email progress (resets at midnight)
3. **Initial Warmup Batch**: Sends up to 5 warmup emails for sender reputation

#### Phase 2: Smart Alternating Pattern
4. **New Leads Processing**: Sends cold emails to uncontacted leads (rotating templates)
5. **Follow-up Processing**: When no new leads, automatically processes follow-up sequences
6. **Smart Delays**: Random delays between emails to avoid spam detection

### Sample Output:
```
🚀 Starting Advanced Cold Email Outreach System...
============================================================
📋 Features: Rotating Templates | Random Delays | Smart Alternating
============================================================

📊 Today's Progress:
   Cold emails sent: 3/15
   Warmup emails sent: 2/5

🎯 Template Engine loaded with 3 rotating templates
🔄 Follow-up Engine loaded with 3 follow-up templates

🔗 Testing SMTP connection...
✅ SMTP connection test successful (SSL)

📋 Loading leads for 12 cold emails...
✅ No new leads to process. Checking for follow-up opportunities...
🔄 Found 8 leads ready for follow-up

🔥 PHASE 1: Initial warmup batch (3 emails)
📧 Warmup email 1/3 to test@gmail.com...
✅ Warmup email sent successfully
⏱️  Adding random delay: 127 seconds...

📧 PHASE 2: Alternating send pattern
   Pattern: 1 warmup → 3 follow-up → 1 warmup → 3 follow-up...

🔄 Alternating: Sending 1 warmup email...
📤 Follow-up 2 to John at TechCorp Ltd (16 days since last contact)...
✅ Successfully sent follow-up 2 to john@techcorp.com
```

## 📧 Email Templates

### Cold Email Templates (3 rotating)

#### Template 1: Quick Idea
**Subject:** `Quick idea for {{Company Name}} 💡`
- Focus: Custom booking systems and automation
- Tone: Direct and practical

#### Template 2: Running Smoother  
**Subject:** `Helping {{Company Name}} run smoother`
- Focus: Process automation and efficiency
- Tone: Helpful and collaborative

#### Template 3: Social Proof
**Subject:** `Built one tool — got 10+ new clients`
- Focus: Results and social proof
- Tone: Achievement-focused

### Follow-up Templates (3 sequential)

#### Follow-up 1 (7 days later)
**Subject:** `Re: Quick idea for {{Company Name}} (did this get buried?)`
- Approach: Acknowledges busy inboxes, provides social proof
- Tone: Understanding and helpful

#### Follow-up 2 (14 days later)
**Subject:** `{{Company Name}} — 3 ways I could help`
- Approach: Specific value propositions with concrete examples
- Tone: Structured and detailed

#### Follow-up 3 (21 days later)
**Subject:** `Last email — {{Company Name}} automation opportunity`
- Approach: Creates urgency with limited availability
- Tone: Respectful final attempt with easy opt-out

### Professional Signature (All Templates)
```
Best regards,
Felix van Dijk
Founder — F van Dijk Ltd
📞 07956 171906
🌐 https://felixvandijk.dev/business.html
```

### Available Merge Fields:
- `{{Company Name}}` - Company name (from Company column)
- `{{First Name}}` - Lead's first name
- `{{Last Name}}` - Lead's last name  
- `{{Title}}` - Job title
- `{{City}}` - City location
- `{{State}}` - State/province
- `{{Country}}` - Country

## 🔄 Follow-up System

### How Follow-ups Work

1. **Initial Contact**: System sends cold email using rotating templates
2. **7-Day Follow-up**: First follow-up with "buried inbox" approach
3. **14-Day Follow-up**: Second follow-up with specific value propositions
4. **21-Day Follow-up**: Final follow-up with urgency and respect for their time
5. **Complete**: Lead marked as fully processed (no more follow-ups)

### Follow-up Logic
- **Time-based**: Only sends when enough time has passed since last contact
- **Sequence-aware**: Tracks which follow-up stage each lead is on
- **Automatic processing**: When no new leads available, processes follow-ups
- **Respectful limits**: Maximum 3 follow-ups per lead (+ initial contact)

### Follow-up Intervals (Configurable)
```python
followup_intervals = {
    1: 7,   # First follow-up after 7 days
    2: 14,  # Second follow-up after 14 days  
    3: 21   # Third follow-up after 21 days
}
```

## 📊 File Structure

```
COLD_EMAILER/
├── main.py                    # Main entry point with advanced logic
├── email_sender.py           # SMTP sending with HTML support
├── lead_loader.py            # CSV processing, deduplication & follow-up tracking
├── template_engine.py        # Template rotation & follow-up management
├── warmup_sender.py          # Warm-up email functionality
├── test_system.py            # Comprehensive system testing
├── test_env.py               # Environment validation
├── setup.py                  # System setup and configuration
├── .env                      # Your email credentials (create this)
├── env_example.txt           # Environment template
├── apollo-contacts-export.csv # Your leads file
├── sent_log.csv              # Auto-generated email log with follow-up tracking
├── .gitignore                # Protects sensitive files
└── README.md                 # This documentation
```

## 📊 Enhanced Logging

### sent_log.csv Columns:
- `timestamp` - When email was sent (ISO format)
- `email` - Recipient email address
- `subject` - Email subject line used
- `status` - Send status (sent/failed)
- `type` - Email type (cold/warmup/followup)
- `first_name`, `last_name`, `organization` - Lead data
- `template_used` - Which template was used (Template 1, Follow-up 2, etc.)
- `followup_sequence` - Follow-up stage number (1, 2, 3)

### Daily Tracking:
- Automatic daily reset at midnight (00:00)
- Tracks both cold emails and follow-ups against daily limits
- Follow-ups count toward cold email quota

## ⚙️ Configuration Options

### Daily Limits (modify in main.py):
```python
DAILY_COLD_EMAIL_LIMIT = 15    # Includes follow-ups
DAILY_WARMUP_EMAIL_LIMIT = 5   # Warm-up emails only
```

### Follow-up Timing (modify in lead_loader.py):
```python
followup_intervals = {
    1: 7,   # Days until first follow-up
    2: 14,  # Days until second follow-up  
    3: 21   # Days until third follow-up
}
max_followups = 3  # Maximum follow-up attempts
```

### SMTP Providers:
- **Zoho Europe**: `smtp.zoho.eu:465` (SSL) - Recommended
- **Zoho Global**: `smtp.zoho.com:465` (SSL)
- **Gmail**: `smtp.gmail.com:465` (SSL)
- **Outlook**: `smtp-mail.outlook.com:587` (TLS)

## 🔐 Security & Best Practices

### Email Credentials:
- **Never use your main email password**
- Generate app-specific passwords:
  - **Zoho**: Mail Settings → Security → App Passwords
  - **Gmail**: Account Settings → 2FA → App Passwords
  - **Outlook**: Account Security → Advanced Security Options

### File Security:
- `.env` file automatically excluded from git
- `sent_log.csv` and CSV files protected from repository
- Enhanced .gitignore prevents accidental credential exposure

### Deliverability Best Practices:
- Respect daily limits (15 cold + 5 warmup recommended)
- Use warm-up emails to build sender reputation
- Random delays prevent spam detection
- Professional HTML formatting improves engagement

## 🧪 Testing

### Run All Tests:
```bash
python test_system.py
```

### Test Components:
- Environment configuration validation
- Lead loading and CSV processing
- Template engine (cold + follow-up templates)
- Email sender with HTML support
- Warmup sender functionality
- Follow-up system logic
- Integration testing

### Expected Output:
```
🎉 All tests passed! Advanced system with follow-ups is ready to use.

✨ System Features Ready:
   🔄 3 Rotating cold email templates
   📧 3 Follow-up email templates (7/14/21 day intervals)
   📧 HTML email formatting with proper paragraph spacing
   ⏱️  Random delay intervals
   🔄 Smart alternating send pattern
   📊 Enhanced logging and statistics tracking
   🔄 Automatic follow-up sequence management
```

## 🚨 Troubleshooting

### Common Issues:

1. **"SMTP Authentication Failed"**
   - Check your email credentials in `.env`
   - Ensure you're using app-specific password
   - Try `smtp.zoho.eu` instead of `smtp.zoho.com`

2. **"Missing required columns in CSV"**
   - New Apollo format uses `Company` instead of `Organization Name`
   - Verify CSV has: `First Name`, `Last Name`, `Email`, `Company`, `Title`, `City`, `State`, `Country`

3. **"No leads ready for follow-up"**
   - Normal behavior if all leads are recently contacted
   - Follow-ups respect timing intervals (7/14/21 days)
   - Check `sent_log.csv` for last contact dates

4. **"Daily limit reached"**
   - Limits reset automatically at midnight
   - Follow-ups count toward cold email quota
   - Adjust limits in `main.py` if needed

5. **Follow-up Timing Issues**
   - System uses local system time
   - Ensure system clock is accurate
   - Check timestamp format in `sent_log.csv`

## 📈 Performance & Analytics

### System Statistics:
- Total emails sent vs. failed
- Success rate percentage
- Cold emails vs. warmup breakdown
- Follow-up sequence completion rates

### Monitoring Recommendations:
- Daily review of `sent_log.csv`
- Monitor SMTP connection success
- Track follow-up response rates
- Adjust templates based on performance

## 🤝 Support & Contributing

### For Issues or Questions:
1. Check this README documentation
2. Run `python test_system.py` to validate setup
3. Review error messages and logs carefully
4. Ensure all setup steps completed

### Repository:
- **GitHub**: https://github.com/FelixvanDijk/COLD_EMAILER
- **Issues**: Use GitHub Issues for bug reports
- **Contributions**: Pull requests welcome

---

**Ready for production use with comprehensive follow-up capabilities!** 🚀 