import json

from google import genai

from .schemas import EmailAnalysis


def analyze_email(
    subject: str,
    sender: str,
    body: str,
    date: str,
    api_key: str
) -> dict:
    """
    Analyze an email using Gemini 3.8 Flash and return
    validated data matching the EmailAnalysis schema.
    """

    fallback_response = {
        "analysis_status": "fallback",
        "category": "General",
        "importance": "low",
        "summary": "AI analysis unavailable.",
        "action_required": False,
        "action": None,
        "deadline": None,
        "entities": [],
        "why_important": None,
    }

    # Make sure an API key is available.
    if not api_key:
        print("GEMINI ERROR: API key is missing.")
        return fallback_response

    try:
        # Create Gemini client.
        client = genai.Client(api_key=api_key)

        # Prompt for email analysis.
        prompt = f"""
Analyze this email and extract the requested information.

Rules:
- If the email does not clearly specify a deadline, return null.
- Never infer or guess a deadline.
- Determine the importance based only on the email content.
- Identify whether the recipient needs to take an action.
- Keep the summary concise and useful.
- Return only information supported by the email.

Email received date context:
{date}

Sender:
{sender}

Subject:
{subject}

Body:
{body}
"""

        # Generate structured JSON using Gemini 3.8 Flash.
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
            generation_config={
                "thinking_level": "low"
            },
            response_format=[
                {
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": EmailAnalysis.model_json_schema(),
                }
            ],
            timeout=30,
        )

        # Get Gemini's output.
        output_text = interaction.output_text

        if not output_text:
            raise ValueError("Gemini returned an empty response.")

        # Parse JSON.
        parsed_data = json.loads(output_text)

        # Validate response using Pydantic.
        validated_data = EmailAnalysis(**parsed_data).model_dump()

        # Mark successful analysis.
        validated_data["analysis_status"] = "success"

        print("GEMINI ANALYSIS SUCCESSFUL")

        return validated_data

    except Exception as e:
        print("GEMINI ANALYSIS ERROR:", repr(e))
        return fallback_response