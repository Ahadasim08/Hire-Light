import json
import re
from langchain_ollama import ChatOllama

def job_analyst_agent(state):
    """
    Strategic Talent Architect: Translates user intent and brand prestige 
    into technical evidence requirements.
    """
    llm = ChatOllama(model="mistral", temperature=0, format="json")
    job_desc = state.get("job_description", "")
    
    prompt = f"""
    SYSTEM: You are a Strategic Talent Architect.
    TASK: Translate the user's job description or intent into a Forensic Audit Profile.

    INTENT MAPPING:
    1. If 'Google' or 'Top-tier' is mentioned, prioritize 'Distributed Systems' and 'Scalability'.
    2. Identify 'Deal-Breakers' (Degrees, Certs).
    3. Extract verbatim technical skills.

    JOB DESCRIPTION: {job_desc}
    
    OUTPUT JSON ONLY:
    {{
        "industry": "string",
        "deal_breakers": ["string"],
        "required_skills": ["string"],
        "prestige_markers": ["implied requirements like Scalability or Enterprise architecture"]
    }}
    """
    try:
        response = llm.invoke(prompt)
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            return {"job_analysis": json.loads(match.group())}
        return {"error": "Failed to parse job analysis"}
    except Exception as e:
        return {"error": str(e)}