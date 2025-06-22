# Cold Email Outreach System

A full-featured Python cold email outreach system that reads leads from Apollo-exported CSV files and sends personalized cold emails via SMTP using Zoho. Includes email warm-up, daily limits, logging, and template-based personalization.

## 🚀 Features

- **CSV Lead Import**: Load leads from Apollo CSV exports with data cleaning and validation
- **Daily Limits**: Send maximum 15 cold emails + 5 warm-up emails per day
- **Email Warm-up**: Automatic warm-up emails to improve deliverability
- **Smart Deduplication**: Prevents sending duplicate emails using local logging
- **Template Personalization**: Customize emails with merge fields ({{first_name}}, {{organization}}, etc.)
- **Retry Mechanism**: Automatic retry for failed email sends
- **SSL Security**: Secure SMTP connection with SSL encryption
- **Comprehensive Logging**: Track all sent emails with timestamps and lead data

## 📋 Requirements

- Python 3.6+
- SMTP email account (Zoho, Gmail, Outlook)
- Apollo CSV export file

## 🛠 Installation & Setup

1. **Clone or Download the System**
   ```bash
   # No installation required - uses only Python built-in libraries
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
   SMTP_SERVER=smtp.zoho.com
   SMTP_PORT=465
   ```

   **Important**: Use app-specific passwords, not your main email password!

4. **Prepare Your CSV File**
   - Export your leads from Apollo
   - Save as `apollo-contacts-export.csv` in the project directory
   - Ensure it has these columns: `First Name`, `Last Name`, `Email`, `Organization Name`, `Title`, `City`, `State`, `Country`

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### What Happens When You Run It:
1. **Environment Check**: Validates .env configuration
2. **Daily Limit Check**: Shows today's email progress
3. **Warm-up Emails**: Sends 5 warm-up emails (if quota available)
4. **Cold Emails**: Processes and sends up to 15 cold emails (if quota available)
5. **Logging**: Records all activities in `sent_log.csv`

### Sample Output:
```
🚀 Starting Cold Email Outreach System...
==================================================
📊 Today's Progress:
   Cold emails sent: 0/15
   Warmup emails sent: 0/5

🔥 Sending 5 warmup emails...
🔥 Starting warmup email sequence (5 emails)...
✅ Warmup email 1 sent successfully
...

📧 Processing cold emails (limit: 15)...
📋 Loaded 25 valid leads from CSV
🔍 Filtered out 5 previously contacted leads
📤 Sending 15 cold emails...
✅ Successfully sent to john.smith@example.com
...
```

## 📝 Email Templates

### Default Subject Template:
```
Quick idea for {{organization}}
```

### Default Body Template:
```
Hi {{first_name}},

I came across {{organization}} and noticed the great work you're doing in {{city}}. I'm a software engineer building custom tools that help companies like yours automate client bookings, scheduling, and customer comms. I'd love to offer something tailored to you.

Let me know if I can send over a few ideas?

Kind regards,
Felix
```

### Available Merge Fields:
- `{{first_name}}` - Lead's first name
- `{{last_name}}` - Lead's last name  
- `{{organization}}` - Company name
- `{{title}}` - Job title
- `{{city}}` - City location
- `{{state}}` - State/province
- `{{country}}` - Country

## 📊 File Structure

```
COLD_EMAIL/
├── main.py                    # Main entry point
├── email_sender.py           # SMTP email sending logic
├── lead_loader.py            # CSV processing and deduplication
├── template_engine.py        # Email personalization
├── warmup_sender.py          # Warm-up email functionality
├── .env                      # Your email credentials (create this)
├── env_example.txt           # Environment template
├── apollo-contacts-export.csv # Your leads file
├── sample_apollo_contacts.csv # Example CSV structure
├── sent_log.csv              # Auto-generated email log
└── README.md                 # This file
```

## 🔐 Security & Best Practices

### Email Credentials:
- **Never use your main email password**
- Generate app-specific passwords:
  - **Zoho**: Mail Settings → Security → App Passwords
  - **Gmail**: Account Settings → 2FA → App Passwords
  - **Outlook**: Account Security → Advanced Security Options

### File Security:
- Never commit `.env` to version control
- Keep `sent_log.csv` private (contains lead data)
- Regularly backup your logs

## ⚙️ Configuration Options

### Daily Limits (modify in main.py):
```python
DAILY_COLD_EMAIL_LIMIT = 15    # Adjust as needed
DAILY_WARMUP_EMAIL_LIMIT = 5   # Adjust as needed
```

### SMTP Providers:
- **Zoho**: `smtp.zoho.com:465` (SSL)
- **Gmail**: `smtp.gmail.com:465` (SSL)
- **Outlook**: `smtp-mail.outlook.com:587` (TLS)

## 📈 Monitoring & Logs

### sent_log.csv Columns:
- `timestamp` - When email was sent
- `email` - Recipient email address
- `subject` - Email subject line
- `first_name`, `last_name`, `organization`, `title`, `city`, `state`, `country` - Lead data
- `type` - Email type (cold/warmup)

### Daily Tracking:
The system automatically tracks daily email counts and prevents exceeding limits.

## 🚨 Troubleshooting

### Common Issues:

1. **"SMTP Authentication Failed"**
   - Check your email credentials in `.env`
   - Ensure you're using app-specific password
   - Verify SMTP server settings

2. **"CSV file not found"**
   - Ensure `apollo-contacts-export.csv` exists
   - Check file permissions

3. **"Missing required columns"**
   - Verify CSV has all required columns
   - Check column names match exactly

4. **"Daily limit reached"**
   - System enforces daily limits for deliverability
   - Wait until next day or adjust limits in code

## 🤝 Support

For issues or questions:
1. Check this README first
2. Review error messages carefully
3. Ensure all setup steps completed
4. Verify CSV file format matches requirements

## ⚖️ Legal & Compliance

- Ensure compliance with CAN-SPAM Act, GDPR, etc.
- Only email leads who have consented
- Include unsubscribe mechanisms
- Respect recipient preferences
- Follow your email provider's terms of service

## 🔄 Updates & Maintenance

- Regularly clean your CSV files
- Monitor deliverability rates
- Update warm-up email addresses as needed
- Review and optimize email templates
- Keep sent logs backed up

---

**Happy Emailing! 📧** 