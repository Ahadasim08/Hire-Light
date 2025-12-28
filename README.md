<div align="center">
  <h1>Hire-Light ⛓️🔍</h1>
  <p><b>The Forensic AI Resume Auditor: Verifying Proof, Not Keywords.</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js">
    <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  </p>
</div>

---

## 🚀 The Vision
Standard recruitment is often broken. Candidates can "game" the system with keyword stuffing, and manual screening is slow and prone to human bias. 

**Hire-Light** is a forensic decision engine that replaces shallow keyword filtering with deep evidence auditing. Using a **5-layer multi-agent chain**, it identifies "Verified Expertise" vs. "Theoretical Claims" to find the true best-fit candidate for any role.

---

## 🏗️ How the Multi-Agent Chain Works
The system orchestrates five specialized AI agents that work in a sequential pipeline to ensure high-precision results:



| Agent | Responsibility |
| :--- | :--- |
| **1. Job Analyst** | Benchmarks the Job Description to define exactly what technical depth is required. |
| **2. Anonymizer** | Automatically strips PII (Names, Emails, Locations) to ensure a 100% bias-free audit. |
| **3. Resume Analyst** | Extracts technical evidence, tools, and specific project outcomes verbatim. |
| **4. Evidence Auditor** | Cross-references extracted facts against industry standards to verify complexity. |
| **5. Hiring Critic** | Generates the final **Suitability Score (0-100)** based on verified proof. |

---

## ✨ Key Features
* **Forensic Verification:** Moves beyond simple word-matching to audit actual project impact.
* **Bias Elimination:** Automated anonymization ensures candidates are judged solely on merit.
* **Data Privacy:** Designed to run with local models (via **Ollama**) so candidate data never leaves your infrastructure.
* **Scalable Architecture:** A modular agentic workflow built for speed and accuracy.

---

## 🛠️ Tech Stack
* **AI Engine:** LangChain & Multi-Agent Orchestration.
* **LLM Support:** Local Models (Mistral, Llama 3).
* **Backend:** Python & FastAPI.
* **Frontend:** Next.js, React, & Tailwind CSS.

---

## ⚙️ Setup & Installation

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
