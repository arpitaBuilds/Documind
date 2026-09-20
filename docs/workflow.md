# DocuMind End-to-End User & Data Workflow

## Workflow Execution Steps

```
[ User ] --(1. Login)--> [ AuthService ] --(JWT Token)--> [ Session State ]
   |
   +--(2. Upload File)--> [ DocumentProcessor ] --(Clean Text)--> [ LangflowClient ]
                                                                          |
                                                               (3. Send REST API Payload)
                                                                          v
[ Gradio UI ] <-- (5. Render Category & Tree) <-- [ Langflow Agent / LLM Flow ]
   |
   +--(6. Click Accept/Reject)--> [ Execution Result / User Confirmation ]
```

### Step 1: Authentication & JWT Acquisition
1. User navigates to the **Authentication & Session** tab in the Gradio GUI.
2. User enters credentials (e.g. `admin` / `adminpassword123`).
3. `AuthService.login_user()` authenticates the request and generates a signed JWT token stored in Gradio `gr.State`.

### Step 2: Document Ingestion & Text Extraction
1. User selects or uploads a `.pdf`, `.docx`, or `.txt` document (or selects a sample document).
2. `validators.py` verifies extension and enforces the 10MB size limit.
3. `document_processor.py` extracts text using `PyMuPDF` (for PDF), `python-docx` (for DOCX), or UTF-8 file reading (for TXT).

### Step 3: Agent Inference & Structured Output Generation
1. `langflow_client.py` constructs a JSON payload containing the extracted document text and JWT token/API Key header.
2. The Langflow workflow executes:
   - System Prompt enforces JSON output matching the target schema.
   - LLM analyzes document semantics.
   - Output Parser returns structured JSON:
     `category`, `subcategory`, `summary`, `tags`, `suggested_folder`, `confidence`, `reason`, `recommended_action`.

### Step 4: UI Rendering & Tree Visualization
1. Gradio populates metadata cards, category fields, confidence scores, and reasoning accordion.
2. `helpers.generate_folder_tree()` renders an ASCII visual directory tree.

### Step 5: Human-in-the-Loop Approval
1. User reviews the AI decision and clicks **Accept Recommendation** or **Reject**.
2. Action feedback is displayed on screen.
