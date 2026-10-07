def prioritize_analysis(analysis: dict) -> dict:
    """
    Rule-based prioritizer to adjust importance after AI analysis.
    Safety net over LLM outputs.
    """
    if analysis.get("analysis_status") == "fallback":
        analysis["importance"] = "low"
        return analysis
        
    importance = analysis.get("importance", "low").lower()
    
    # 1. Action required or deadline -> always at least medium, usually high
    if analysis.get("action_required") or analysis.get("deadline"):
        if importance == "low":
            importance = "medium"
            
    # 2. Placement/Internship -> usually high priority for students
    category = analysis.get("category", "")
    if category in ["Placements", "Internships"] and importance == "low":
        importance = "medium"
        
    analysis["importance"] = importance
    return analysis
