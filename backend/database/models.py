from sqlalchemy import Column, String, Boolean, DateTime, JSON
from .db import Base
from datetime import datetime

class ProcessedEmail(Base):
    __tablename__ = "processed_emails"
    
    id = Column(String, primary_key=True, index=True) # Gmail Message ID
    thread_id = Column(String, index=True)
    subject = Column(String)
    sender = Column(String)
    date_received = Column(String)
    
    # AI Analysis Results
    analysis_status = Column(String, default="success")
    category = Column(String, index=True)
    importance = Column(String)
    summary = Column(String)
    action_required = Column(Boolean, default=False)
    action = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    entities = Column(JSON)
    why_important = Column(String, nullable=True)
    
    processed_at = Column(DateTime, default=datetime.utcnow)
