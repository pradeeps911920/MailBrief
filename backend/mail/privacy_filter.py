import re

OTP_PATTERNS = [
    r'\b(?:otp|one[- ]?time password)\b',
    r'\b(?:verification code|auth code|security code|login code|sign-in code)\b',
    r'\b\d{4,8}\b.*(?:code|pin|password)',
]

SECURITY_KEYWORDS = [
    "password reset",
    "password changed",
    "security alert",
    "suspicious login",
    "new sign-in",
    "account recovery",
    "unauthorized access",
    "two factor",
    "2fa",
    "authentication"
]

FINANCIAL_KEYWORDS = [
    "bank",
    "transaction",
    "debit",
    "credit",
    "account balance",
    "withdrawal",
    "upi"
]

def is_sensitive(subject: str, sender: str, body: str) -> str | None:
    """
    Determines if an email is sensitive.
    Returns the reason string if sensitive, otherwise None.
    """
    text_to_check = f"{subject} {sender} {body}".lower()
    
    # 1. Check Security Keywords
    for keyword in SECURITY_KEYWORDS:
        if keyword in text_to_check:
            return f"Security keyword detected: {keyword}"
            
    # 2. Check Financial Keywords
    for keyword in FINANCIAL_KEYWORDS:
        if keyword in text_to_check:
            return f"Financial keyword detected: {keyword}"
            
    # 3. Check OTP Regex
    for pattern in OTP_PATTERNS:
        if re.search(pattern, text_to_check):
            return "OTP or verification code pattern detected"
            
    return None

def filter_emails(emails: list) -> tuple:
    """
    Splits emails into normal and sensitive lists.
    Returns: (normal_emails, sensitive_emails_with_reasons)
    """
    normal = []
    sensitive = []
    
    for email in emails:
        reason = is_sensitive(email.get('subject', ''), email.get('sender', ''), email.get('body', ''))
        if reason:
            sensitive.append({
                "email_id": email['id'],
                "reason": reason
            })
        else:
            normal.append(email)
            
    return normal, sensitive
