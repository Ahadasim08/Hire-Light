import json
from langchain_ollama import ChatOllama

def evidence_auditor_agent(state):
    """
    Evidence Auditor: Cross-references claimed skills against project history.
    Detects if a skill is 'Verified' (used in a project) or 'Unverified' (just listed).
    """
    llm = ChatOllama(
        model="mistral", 
        temperature=0, # Forces deterministic cross-referencing
        format="json"
    )
    
    # We take the structured facts from the Resume Analyst
    analysis = state.get("resume_analysis") or {}
    
    prompt = f"""
    SYSTEM: You are a Forensic Evidence Auditor.
    TASK: Verify the legitimacy of the candidate's technical claims using ONLY the provided data.

    STRATEGY:
    1. CROSS-REFERENCE: For every 'technical_skill', search the 'project_audit' for proof of usage.
    2. STATUS ASSIGNMENT:
       - 'VERIFIED': Skill is used in a specific project with a verbatim result.
       - 'UNVERIFIED': Skill is listed in 'technical_skills' but has no project evidence.
    3. DETECT EXAGGERATION: Flag if a skill (e.g., Surgery) is claimed but the projects are in a different domain (e.g., CS).

    INPUT DATA:
    {json.dumps(analysis)}

    OUTPUT JSON ONLY:
    {{
        "verified_skills": [
            {{ "skill": "string", "proof_project": "exact project name from CV" }}
        ],
        "unverified_claims": [
            {{ "skill": "string", "warning": "No verbatim project evidence found" }}
        ],
        "legitimacy_score": integer (0-100)
    }}
    """

    try:
        response = llm.invoke(prompt)
        content = response.content.strip().replace("```json", "").replace("```", "")
        return {"evidence_audit": json.loads(content)}
    except Exception as e:
        print(f"❌ Evidence Audit Error: {str(e)}")
        return {"error": f"Proof verification failed: {str(e)}"}