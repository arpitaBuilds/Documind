# CA3 MINI PROJECT REPORT

## PROJECT TITLE: DocuMind: Intelligent Document Organization Assistant Using AI Agents
**Course**: B.Tech Computer Science and Engineering (CSE)  
**Evaluation**: CA3 Mini Project (30 Marks)  

---

### ABSTRACT
Modern digital environments are inundated with unstructured document formats including PDFs, Word documents, and text files. Manual document classification and directory structuring is tedious, error-prone, and time-consuming. This report presents **DocuMind**, an intelligent document organization assistant engineered using AI agent architecture, Langflow orchestration, JWT authentication, and a Gradio web interface. DocuMind perceives document text across multi-file formats, reasons over contextual semantics using Large Language Models (LLMs), classifies content into precise domain taxonomies, generates metadata (summary, tags, confidence score, decision rationale), and proposes visual folder hierarchies for human approval. The system incorporates JWT-based session security via Langflow authentication mechanisms and operates seamlessly with an intelligent offline fallback engine for robust local demonstration.

**Keywords**: AI Agents, Langflow, Gradio, Document Classification, JWT Authentication, Natural Language Processing, Software Architecture.

---

## CHAPTER 1: BACKGROUND AND TECHNICAL OVERVIEW

### 1.1 Background
Data proliferation across academic, personal, and enterprise environments has transformed personal document management into a critical challenge. Users frequently accumulate hundreds of downloads, notes, research papers, and invoices into single unorganized folders. Standard search utilities rely on literal string matching, failing to capture semantic domain relationships. Recent developments in Large Language Model (LLM) workflows and AI Agent paradigms allow software systems to act autonomously—extracting content, reasoning over intent, classifying taxonomies, and generating structured execution plans.

### 1.2 Objectives
1. **Automated Multi-Format Ingestion**: Extract clean text from PDF, DOCX, and TXT files using Python libraries (`PyMuPDF`, `python-docx`).
2. **AI Agent Workflow Orchestration**: Implement a Langflow-based prompt and inference pipeline that outputs validated JSON containing document category, sub-category, summary, tags, suggested folder, confidence score, and rationale.
3. **Secure JWT Authentication**: Integrate Langflow's built-in JWT authentication and API key headers to protect document processing endpoints.
4. **Interactive GUI**: Build an intuitive, responsive Gradio web interface providing real-time feedback, reasoning accordions, and ASCII directory tree visual previews.
5. **Human-in-the-Loop Control**: Enable explicit user approval (`[Accept Recommendation] / [Reject]`) prior to finalizing file movements.

### 1.3 Hardware Components
As DocuMind is a **pure software application**, no physical hardware circuit components (e.g., microcontrollers, sensors, relays) are required. The hardware environment comprises standard host computer specifications:
- **Processor**: x86_64 / ARM64 Quad-Core CPU (2.0 GHz or higher)
- **Memory (RAM)**: 8 GB minimum (16 GB recommended)
- **Storage**: 500 MB available solid-state storage
- **Network**: Localhost network interface for Gradio web host (`127.0.0.1:7860`) and REST API calls.

---

## CHAPTER 2: PROBLEM STATEMENT AND MOTIVATION

### 2.1 Problem Statement
Unstructured digital files lack uniform metadata, making manual organization inefficient. Existing file managers require users to manually create nested folder trees and drag-and-drop individual files. When dealing with large volumes of course notes, research publications, resumes, and financial receipts, manual sorting leads to misplaced files, duplicated records, and wasted productivity.

### 2.2 Motivation
The primary motivation for DocuMind is to replace static manual sorting with an **autonomous AI Agent** capable of understanding *what* a document is about rather than merely looking at its title. By integrating Langflow for visual flow orchestration and Gradio for accessible UI design, DocuMind demonstrates how AI agents can perform intelligent administrative tasks securely and transparently for end users.

---

## CHAPTER 3: NOVELTY AND INNOVATIVE CONTRIBUTIONS

### 3.1 Novelty
- **Autonomous Agent Loop**: Combines Perception -> Reasoning -> Decision -> Explanation -> Recommendation -> Human Approval in a single closed-loop workflow.
- **Explainable AI Classification**: Unlike black-box classifiers, DocuMind emits quantitative confidence scores alongside plain-English explanations detailing *why* a specific category and folder path were recommended.
- **Visual Folder Tree Generation**: Generates instantaneous ASCII directory previews enabling immediate visual verification.

### 3.2 Innovative Contributions
1. **Langflow & Gradio Integration**: Demonstrates low-code AI workflow orchestration with a high-flexibility Python frontend.
2. **JWT-Secured Session Layer**: Enforces token-based session handling derived from Langflow's authentication system.
3. **Dual-Engine Hybrid Execution**: Features a live REST API connector to Langflow alongside an offline fallback engine ensuring 100% operational uptime during live viva demonstrations.

---

## CHAPTER 4: TECHNICAL ADVANTAGES AND PRACTICAL USEFULNESS

### 4.1 Technical Advantages
- **Modular Micro-Architecture**: Clean separation between UI (`app.py`), services (`auth.py`, `document_processor.py`, `langflow_client.py`), and utilities (`helpers.py`, `validators.py`).
- **Strict Environment Isolation**: API keys and JWT secrets are managed strictly through `.env` environment variables.
- **Format Agnostic**: Seamlessly handles PDF, DOCX, and TXT files without requiring external software dependencies.

### 4.2 Practical Usefulness
DocuMind directly addresses real-world document sprawl for students, researchers, finance teams, and job seekers by providing automated sorting recommendations within seconds of upload.

---

## CHAPTER 5: DETAILED METHODOLOGY / SYSTEM ARCHITECTURE

### 5.1 System Architecture
The application follows a three-tier architecture:
1. **Presentation Layer (Gradio GUI)**: Handles authentication forms, document upload inputs, metadata displays, reasoning accordions, and folder tree outputs.
2. **Application Service Layer (Python Backend)**: Enforces input validation, file text extraction, session token generation, and REST communication.
3. **Orchestration Layer (Langflow Agent)**: Manages prompt formatting, LLM inference, and JSON parsing.

### 5.2 Working Principle
When a user uploads a document:
1. `validators.py` verifies the extension and file size limit (10MB).
2. `document_processor.py` extracts text using `fitz` or `python-docx`.
3. `langflow_client.py` transmits the text along with JWT/API Key headers to the Langflow flow endpoint.
4. The LLM processes the prompt and returns structured JSON.
5. Gradio renders the structured result and displays the ASCII tree path for human approval.

### 5.3 Circuit Connections
> **Note**: This project is completely **software-based**. No physical electronic circuit connections, hardware components, breadboards, or microcontrollers are utilized.

### 5.4 Simulation & Testing
System functionality was simulated and verified through:
- **Unit Validation**: Verified text extraction across sample PDF, DOCX, and TXT test files.
- **Session Security Testing**: Tested login authentication with valid and invalid JWT tokens.
- **UI Integration Verification**: Executed end-to-end tests on Gradio web interface (`http://127.0.0.1:7860`).

---

## CHAPTER 6: PRIOR ART AND RELATED WORK

### 6.1 Introduction
Document classification has evolved from traditional rule-based regex parsers to machine learning classifiers and modern LLM-driven agents.

### 6.2 Existing Technologies
- **Rule-Based Scripting**: Fast but brittle; fails when file naming conventions change.
- **Supervised ML Classifiers (TF-IDF + Naive Bayes)**: Require extensive pre-labeled training data and struggle with out-of-vocabulary terms.
- **Desktop Search Tools (Everything, Spotlight)**: Provide indexed search but do not automatically organize or move files into structured hierarchies.

### 6.3 Related Work
Recent research emphasizes LLM agents capable of dynamic reasoning and structured tool interaction. DocuMind builds upon this paradigm by combining agent reasoning with visual flow orchestration in Langflow and accessible GUI deployment in Gradio.

### 6.4 Summary Comparison
| Feature | Rule-Based Scripts | Supervised ML | DocuMind AI Agent |
| :--- | :--- | :--- | :--- |
| **Semantic Reasoning** | No | Limited | High (LLM Context) |
| **Setup Cost** | Low | High (Training required) | Zero Training (Prompt-based) |
| **Explainable Reasoning** | No | No | Yes (Explicit Rationale) |
| **GUI & JWT Security** | Rare | Rare | Native (Gradio + JWT) |

---

## CHAPTER 7: APPLICATIONS AND DEPLOYMENT AREAS

### 7.1 Applications
- **Academic Note Organization**: Categorizing lecture notes, lab manuals, and assignments by subject (e.g., `Education/DBMS`).
- **Career Management**: Sorting resumes, cover letters, and certificates.
- **Financial Record Archiving**: Sorting invoices, receipts, and tax audits.

### 7.2 Deployment Areas
- Student laptops and university computer laboratories.
- Enterprise document management repositories.
- Personal cloud storage preliminary sorting assistant.

---

## CHAPTER 8: CONCLUSION AND FUTURE SCOPE

### 8.1 Conclusion
DocuMind successfully demonstrates a complete, beginner-friendly yet technically robust AI Agent mini-project for document organization. By leveraging Python, Gradio, Langflow, PyMuPDF, and JWT authentication, the system transforms unstructured document text into organized folder taxonomies accompanied by clear reasoning and user control.

### 8.2 Future Scope
1. **Physical File Operations**: Implementing disk file move/copy execution upon user acceptance.
2. **Vector Database Integration (RAG)**: Indexing organized documents into ChromaDB or FAISS for semantic Q&A.
3. **Optical Character Recognition (OCR)**: Integrating Tesseract OCR to support scanned image documents (`.png`, `.jpg`).
4. **Cloud Integration**: Supporting Google Drive and Dropbox automated sync.

---

## CHAPTER 9: GITHUB LINK AND SHORT CODE

### 9.1 Repository Structure
```text
DocuMind/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── config/settings.py
├── services/
│   ├── document_processor.py
│   ├── langflow_client.py
│   └── auth.py
├── utils/
│   ├── validators.py
│   └── helpers.py
├── langflow/documind_flow.json
└── sample_documents/
```

### 9.2 Representative Code Snippets

#### Document Text Extraction (`document_processor.py`):
```python
import fitz # PyMuPDF
import docx

def _extract_pdf(file_path: str) -> tuple[str, int]:
    doc = fitz.open(file_path)
    text_pages = [page.get_text("text") for page in doc]
    return "\n\n".join(text_pages), len(doc)
```

#### JWT Token Validation (`auth.py`):
```python
import jwt
import datetime

def generate_jwt_token(username: str, secret_key: str) -> str:
    payload = {
        "sub": username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")
```
