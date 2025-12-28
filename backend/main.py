import os
import uuid
import asyncio 
import io 
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader 

# --- ADD THIS LINE ---
from langchain_ollama import ChatOllama 
# ---------------------

# Your existing agent imports
from agents.job_analyst import job_analyst_agent
from agents.anonymizer_agent import anonymizer_agent
from agents.resume_analyst import resume_analyst_agent 
from agents.evidence_auditor_agent import evidence_auditor_agent
from agents.matcher_agent import hiring_critic_agent

# Load environment variables
load_dotenv()

# Step 1: Secure Imports of your Forensic Agents
from agents.job_analyst import job_analyst_agent
from agents.anonymizer_agent import anonymizer_agent
from agents.resume_analyst import resume_analyst_agent 
from agents.evidence_auditor_agent import evidence_auditor_agent
from agents.matcher_agent import hiring_critic_agent

app = FastAPI(title="Hire-Light Decision Engine API")

# Broad origins for local development and testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# Shared state for tracking batch progress
BATCH_STATUS = {}

import os
import uuid
import asyncio 
import io 
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader 
from langchain_ollama import ChatOllama # Fix: Required for pipeline scope

# Load and Import Agents
from agents.job_analyst import job_analyst_agent
from agents.anonymizer_agent import anonymizer_agent
from agents.resume_analyst import resume_analyst_agent 
from agents.evidence_auditor_agent import evidence_auditor_agent
from agents.hiring_critic import hiring_critic_agent # Unified import

app = FastAPI(title="Hire-Light All-Rounder API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BATCH_STATUS = {}

async def run_forensic_pipeline(batch_id: str, files: List[UploadFile], job_description: str):
    BATCH_STATUS[batch_id]["status"] = "processing"
    try:
        job_res = job_analyst_agent({"job_description": job_description})
        job_profile = job_res.get("job_analysis", {})

        for file in files:
            # Extraction & Anonymization
            pdf_bytes = await file.read()
            reader = PdfReader(io.BytesIO(pdf_bytes))
            resume_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
            
            clean_res = anonymizer_agent({"resume_text": resume_text})
            audit_res = resume_analyst_agent({"anonymized_data": clean_res.get("anonymized_data")})
            resume_analysis = audit_res.get("resume_analysis", {})

            # Verification
            verification_res = evidence_auditor_agent({"resume_analysis": resume_analysis})
            evidence_audit = verification_res.get("evidence_audit", {})

            # Evaluation
            critic_res = hiring_critic_agent({
                "job_analysis": job_profile,
                "resume_analysis": resume_analysis,
                "evidence_audit": evidence_audit
            })
            evaluation = critic_res.get("critic_result", {})
            
            # Final Balanced Package
            BATCH_STATUS[batch_id]["results"].append({
                "filename": file.filename,
                "score": evaluation.get("suitability_score", 0),
                "summary": evaluation.get("executive_summary"),
                "organizations": resume_analysis.get("organizations", []),
                "strengths": evaluation.get("top_strengths", []),
                "improvement_tips": evaluation.get("improvement_tips", []),
                "brand_alignment": evaluation.get("brand_alignment"),
                "verified_skills": evidence_audit.get("verified_skills", [])
            })

        BATCH_STATUS[batch_id]["status"] = "completed"
    except Exception as e:
        BATCH_STATUS[batch_id]["status"] = "failed"
        print(f"PIPELINE CRASH: {str(e)}")

@app.post("/upload-batch")
async def upload_batch(
    background_tasks: BackgroundTasks, 
    job_description: str = Form(...), 
    files: List[UploadFile] = File(...)
):
    """
    Endpoint to trigger the forensic audit batch.
    """
    batch_id = str(uuid.uuid4())
    BATCH_STATUS[batch_id] = {
        "id": batch_id, 
        "status": "queued", 
        "progress": 0,
        "total_files": len(files), 
        "current_file": None, 
        "results": []
    }
    background_tasks.add_task(run_forensic_pipeline, batch_id, files, job_description)
    return {"batch_id": batch_id}

@app.get("/status/{batch_id}")
def get_status(batch_id: str):
    """
    Frontend polling endpoint to track progress.
    """
    if batch_id not in BATCH_STATUS:
        raise HTTPException(status_code=404, detail="Batch ID not found")
    return BATCH_STATUS[batch_id]