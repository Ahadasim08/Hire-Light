import json
import re
from langchain_ollama import ChatOllama

def resume_analyst_agent(state):
    """
    All-Rounder Analyst: Extracts verbatim facts plus brand prestige and complexity metrics.
    """
    llm = ChatOllama(model="mistral", temperature=0, format="json", num_ctx=8192)
    resume_text = state.get("anonymized_data", "")
    
    prompt = f"""
    SYSTEM: You are a Zero-Tolerance Forensic Data Analyst.
    TASK: Extract technical facts and organizational history with 100% verbatim accuracy.

    EXTRACTION FIELDS:
    1. ORGANIZATIONS: Verbatim list of all companies/universities.
    2. COMPLEXITY: Look for metrics (e.g., 'reduced latency by 40%', '60% workload reduction').
    3. TECH STACK: Verbatim tools.

    CV TEXT: {resume_text}

    OUTPUT JSON ONLY:
    {{
        "organizations": ["verbatim entities"],
        "technical_skills": [{{ "skill": "verbatim", "context": "source sentence" }}],
        "project_audit": [{{ "name": "verbatim title", "impact": "metrics/complexity", "stack": [] }}],
        "education": {{ "degree": "verbatim", "institution": "verbatim" }}
    }}
    """
    try:
        response = llm.invoke(prompt)
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            return {"resume_analysis": json.loads(match.group())}
        return {"error": "Failed to parse resume facts"}
    except Exception as e:
        return {"error": str(e)}