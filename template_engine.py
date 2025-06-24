#!/usr/bin/env python3
"""
Template Engine - Handles email personalization with rotating templates
"""

import random
import re
from typing import Dict, List

class TemplateEngine:
    def __init__(self):
        # Define the 3 rotating templates with proper HTML formatting
        self.templates = [
            {
                "subject": "Quick idea for {{Company Name}} 💡",
                "body": """<p>Hi {{First Name}},</p>

<p>I build custom booking systems, websites, and tools that help small businesses save time and get more clients.</p>

<p>I just finished one for a barber — totally tailored to him — and he's already seeing more bookings through it. I code everything myself — no big agency, no BS.</p>

<p>Would you be open to a quick call sometime this week to see what I could build for {{Company Name}}?</p>

<p>Best regards,<br>
Felix van Dijk<br>
Founder — F van Dijk Ltd<br>
📞 07956 171906<br>
🌐 https://felixvandijk.dev/business.html</p>"""
            },
            {
                "subject": "Helping {{Company Name}} run smoother",
                "body": """<p>Hey {{First Name}},</p>

<p>I'm a freelance developer helping small businesses like yours cut out repetitive tasks with custom software and automation.</p>

<p>Not some big firm — it's just me, and I build everything from scratch based on what you actually need. I've done calendars, booking flows, dashboards, everything.</p>

<p>Would you be open to a 10-minute call to see if there's anything I could simplify for {{Company Name}}?</p>

<p>Best regards,<br>
Felix van Dijk<br>
Founder — F van Dijk Ltd<br>
📞 07956 171906<br>
🌐 https://felixvandijk.dev/business.html</p>"""
            },
            {
                "subject": "Built one tool — got 10+ new clients",
                "body": """<p>Hi {{First Name}},</p>

<p>I recently built a custom tool for a small local business and they picked up 10+ new clients in their first week just from simplifying their booking process.</p>

<p>I do everything myself — websites, automation tools, custom booking platforms — no agencies, no templates, just results.</p>

<p>If I could help {{Company Name}} do something similar, would you be up for a quick chat this week?</p>

<p>Best regards,<br>
Felix van Dijk<br>
Founder — F van Dijk Ltd<br>
📞 07956 171906<br>
🌐 https://felixvandijk.dev/business.html</p>"""
            }
        ]
        
        # Define 3 follow-up templates with different approaches
        self.followup_templates = [
            {
                "subject": "Re: Quick idea for {{Company Name}} (did this get buried?)",
                "body": """<p>Hi {{First Name}},</p>

<p>I sent you a message last week about building custom tools for {{Company Name}}, but I know inboxes can get crazy.</p>

<p>I just helped another business owner automate their client booking process — they went from spending 2 hours a day on scheduling to having it all happen automatically. Now they're focusing on what they do best instead of admin work.</p>

<p>If streamlining any part of {{Company Name}}'s operations sounds useful, I'd love to have a quick 10-minute conversation about what's possible.</p>

<p>Best regards,<br>
Felix van Dijk<br>
Founder — F van Dijk Ltd<br>
📞 07956 171906<br>
🌐 https://felixvandijk.dev/business.html</p>"""
            },
            {
                "subject": "{{Company Name}} — 3 ways I could help",
                "body": """<p>Hi {{First Name}},</p>

<p>I've been thinking about {{Company Name}} and wanted to share 3 specific ways I could help:</p>

<p>1. <strong>Custom booking system</strong> — eliminate back-and-forth emails and missed appointments<br>
2. <strong>Client dashboard</strong> — give customers 24/7 access to their information<br>
3. <strong>Process automation</strong> — turn repetitive tasks into automatic workflows</p>

<p>I recently built a custom portal for a consulting firm that saved them 15 hours per week on client management alone. The owner told me it was the best investment he'd made in years.</p>

<p>Would any of these be valuable for {{Company Name}}? Happy to jump on a brief call to explore what makes sense.</p>

<p>Best regards,<br>
Felix van Dijk<br>
Founder — F van Dijk Ltd<br>
📞 07956 171906<br>
🌐 https://felixvandijk.dev/business.html</p>"""
            },
            {
                "subject": "Last email — {{Company Name}} automation opportunity",
                "body": """<p>Hi {{First Name}},</p>

<p>I don't want to keep bothering you, so this will be my last email about helping {{Company Name}} with custom automation.</p>

<p>I'm only taking on 2 more projects before Christmas, and I had {{Company Name}} in mind for one of them. The businesses I work with typically see results within the first month — better client experience, less admin time, more revenue.</p>

<p>If you're interested in exploring what's possible, just reply and I'll send over some examples of what I've built for similar businesses.</p>

<p>If not, no worries at all — I completely understand you're busy running {{Company Name}}.</p>

<p>Best regards,<br>
Felix van Dijk<br>
Founder — F van Dijk Ltd<br>
📞 07956 171906<br>
🌐 https://felixvandijk.dev/business.html</p>"""
            }
        ]
        
    def get_random_template(self) -> Dict:
        """Get a random template from the available templates"""
        return random.choice(self.templates)
    
    def personalize_subject(self, lead: Dict) -> str:
        """
        Personalize email subject with lead data
        
        Args:
            lead (Dict): Lead information
            
        Returns:
            str: Personalized subject line
        """
        template = self.get_random_template()
        subject = template["subject"]
        
        # Replace placeholders with lead data
        replacements = {
            '{{Company Name}}': lead.get('organization', 'your company'),
            '{{First Name}}': lead.get('first_name', 'there'),
            '{{Last Name}}': lead.get('last_name', ''),
            '{{Title}}': lead.get('title', ''),
            '{{City}}': lead.get('city', ''),
            '{{State}}': lead.get('state', ''),
            '{{Country}}': lead.get('country', ''),
            '{{industry or location}}': self._get_industry_or_location(lead)
        }
        
        for placeholder, value in replacements.items():
            subject = subject.replace(placeholder, str(value))
            
        return subject
    
    def personalize_body(self, lead: Dict, template_index: int = None) -> str:
        """
        Personalize email body with lead data
        
        Args:
            lead (Dict): Lead information
            template_index (int): Specific template index (optional)
            
        Returns:
            str: Personalized email body in HTML format
        """
        if template_index is not None and 0 <= template_index < len(self.templates):
            template = self.templates[template_index]
        else:
            template = self.get_random_template()
            
        body = template["body"]
        
        # Replace placeholders with lead data
        replacements = {
            '{{Company Name}}': lead.get('organization', 'your company'),
            '{{First Name}}': lead.get('first_name', 'there'),
            '{{Last Name}}': lead.get('last_name', ''),
            '{{Title}}': lead.get('title', ''),
            '{{City}}': lead.get('city', ''),
            '{{State}}': lead.get('state', ''),
            '{{Country}}': lead.get('country', ''),
            '{{industry or location}}': self._get_industry_or_location(lead)
        }
        
        for placeholder, value in replacements.items():
            body = body.replace(placeholder, str(value))
            
        return body
    
    def get_template_pair(self, lead: Dict) -> tuple:
        """
        Get a matching subject and body template pair
        
        Args:
            lead (Dict): Lead information
            
        Returns:
            tuple: (subject, body) both personalized from the same template
        """
        template = self.get_random_template()
        
        # Replace placeholders in both subject and body
        replacements = {
            '{{Company Name}}': lead.get('organization', 'your company'),
            '{{First Name}}': lead.get('first_name', 'there'),
            '{{Last Name}}': lead.get('last_name', ''),
            '{{Title}}': lead.get('title', ''),
            '{{City}}': lead.get('city', ''),
            '{{State}}': lead.get('state', ''),
            '{{Country}}': lead.get('country', ''),
            '{{industry or location}}': self._get_industry_or_location(lead)
        }
        
        subject = template["subject"]
        body = template["body"]
        
        for placeholder, value in replacements.items():
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))
            
        return subject, body
    
    def _get_industry_or_location(self, lead: Dict) -> str:
        """
        Get industry or location for the custom merge field
        Prioritizes industry, falls back to location
        
        Args:
            lead (Dict): Lead information
            
        Returns:
            str: Industry or location string
        """
        industry = lead.get('industry', '').strip()
        if industry:
            return industry.lower()
        
        # Build location string
        location_parts = []
        if lead.get('city'):
            location_parts.append(lead.get('city'))
        if lead.get('state'):
            location_parts.append(lead.get('state'))
        if lead.get('country') and lead.get('country').upper() != 'US':
            location_parts.append(lead.get('country'))
            
        if location_parts:
            return ', '.join(location_parts)
        
        return 'your area'
    
    def validate_template(self, template_text: str) -> Dict:
        """
        Validate template for common issues
        
        Args:
            template_text (str): Template to validate
            
        Returns:
            Dict: Validation results
        """
        issues = []
        
        # Check for unmatched placeholders
        placeholders = re.findall(r'\{\{[^}]+\}\}', template_text)
        valid_placeholders = [
            '{{First Name}}', '{{Last Name}}', '{{Company Name}}', 
            '{{Title}}', '{{City}}', '{{State}}', '{{Country}}',
            '{{industry or location}}'
        ]
        
        for placeholder in placeholders:
            if placeholder not in valid_placeholders:
                issues.append(f"Unknown placeholder: {placeholder}")
        
        # Check for basic HTML structure if contains HTML
        if '<p>' in template_text and '</p>' not in template_text:
            issues.append("Unmatched <p> tags")
            
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'placeholder_count': len(placeholders)
        }
    
    def get_template_count(self) -> int:
        """Get number of available templates"""
        return len(self.templates)
    
    def get_followup_template_count(self) -> int:
        """Get number of available follow-up templates"""
        return len(self.followup_templates)
    
    def get_random_followup_template(self) -> Dict:
        """Get a random follow-up template from the available templates"""
        return random.choice(self.followup_templates)
    
    def get_followup_template_pair(self, lead: Dict, followup_sequence: int = 1) -> tuple:
        """
        Get a matching subject and body template pair for follow-up emails
        
        Args:
            lead (Dict): Lead information
            followup_sequence (int): Which follow-up this is (1, 2, or 3)
            
        Returns:
            tuple: (subject, body) both personalized from the same follow-up template
        """
        # Use specific follow-up template based on sequence, or random if out of range
        if 1 <= followup_sequence <= len(self.followup_templates):
            template = self.followup_templates[followup_sequence - 1]
        else:
            template = self.get_random_followup_template()
        
        # Replace placeholders in both subject and body
        replacements = {
            '{{Company Name}}': lead.get('organization', 'your company'),
            '{{First Name}}': lead.get('first_name', 'there'),
            '{{Last Name}}': lead.get('last_name', ''),
            '{{Title}}': lead.get('title', ''),
            '{{City}}': lead.get('city', ''),
            '{{State}}': lead.get('state', ''),
            '{{Country}}': lead.get('country', ''),
            '{{industry or location}}': self._get_industry_or_location(lead)
        }
        
        subject = template["subject"]
        body = template["body"]
        
        for placeholder, value in replacements.items():
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))
            
        return subject, body
    
    def preview_all_templates(self, sample_lead: Dict) -> List[Dict]:
        """
        Generate previews of all templates with sample data
        
        Args:
            sample_lead (Dict): Sample lead data for preview
            
        Returns:
            List[Dict]: List of template previews
        """
        previews = []
        
        # Preview regular templates
        for i, template in enumerate(self.templates):
            subject = template["subject"]
            body = template["body"]
            
            # Replace placeholders
            replacements = {
                '{{Company Name}}': sample_lead.get('organization', 'Sample Company'),
                '{{First Name}}': sample_lead.get('first_name', 'John'),
                '{{Last Name}}': sample_lead.get('last_name', 'Smith'),
                '{{Title}}': sample_lead.get('title', 'CEO'),
                '{{City}}': sample_lead.get('city', 'London'),
                '{{State}}': sample_lead.get('state', 'England'),
                '{{Country}}': sample_lead.get('country', 'United Kingdom'),
                '{{industry or location}}': self._get_industry_or_location(sample_lead)
            }
            
            for placeholder, value in replacements.items():
                subject = subject.replace(placeholder, str(value))
                body = body.replace(placeholder, str(value))
                
            previews.append({
                'template_index': i + 1,
                'template_type': 'cold',
                'subject': subject,
                'body': body
            })
        
        # Preview follow-up templates
        for i, template in enumerate(self.followup_templates):
            subject = template["subject"]
            body = template["body"]
            
            # Replace placeholders
            replacements = {
                '{{Company Name}}': sample_lead.get('organization', 'Sample Company'),
                '{{First Name}}': sample_lead.get('first_name', 'John'),
                '{{Last Name}}': sample_lead.get('last_name', 'Smith'),
                '{{Title}}': sample_lead.get('title', 'CEO'),
                '{{City}}': sample_lead.get('city', 'London'),
                '{{State}}': sample_lead.get('state', 'England'),
                '{{Country}}': sample_lead.get('country', 'United Kingdom'),
                '{{industry or location}}': self._get_industry_or_location(sample_lead)
            }
            
            for placeholder, value in replacements.items():
                subject = subject.replace(placeholder, str(value))
                body = body.replace(placeholder, str(value))
                
            previews.append({
                'template_index': i + 1,
                'template_type': 'followup',
                'subject': subject,
                'body': body
            })
            
        return previews 