import json
import re
from langchain_ollama import ChatOllama

def hiring_critic_agent(state):
    """
    Expert Recruiter: Provides balanced, professional feedback and prestige alignment.
    """
    llm = ChatOllama(model="mistral", temperature=0.2, format="json")
    
    prompt = f"""
    SYSTEM: You are a Senior Talent Consultant. Provide a balanced evaluation of candidate fit.
    TASK: Highlight 3 strengths, 3 growth areas, and assess 'Brand Alignment' (prestige).

    DATA:
    Requirements: {json.dumps(state.get('job_analysis'))}
    Candidate: {json.dumps(state.get('resume_analysis'))}
    Proof: {json.dumps(state.get('evidence_audit'))}

    OUTPUT JSON ONLY:
    {{
        "suitability_score": int,
        "executive_summary": "string",
        "top_strengths": ["string"],
        "growth_areas": ["string"],
        "improvement_tips": ["precise career advice"],
        "brand_alignment": "Assessment of prestige match"
    }}
    """
    try:
        response = llm.invoke(prompt)
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            return {"critic_result": json.loads(match.group())}
        return {"error": "Failed to parse evaluation"}
    except Exception as e:
        return {"error": str(e)}