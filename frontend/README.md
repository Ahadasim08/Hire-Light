<div align="center">
  <img src="assets/logo.png" alt="Hire-Light Logo" width="120" style="margin-bottom: 10px;">

  <h1>Hire-Light ⛓️🔍</h1>
  <p><b>The Forensic AI Resume Auditor: Stop matching keywords, start auditing evidence.</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js">
    <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
    <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  </p>
  
  <p>
    <a href="#-key-features">Features</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-setup">Setup</a> •
    <a href="#-tech-stack">Tech Stack</a>
  </p>
</div>

---

## 🚀 The Vision
Standard recruitment is broken. Candidates game the system with keyword stuffing, and recruiters struggle with manual bias. **Hire-Light** is a forensic decision engine that uses a **5-layer multi-agent chain** to verify technical evidence verbatim from project histories. It identifies "Verified" vs. "Theoretical" skills to find the true best-fit candidate.



## 🏗️ Architecture
The system orchestrates five specialized AI agents to ensure a high-precision, bias-free audit:



1.  **Job Analyst:** Benchmarks the JD against industry standards.
2.  **Anonymizer:** Strips PII for 100% objective, bias-free screening.
3.  **Resume Analyst:** Extracts technical evidence, tools, and complexity metrics verbatim.
4.  **Evidence Auditor:** Cross-references claimed skills against actual project outcomes.
5.  **Hiring Critic:** Generates a final **Suitability Score (0-100)** and growth feedback.

---

## ✨ Key Features
* **Forensic Verification:** Replaces shallow keyword matching with verbatim evidence auditing.
* **Multi-Agent Orchestration:** Powered by LangChain for seamless agent-to-agent communication.
* **Privacy-First:** Designed for local LLM deployment (**Ollama**) to keep candidate data on-premise.
* **Bias Elimination:** Automated PII stripping ensures merit-based hiring.

---

## 🛠️ Tech Stack

<details>
<summary><b>Click to expand Technical Details</b></summary>

* **Backend:** Python 3.10+, FastAPI, Pydantic, PyPDF.
* **AI Engine:** LangChain, Mistral / Gemini (via Ollama).
* **Frontend:** Next.js 14, React, Tailwind CSS, TypeScript.
* **DevOps:** Local LLM hosting, Environment-based configuration.
</details>

---

## ⚙️ Setup & Installation

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python main.py