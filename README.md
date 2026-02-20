
# AI QA ROI Platform

An AI-assisted platform to estimate QA effort, automation suitability, and Return on Investment (ROI) for automation testing using Large Language Models (LLMs) and deterministic cost models.

This tool enables QA leaders, architects, and managers to make data-driven automation decisions with explainable AI and CFO-friendly metrics.

---

## 🚀 Features

- AI-based QA effort estimation from user stories
- Automated test case generation
- Deterministic automation ROI calculation
- Automation suitability scoring
- What-If ROI cost risk simulation
- Executive KPI dashboard
- Multi-sheet Excel ROI report export
- LangChain @tool based ROI calculator

---

## 🏗️ Project Structure

ai_qa_roi_platform/
├── app.py
├── agents/
│   ├── estimation_agent.py
│   └── test_case_agent.py
├── services/
│   ├── roi_service.py
│   └── excel_service.py
├── tools/
│   └── roi_tool.py
├── utils/
│   └── helpers.py
├── data/
│   ├── qa_estimation_standards.txt
│   └── testing_standard.txt
├── requirements.txt
└── README.md

---

## 🧠 Architecture Principles

- Thin UI layer (Streamlit)
- AI for judgment, not math
- Deterministic and auditable ROI
- Modular enterprise-ready design

---

## ⚙️ Setup

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Configure .env
5. Run Streamlit app

---

## 🔐 Environment Variables

AZURE_ENDPOINT
AZURE_DEPLOYMENT_NAME
OPENAI_ACCESS_TOKEN
API_VERSION

---

## 📊 ROI Formula

ROI (%) = (Manual Cost – Automation Cost) / Automation Cost × 100

---

## 🔮 What-If ROI

Simulates cost uncertainty using automation cost multiplier.

---

## 📁 Excel Output

Includes ROI summary, decision matrix, and test cases.

---

## 👤 Audience

QA Managers, Automation Leads, Architects

---
Output:
<img width="900" height="348" alt="image" src="https://github.com/user-attachments/assets/4f74a3c9-222e-401c-ad37-89beda48961b" />

<img width="665" height="330" alt="image" src="https://github.com/user-attachments/assets/bdda0975-295a-40eb-ab27-bee4a44d7c3b" />

<img width="674" height="344" alt="image" src="https://github.com/user-attachments/assets/930c0293-864e-448d-b2c4-1f9be4106c9f" />

<img width="671" height="367" alt="image" src="https://github.com/user-attachments/assets/1383b441-cf7e-4e8b-9674-8d76fbf2c771" />



