# 🧠 DocuMind: Intelligent Document Organization Assistant Using AI Agents

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gradio](https://img.shields.io/badge/GUI-Gradio%20v4-orange)
![Langflow](https://img.shields.io/badge/AI%20Agent-Langflow-purple)
![JWT](https://img.shields.io/badge/Security-JWT%20Auth-green)
![Evaluation](https://img.shields.io/badge/Evaluation-B.Tech%20CSE%20CA3%20(30%20Marks)-red)

**DocuMind** is an AI-agent-powered document organization system designed for the B.Tech CSE CA3 Mini-Project evaluation. It automatically ingests unstructured documents (`.pdf`, `.docx`, `.txt`), extracts content, passes text through a **Langflow LLM Agent workflow**, generates structured metadata (category, sub-category, summary, tags, suggested folder, confidence score, reasoning rationale), and presents recommendations in a modern **Gradio web GUI** with **JWT-based session authentication**.

---

## 📌 Project Overview & CA3 Evaluation Summary

| Evaluation Domain | Marks | Feature / Component |
| :--- | :---: | :--- |
| **Submission** | **5** | GitHub-ready repository with complete modular codebase. |
| **GitHub Link** | **5** | Structured repository with `.gitignore`, `README.md`, and clean commits. |
| **Model / Implementation** | **10** | PyMuPDF text extraction + Langflow AI Agent workflow + Intelligent Fallback engine. |
| **Project Report** | **5** | Full 9-chapter IEEE/College template report in [`docs/report.md`](docs/report.md). |
| **Viva Voce** | **5** | 20 detailed Q&As in [`docs/viva_questions.md`](docs/viva_questions.md). |

---

## 🎯 Objectives & Key Features

- 📄 **Multi-Format Extraction**: Parses text and page metadata from PDF, DOCX, and TXT files.
- 🤖 **AI Agent Reasoning Loop**: Perceives text, reasons over context, decides taxonomy, explains classification rationale, and generates recommended actions.
- 🔒 **JWT Authentication**: Secured session management leveraging Langflow built-in auth (`POST /api/v1/login`) and signed JWT claims.
- 📁 **Visual Folder Tree Preview**: Instant ASCII directory tree preview representing proposed file organization.
- ⚡ **100% Demonstration Reliability**: Includes an Intelligent Fallback Engine for offline testing during viva.

---

## 🏗️ System Architecture

```text
[ User Browser ]
       │
       ▼
[ Gradio GUI (app.py) ] ── (JWT Token Auth) ──► [ AuthService (services/auth.py) ]
       │
       ├─► [ DocumentProcessor (services/document_processor.py) ] (Extracts PDF/DOCX/TXT)
       │
       └─► [ LangflowClient (services/langflow_client.py) ]
                 │
                 ├──► (Live Mode) ──► [ Langflow REST API Endpoint / LLM Flow ]
                 │
                 └──► (Offline Mode) ──► [ DocuMind Intelligent Fallback Engine ]
```

---

## 🛠️ Technology Stack

- **GUI / Frontend**: Gradio Blocks (`gradio >= 4.0`)
- **Backend / Language**: Python 3.10+
- **AI Agent Workflow**: Langflow (`documind_flow.json`)
- **Document Processing**: PyMuPDF (`fitz`), `python-docx`, native UTF-8 file I/O
- **Authentication & Security**: PyJWT, `python-dotenv`, HTTP Bearer / `x-api-key`

---

## 🚀 Quickstart & Setup Commands

### 1. Clone & Navigate to Project Directory
```bash
cd DocuMind
```

### 2. Create Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Ensure your `.env` contains:
```env
LANGFLOW_URL=http://localhost:7860
LANGFLOW_FLOW_ID=documind-agent-flow-v1
LANGFLOW_API_KEY=lf_key_documind_demo_12345
LANGFLOW_SUPERUSER=admin
LANGFLOW_SUPERUSER_PASSWORD=adminpassword123
LANGFLOW_SECRET_KEY=documind-super-secret-jwt-key-2026
LANGFLOW_ALGORITHM=HS256
DEMO_MODE=true
```

### 4. Launch the Application
```bash
python app.py
```
Open your browser at `http://127.0.0.1:7860`.

---

## 🔑 Login & Session Guidance

1. Click on the **🔐 Authentication & Session** tab.
2. Enter default login credentials:
   - **Username**: `admin`
   - **Password**: `adminpassword123`
3. Click **🔓 Log In**. You will receive an active JWT session token allowing access to the Document Analysis tab.

---

## 🤖 AI Agent Execution Loop

```text
1. PERCEIVE  ──► Reads text from PDF / DOCX / TXT using fitz / docx.
2. REASON    ──► Analyzes contextual domain keywords using Langflow prompt.
3. DECIDE    ──► Determines category, subcategory, tags, and suggested folder.
4. EXPLAIN   ──► Generates explicit decision reasoning and confidence score (0-100%).
5. RECOMMEND ──► Constructs visual folder tree preview.
6. APPROVE   ──► Human user clicks [Accept Recommendation] or [Reject].
```

---

## 📊 Sample Output Schema

```json
{
  "category": "Education",
  "subcategory": "Database Management Systems",
  "summary": "This document contains academic study material covering relational database concepts, SQL queries, normalization rules, and ACID transaction properties.",
  "tags": ["DBMS", "SQL", "Database", "CollegeNotes"],
  "suggested_folder": "Education/DBMS",
  "confidence": 94,
  "reason": "High density of academic DBMS terminology including SQL keywords, normalization forms, and transaction ACID properties.",
  "recommended_action": "Move document 'DBMS_Notes.txt' to Education/DBMS/"
}
```

---

## 📂 Project Directory Structure

```text
DocuMind/
│
├── app.py                      # Main Gradio Blocks GUI Application
├── requirements.txt            # Python Package Dependencies
├── README.md                   # Project Documentation
├── .env                        # Local Environment Variables (Git ignored)
├── .env.example                # Environment Template
├── .gitignore                  # Git Ignore Specifications
│
├── config/
│   └── settings.py             # App Configuration & Dotenv Loader
│
├── services/
│   ├── document_processor.py   # Multi-Format Text Extractor (PDF/DOCX/TXT)
│   ├── langflow_client.py      # Langflow REST Client & Fallback Engine
│   └── auth.py                 # JWT Authentication & Session Service
│
├── utils/
│   ├── validators.py           # File Size & Format Validation
│   └── helpers.py              # Visual Tree Generator & Tag Formatter
│
├── langflow/
│   └── documind_flow.json      # Langflow Export Flow Configuration
│
├── sample_documents/           # Pre-loaded Sample Test Files
│   ├── DBMS_Notes.txt
│   ├── Resume.txt
│   └── Research_Paper.txt
│
└── docs/
    ├── architecture.md         # System Architecture Specification
    ├── workflow.md             # End-to-End User Flow Documentation
    ├── report.md               # CA3 Mini Project Report (9 Chapters)
    └── viva_questions.md       # 20 Viva Questions & Answers
```

---

## 🎓 Viva Preparation & Documentation Links

- 📘 **Full CA3 Project Report**: [docs/report.md](docs/report.md)
- ❓ **20 Viva Questions & Answers**: [docs/viva_questions.md](docs/viva_questions.md)
- 🏗️ **Architecture Specifications**: [docs/architecture.md](docs/architecture.md)

---

## 📜 Author & Acknowledgments
- **Project**: DocuMind Mini-Project
- **Course**: B.Tech CSE (CA3 Evaluation)
- **Built with**: Python, Gradio, Langflow, PyMuPDF, PyJWT
