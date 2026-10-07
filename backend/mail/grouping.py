import re
from collections import defaultdict

def normalize_subject(subject: str) -> str:
    """
    Strips Re:, Fwd:, and other prefixes to group emails by base subject.
    """
    # Remove common prefixes
    subject = re.sub(r'^(re|fwd|fw|reply|forward):\s*', '', subject, flags=re.IGNORECASE)
    # Remove extra spaces
    return subject.strip().lower()

def group_emails(emails: list) -> list:
    """
    Groups emails by normalized subject and thread ID.
    Returns a list of grouped email threads.
    """
    groups = defaultdict(list)
    
    for email in emails:
        # Group by threadId if present, else normalized subject
        thread_id = email.get('threadId')
        subject = email.get('subject', '')
        
        if thread_id:
            groups[thread_id].append(email)
        else:
            norm_subj = normalize_subject(subject)
            groups[norm_subj].append(email)
            
    # Format the output
    grouped_list = []
    for key, group in groups.items():
        if len(group) == 1:
            grouped_list.append(group[0])
        else:
            import email.utils
            
            def get_timestamp(e):
                try:
                    pt = email.utils.parsedate_tz(e.get('date', ''))
                    return email.utils.mktime_tz(pt) if pt else 0
                except:
                    return 0
                    
            group.sort(key=get_timestamp)
            
            # Create a combined representation
            base_subject = group[0].get('subject')
            grouped_list.append({
                'is_group': True,
                'group_key': key,
                'subject': base_subject,
                'email_count': len(group),
                'emails': group,
                # Use the latest email's properties for top-level display
                'sender': group[-1].get('sender'),
                'date': group[-1].get('date'),
                'category': group[-1].get('category'),
                'importance': group[-1].get('importance'),
                'summary': f"[{len(group)} related emails] " + group[-1].get('summary', ''),
                'action_required': any(e.get('action_required') for e in group),
                'action': next((e.get('action') for e in group if e.get('action')), None),
                'deadline': next((e.get('deadline') for e in group if e.get('deadline')), None),
                'why_important': group[-1].get('why_important')
            })
            
    return grouped_list
