import json
from langchain_ollama import ChatOllama # Use the local Ollama integration

def anonymizer_agent(state):
    """
    Anonymizer: Strips PII (Name, Email, Phone, Address) locally using Mistral.
    Ensures bias-free auditing by focusing only on technical evidence.
    """
    # 1. Initialize local Mistral model
    llm = ChatOllama(
        model="mistral", 
        temperature=0, # Maximum determinism for consistency
        format="json" 
    )
    
    raw_text = state.get("resume_text", "")
    
    # Prompt focuses on redaction while keeping technical keywords safe
    prompt = f"""
    SYSTEM: You are a Privacy Specialist. 
    TASK: Redact all PII (Name, Email, Phone, Address) from the provided resume text.
    
    STRICT RULES:
    1. KEEP all technical skills, project titles, and tools (e.g., Python, FastAPI, Node.js).
    2. REPLACE PII with generic placeholders (e.g., [NAME], [EMAIL]).
    3. NO SUMMARY: Do not add any conversational text.
    
    INPUT TEXT: {raw_text}
    
    OUTPUT JSON ONLY:
    {{
        "anonymized_data": "string containing the redacted text",
        "redaction_log": ["list of what was redacted"]
    }}
    """
    
    try:
        # 2. Execute local inference
        response = llm.invoke(prompt)
        
        # Clean and parse JSON
        content = response.content.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(content)
        
        return {
            "anonymized_data": parsed.get("anonymized_data", ""),
            "redaction_log": parsed.get("redaction_log", [])
        }
            
    except Exception as e:
        print(f"❌ Local Anonymizer Error: {str(e)}")
        # Fallback to returning the raw text if the LLM fails
        return {"anonymized_data": raw_text, "redaction_log": ["ERROR: FAILED_TO_ANONYMIZE"]}