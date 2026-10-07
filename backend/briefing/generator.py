from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from database.db import get_db
from database.models import ProcessedEmail
from mail.fetcher import fetch_recent_emails
from mail.privacy_filter import filter_emails
from mail.grouping import group_emails
from ai.analyzer import analyze_email
from briefing.prioritizer import prioritize_analysis
from config import settings

router = APIRouter(prefix="/briefing", tags=["briefing"])

@router.post("/generate")
def generate_pipeline(max_emails: int = 50, db: Session = Depends(get_db)):
    """
    Executes the ingestion pipeline: Fetch -> Privacy -> Analyze -> Store.
    Does NOT return the full brief, just the stats of the run.
    """
    raw_emails = fetch_recent_emails(max_results=max_emails)
    if not raw_emails:
        return {"message": "No new emails found.", "stats": {}}
        
    existing_ids = {e.id for e in db.query(ProcessedEmail.id).all()}
    new_emails = [e for e in raw_emails if e['id'] not in existing_ids]
    
    if not new_emails:
        return {"message": "No new unprocessed emails.", "stats": {"fetched": len(raw_emails)}}
        
    normal_emails, sensitive_emails = filter_emails(new_emails)
    
    processed_count = 0
    for e in normal_emails:
        analysis = analyze_email(e['subject'], e['sender'], e['body'], e['date'], settings.LLM_API_KEY)
        analysis = prioritize_analysis(analysis)
        
        db_email = ProcessedEmail(
            id=e['id'],
            thread_id=e.get('threadId'),
            subject=e['subject'],
            sender=e['sender'],
            date_received=e['date'],
            analysis_status=analysis.get('analysis_status'),
            category=analysis.get('category'),
            importance=analysis.get('importance'),
            summary=analysis.get('summary'),
            action_required=analysis.get('action_required', False),
            action=analysis.get('action'),
            deadline=analysis.get('deadline'),
            entities=analysis.get('entities', []),
            why_important=analysis.get('why_important')
        )
        db.add(db_email)
        processed_count += 1
        
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database transaction failed")
    
    return {
        "message": "Processing complete.",
        "stats": {
            "emails_received": len(raw_emails),
            "emails_processed": processed_count,
            "sensitive_excluded": len(sensitive_emails)
        }
    }

@router.get("/today")
def get_daily_brief(db: Session = Depends(get_db)):
    """
    Retrieves the brief based on today's stored data.
    """
    import email.utils
    from datetime import datetime, timezone
    
    # Use local time for "today"
    today = datetime.now().date()
    
    all_emails = db.query(ProcessedEmail).all()
    todays_emails = []
    
    for e in all_emails:
        try:
            # Parse RFC 2822 date from Gmail
            parsed_tuple = email.utils.parsedate_tz(e.date_received)
            if parsed_tuple:
                dt = datetime.fromtimestamp(email.utils.mktime_tz(parsed_tuple))
                if dt.date() == today:
                    todays_emails.append(e)
            else:
                # Fallback to processed_at if date parsing fails
                if e.processed_at.date() == today:
                    todays_emails.append(e)
        except Exception:
            pass
    
    if not todays_emails:
        return {"message": "No emails processed today.", "stats": {}, "brief": []}
        
    # Grouping (Assuming group_emails is adapted for DB models or dicts)
    email_dicts = [{
        'id': e.id,
        'threadId': e.thread_id,
        'subject': e.subject,
        'sender': e.sender,
        'date': e.date_received,
        'category': e.category,
        'importance': e.importance,
        'summary': e.summary,
        'action_required': e.action_required,
        'action': e.action,
        'deadline': e.deadline,
        'why_important': e.why_important
    } for e in todays_emails]
    
    grouped = group_emails(email_dicts)
    
    stats = {
        "emails_processed": len(todays_emails),
        "important": sum(1 for e in todays_emails if e.importance == 'high'),
        "actions": sum(1 for e in todays_emails if e.action_required),
        "deadlines": sum(1 for e in todays_emails if e.deadline)
    }
    
    return {
        "stats": stats,
        "brief": grouped
    }
