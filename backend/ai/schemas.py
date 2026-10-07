from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class EmailAnalysis(BaseModel):
    category: Literal["Academics", "Placements", "Internships", "Events", "Scholarships", "Administrative", "Lost & Found", "Finance", "General"] = Field(
        description="Must be exactly one of the allowed values."
    )
    importance: Literal["high", "medium", "low"] = Field(
        description="High=deadline soon/required action. Medium=useful info. Low=informational."
    )
    summary: str = Field(description="A 1-2 sentence concise summary.")
    action_required: bool = Field(description="True if the recipient needs to do something.")
    action: Optional[str] = Field(description="Description of the action to take, or null.")
    deadline: Optional[str] = Field(description="ISO 8601 date (YYYY-MM-DD) if a deadline is present. Do not infer if not explicitly stated.")
    entities: List[str] = Field(description="List of key entities (companies, people, etc).")
    why_important: Optional[str] = Field(description="Brief explanation of why this was marked high/medium importance.")
