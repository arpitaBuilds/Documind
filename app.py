import os
import json
import gradio as gr

from config.settings import settings
from services.auth import AuthService
from services.document_processor import DocumentProcessor
from services.langflow_client import LangflowClient
from services.file_organizer import FileOrganizer
from utils.helpers import generate_folder_tree, format_tags


# Custom Modern CSS for Professional Aesthetic
CUSTOM_CSS = """
/* Theme Polish & Typography */
body, .gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.main-header {
    text-align: center;
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
    color: white;
    padding: 24px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(49, 46, 129, 0.25);
}

.main-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 6px;
    color: #ffffff;
}

.main-header p {
    font-size: 1.05rem;
    color: #c7d2fe;
    margin: 0;
}

.status-badge-container {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 15px;
}

.result-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.metric-box {
    background: #f1f5f9;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
}

.metric-val {
    font-size: 1.4rem;
    font-weight: 700;
    color: #4338ca;
}
"""

def build_app():
    with gr.Blocks(title="DocuMind - Intelligent Document Organization") as app:
        
        # Session State Storage
        session_state = gr.State(value={
            "is_authenticated": False,
            "username": "Guest",
            "token": "",
            "auth_type": "None",
            "login_time": ""
        })

        # Active Document States for Accept/Reject file movement
        active_file_state = gr.State(value="")
        active_folder_state = gr.State(value="")


        # Application Banner Header
        gr.HTML("""
        <div class="main-header">
            <h1>🧠 DocuMind</h1>
            <p>Intelligent Document Organization Assistant Using AI Agents</p>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">
                B.Tech CSE CA3 Mini-Project Evaluation
            </span>
        </div>
        """)

        # Global Session Status Bar
        with gr.Row(elem_classes=["status-badge-container"]):
            status_markdown = gr.Markdown(
                "🔒 **Status:** Not Authenticated (Guest Mode) — *Please log in to analyze documents.*"
            )

        with gr.Tabs() as main_tabs:
            
            # ==========================================
            # TAB 1: AUTHENTICATION & JWT SESSION
            # ==========================================
            with gr.TabItem("🔐 Authentication & Session", id="auth_tab"):
                gr.Markdown("### 🔑 User Login & JWT Session Management")
                gr.Markdown(
                    "Authenticate using Langflow credentials or Superuser session. "
                    "Secured with JWT (JSON Web Tokens)."
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        login_user_input = gr.Textbox(
                            label="Username",
                            placeholder="Enter username (Default: admin)",
                            value="admin"
                        )
                        login_pass_input = gr.Textbox(
                            label="Password",
                            placeholder="Enter password (Default: adminpassword123)",
                            type="password",
                            value="adminpassword123"
                        )
                        with gr.Row():
                            login_btn = gr.Button("🔓 Log In", variant="primary")
                            logout_btn = gr.Button("🔒 Log Out", variant="secondary")

                        auth_message = gr.Markdown("")

                    with gr.Column(scale=1):
                        gr.Markdown("#### 🛡️ Active JWT Session Details")
                        session_json_display = gr.JSON(
                            value=AuthService.get_safe_session({}),
                            label="Safe Session Claims (Protected JWT)"
                        )


            # ==========================================
            # TAB 2: DOCUMENT ORGANIZATION ASSISTANT
            # ==========================================
            with gr.TabItem("📄 Document Analysis & Organization", id="analysis_tab"):
                gr.Markdown("### 📤 Upload Document for AI Agent Analysis")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        file_input = gr.File(
                            label="Select Document (.pdf, .docx, .txt)",
                            file_types=[".pdf", ".docx", ".txt"],
                            type="filepath"
                        )
                        
                        sample_selector = gr.Radio(
                            choices=[
                                "None",
                                "sample_documents/DBMS_Notes.txt",
                                "sample_documents/Resume.txt",
                                "sample_documents/Research_Paper.txt"
                            ],
                            value="None",
                            label="Or select a pre-loaded sample document:"
                        )

                        analyze_btn = gr.Button("⚡ Analyze & Classify Document", variant="primary", size="lg")
                        
                        # Document Metadata Box
                        with gr.Accordion("ℹ️ Extracted File Details", open=False):
                            doc_meta_display = gr.JSON(label="Metadata")

                    with gr.Column(scale=1):
                        analysis_status = gr.Markdown("*Ready for analysis...*")

                        with gr.Group():
                            gr.Markdown("### 🤖 AI Agent Classification Result")
                            
                            with gr.Row():
                                res_category = gr.Textbox(label="Category", interactive=False)
                                res_subcategory = gr.Textbox(label="Sub-category", interactive=False)
                                res_confidence = gr.Textbox(label="Confidence Score", interactive=False)

                            res_summary = gr.Textbox(label="Short Document Summary", lines=3, interactive=False)
                            res_tags = gr.Markdown(label="Generated Tags")
                            res_action = gr.Textbox(label="Recommended Action", interactive=False)

                            with gr.Accordion("🧠 Agent Decision Rationale & Reasoning", open=False):
                                res_reason = gr.Markdown()

                            gr.Markdown("#### 📁 Suggested Folder Hierarchy Preview")
                            res_tree = gr.Markdown("```text\n(Upload a document to preview folder tree)\n```")

                        with gr.Row():
                            accept_btn = gr.Button("✅ Accept Recommendation", variant="primary")
                            reject_btn = gr.Button("❌ Reject", variant="stop")
                            reset_btn = gr.Button("🔄 Analyze Another", variant="secondary")

                        action_status = gr.Markdown("")

            # ==========================================
            # TAB 3: AGENT WORKFLOW & ARCHITECTURE
            # ==========================================
            with gr.TabItem("🧠 Agent Workflow & System Architecture", id="architecture_tab"):
                gr.Markdown("### 🏗️ DocuMind Autonomous AI Agent Execution Loop")
                gr.Markdown(
                    "DocuMind operates as an **autonomous decision-making AI agent**, progressing through "
                    "7 distinct operational stages from initial ingestion to human-verified file organization."
                )

                gr.HTML("""
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 20px; border-radius: 12px; margin: 15px 0;">
                    <h4 style="text-align: center; color: #1e1b4b; margin-top: 0; font-size: 1.15rem;">🚀 DocuMind 7-Stage Autonomous Agent Pipeline</h4>
                    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; margin-top: 15px;">
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #3b82f6; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #1d4ed8; font-size: 0.9rem;">1. 📤 Upload</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Submits document</span>
                        </div>
                        <div style="color: #94a3b8; font-weight: bold; font-size: 1.2rem;">➔</div>
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #6366f1; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #4338ca; font-size: 0.9rem;">2. 👁️ Perceive</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Extract text & meta</span>
                        </div>
                        <div style="color: #94a3b8; font-weight: bold; font-size: 1.2rem;">➔</div>
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #8b5cf6; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #6d28d9; font-size: 0.9rem;">3. 🧠 Reason</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Langflow LLM Agent</span>
                        </div>
                        <div style="color: #94a3b8; font-weight: bold; font-size: 1.2rem;">➔</div>
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #ec4899; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #be185d; font-size: 0.9rem;">4. 🎯 Decide</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Classify & structure</span>
                        </div>
                        <div style="color: #94a3b8; font-weight: bold; font-size: 1.2rem;">➔</div>
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #f59e0b; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #b45309; font-size: 0.9rem;">5. 💡 Explain</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Rationale & score</span>
                        </div>
                        <div style="color: #94a3b8; font-weight: bold; font-size: 1.2rem;">➔</div>
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #10b981; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #047857; font-size: 0.9rem;">6. 👤 Human Approval</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Accept or Reject</span>
                        </div>
                        <div style="color: #94a3b8; font-weight: bold; font-size: 1.2rem;">➔</div>
                        <div style="flex: 1; min-width: 110px; background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #059669; padding: 12px 8px; border-radius: 8px; text-align: center;">
                            <strong style="color: #065f46; font-size: 0.9rem;">7. ⚡ Action</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">Move file on disk</span>
                        </div>
                    </div>
                </div>
                """)

                gr.Markdown("""
                #### 🎯 Stage Breakdown in DocuMind:
                1. **Upload**: Accepts multi-format documents (`.pdf`, `.docx`, `.txt`) up to 10 MB limit.
                2. **Perception**: Extracts raw text, character counts, page data, and file metadata using PyMuPDF and python-docx.
                3. **Reasoning**: Passes text and metadata to Langflow LLM Agent workflow for domain inference.
                4. **Decision Making**: Selects optimal category, subcategory, tags, and target folder path.
                5. **Explainability**: Outputs explicit reasoning behind the classification alongside confidence percentage (0-100%).
                6. **Human-in-the-Loop**: Presents visual recommendation tree for user verification before finalizing actions.
                7. **Action**: Upon explicit **Accept**, physically organizes and moves the file to `organized_documents/<folder>/`.
                """)


            # ==========================================
            # TAB 4: SUPPORTED TAXONOMY & DOMAIN MAP
            # ==========================================
            with gr.TabItem("🗂️ Supported Taxonomy & Domains (22 Categories)", id="taxonomy_tab"):
                gr.Markdown("### 📚 Comprehensive 22-Domain AI Classification Taxonomy")
                gr.Markdown(
                    "DocuMind uses a multi-tier hierarchical taxonomy covering **22 specialized domains** "
                    "across 6 primary Knowledge Pillars. Below is the active taxonomy breakdown used by the AI Agent."
                )

                gr.HTML("""
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div style="background: #eef2ff; border-left: 5px solid #4338ca; padding: 14px; border-radius: 8px;">
                        <h4 style="margin: 0 0 6px 0; color: #3730a3;">💻 1. Computer Science & IT (9 Domains)</h4>
                        <ul style="font-size: 0.88rem; margin: 0; padding-left: 18px; color: #1e1b4b;">
                            <li>Web Development & Front-End</li>
                            <li>Database Management (DBMS)</li>
                            <li>Operating Systems (OS)</li>
                            <li>Computer Networks & TCP/IP</li>
                            <li>Data Structures & Algorithms (DSA)</li>
                            <li>AI & Machine Learning (AI/ML)</li>
                            <li>Cyber Security & Cryptography</li>
                            <li>Cloud Computing & DevOps</li>
                            <li>Software Engineering & SDLC</li>
                        </ul>
                    </div>

                    <div style="background: #f0fdf4; border-left: 5px solid #16a34a; padding: 14px; border-radius: 8px;">
                        <h4 style="margin: 0 0 6px 0; color: #166534;">🎓 2. Academics & Labs (3 Domains)</h4>
                        <ul style="font-size: 0.88rem; margin: 0; padding-left: 18px; color: #14532d;">
                            <li>College Practical Lab Manuals</li>
                            <li>Course Syllabus & Curriculum</li>
                            <li>Research Manuscripts & IEEE Papers</li>
                        </ul>
                    </div>

                    <div style="background: #fefce8; border-left: 5px solid #ca8a04; padding: 14px; border-radius: 8px;">
                        <h4 style="margin: 0 0 6px 0; color: #854d0e;">💼 3. Career & HR (3 Domains)</h4>
                        <ul style="font-size: 0.88rem; margin: 0; padding-left: 18px; color: #713f12;">
                            <li>Resumes & Candidate CVs</li>
                            <li>Offer Letters & HR Agreements</li>
                            <li>Degree & Course Certificates</li>
                        </ul>
                    </div>

                    <div style="background: #fff1f2; border-left: 5px solid #e11d48; padding: 14px; border-radius: 8px;">
                        <h4 style="margin: 0 0 6px 0; color: #9f1239;">📊 4. Finance & Banking (2 Domains)</h4>
                        <ul style="font-size: 0.88rem; margin: 0; padding-left: 18px; color: #881337;">
                            <li>Tax Invoices & Billing Receipts</li>
                            <li>Bank Statements & Audit Ledgers</li>
                        </ul>
                    </div>

                    <div style="background: #fdf4ff; border-left: 5px solid #c026d3; padding: 14px; border-radius: 8px;">
                        <h4 style="margin: 0 0 6px 0; color: #86198f;">⚖️ 5. Legal & Business (3 Domains)</h4>
                        <ul style="font-size: 0.88rem; margin: 0; padding-left: 18px; color: #701a75;">
                            <li>Legal Contracts & NDAs</li>
                            <li>Product Requirement Specs (PRD)</li>
                            <li>Government Identity Records</li>
                        </ul>
                    </div>

                    <div style="background: #f0f9ff; border-left: 5px solid #0284c7; padding: 14px; border-radius: 8px;">
                        <h4 style="margin: 0 0 6px 0; color: #075985;">🏥 6. Medical & General (2 Domains)</h4>
                        <ul style="font-size: 0.88rem; margin: 0; padding-left: 18px; color: #0c4a6e;">
                            <li>Medical Prescriptions & Health Reports</li>
                            <li>General Reference Documents</li>
                        </ul>
                    </div>
                </div>
                """)

                gr.Markdown("""
                | Knowledge Pillar | Domain Category | Target Recommended Folder | Key Triggers & Keywords |
                | :--- | :--- | :--- | :--- |
                | **Computer Science** | Web Development & Front-End | `Education/Web_Development/` | `JavaScript`, `HTML`, `CSS`, `DOM`, `Form Validation`, `addEventListener`, `React` |
                | **Computer Science** | Database Systems (DBMS) | `Education/DBMS/` | `DBMS`, `SQL`, `Normalization`, `1NF-3NF`, `ACID`, `ER Diagram`, `Transactions` |
                | **Computer Science** | Operating Systems (OS) | `Education/Operating_Systems/` | `Deadlock`, `CPU Scheduling`, `Semaphore`, `Paging`, `Kernel`, `Process Sync` |
                | **Computer Science** | Computer Networks | `Education/Computer_Networks/` | `TCP/IP`, `OSI Model`, `Socket`, `Subnetting`, `Wireshark`, `Router`, `DNS` |
                | **Computer Science** | Data Structures (DSA) | `Education/Data_Structures/` | `Trees`, `Graphs`, `Linked List`, `Dynamic Programming`, `Big O`, `Recursion` |
                | **Computer Science** | Artificial Intelligence / ML | `Education/AI_ML/` | `PyTorch`, `TensorFlow`, `Neural Network`, `LLM`, `NLP`, `Transformers`, `Scikit` |
                | **Computer Science** | Cyber Security | `Education/Cyber_Security/` | `AES/RSA`, `Encryption`, `Penetration Testing`, `Firewall`, `Ethical Hacking` |
                | **Computer Science** | Cloud & DevOps | `Education/Cloud_DevOps/` | `AWS`, `GCP`, `Docker`, `Kubernetes`, `CI/CD`, `Terraform`, `Microservices` |
                | **Computer Science** | Software Engineering | `Education/Software_Engineering/` | `SDLC`, `Agile`, `Scrum`, `UML Diagrams`, `Design Patterns`, `Requirements` |
                | **Academics** | Practical Lab Experiments | `Education/Lab_Experiments/` | `Experiment No`, `Practical Manual`, `Viva Voce`, `Observations Table` |
                | **Academics** | Course Syllabus | `Education/Course_Material/` | `Syllabus`, `Module 1-5`, `University Exam`, `Lecture Notes`, `Curriculum` |
                | **Research** | IEEE Research Papers | `Research/Publications/` | `Abstract`, `IEEE`, `ArXiv`, `Literature Survey`, `Citation`, `Novel Model` |
                | **Career** | Resumes & Portfolios | `Career/Resumes/` | `Resume`, `CV`, `Work Experience`, `Candidate Profile`, `LinkedIn`, `Skills` |
                | **Career** | Offer Letters & HR | `Career/Offer_Letters/` | `Offer Letter`, `Joining Date`, `CTC Package`, `Employment Agreement` |
                | **Career** | Degree & Certificates | `Career/Certificates/` | `Certificate of Completion`, `Degree Award`, `Internship Certificate` |
                | **Finance** | Invoices & Receipts | `Finance/Invoices/` | `Tax Invoice`, `Receipt`, `Amount Due`, `GSTIN`, `Billing Breakdown` |
                | **Finance** | Bank Statements | `Finance/Bank_Statements/` | `Bank Statement`, `Account Balance`, `Debit/Credit`, `Audit Ledger` |
                | **Business** | Product Specs & PRD | `Business/Product_Specs/` | `PRD`, `Product Requirement`, `User Story`, `Pitch Deck`, `Market Analysis` |
                | **Legal** | Contracts & NDAs | `Legal/Contracts/` | `Non-Disclosure Agreement`, `Terms of Service`, `Indemnification`, `Clause` |
                | **Personal** | Government Identity | `Personal/Identity_Records/` | `Passport`, `Aadhaar`, `Driver License`, `PAN Card`, `Rent Agreement` |
                | **Medical** | Health Reports | `Medical/Health_Records/` | `Doctor Prescription`, `Diagnostic Report`, `Clinical Notes`, `Blood Test` |
                | **General** | Reference Docs | `Other/General/` | Unstructured general documents, text archives, miscellaneous notes |
                """)

            # ==========================================
            # TAB 5: SYSTEM SETTINGS & DIAGNOSTICS
            # ==========================================
            with gr.TabItem("⚙️ System Settings & Health Check", id="settings_tab"):

                gr.Markdown("### 🛠️ Environment Configuration & Langflow Health")
                
                env_table = gr.Markdown(f"""
                | Setting | Environment Variable | Current Value |
                | :--- | :--- | :--- |
                | **Langflow Server URL** | `LANGFLOW_URL` | `{settings.LANGFLOW_URL}` |
                | **Flow ID** | `LANGFLOW_FLOW_ID` | `{settings.LANGFLOW_FLOW_ID or 'Not Set'}` |
                | **API Key Status** | `LANGFLOW_API_KEY` | `{'Configured' if settings.LANGFLOW_API_KEY else 'Not Set'}` |
                | **Max File Size** | `MAX_FILE_SIZE_MB` | `{settings.MAX_FILE_SIZE_MB} MB` |
                | **Allowed Formats** | `ALLOWED_EXTENSIONS` | `{', '.join(settings.ALLOWED_EXTENSIONS)}` |
                | **Demo Fallback Mode** | `DEMO_MODE` | `{settings.DEMO_MODE}` |
                """)

                check_health_btn = gr.Button("🔍 Test Langflow Backend Connection", variant="secondary")
                health_output = gr.Markdown("")

        # ==========================================
        # EVENT HANDLERS & CALLBACK FUNCTIONS
        # ==========================================

        def handle_login(username, password):
            result = AuthService.login_user(username, password)
            session = result["session"]
            safe_display_session = AuthService.get_safe_session(session)
            if result["success"]:
                status_txt = f"🟢 **Authenticated User:** `{session['username']}` | **Session:** `{session['auth_type']}`"
                msg_txt = f"✅ {result['message']}"
            else:
                status_txt = "🔒 **Status:** Not Authenticated (Guest Mode)"
                msg_txt = f"❌ {result['message']}"
            
            return session, status_txt, msg_txt, safe_display_session

        def handle_logout():
            result = AuthService.logout_user()
            session = result["session"]
            safe_display_session = AuthService.get_safe_session(session)
            status_txt = "🔒 **Status:** Not Authenticated (Guest Mode)"
            msg_txt = "ℹ️ Logged out of session."
            return session, status_txt, msg_txt, safe_display_session


        def handle_sample_selection(choice):
            if choice != "None" and os.path.exists(choice):
                return choice
            return None

        def handle_analysis(file_path, session):
            if not file_path:
                return (
                    "❌ **Error:** Please upload a document or select a sample document first.",
                    {}, "", "", "", "", "`#None`", "", "", "```text\nNo document loaded\n```",
                    "", ""
                )

            # 1. Process Document Text & Extract Metadata
            try:
                doc_data = DocumentProcessor.extract_text_and_metadata(file_path)
            except Exception as e:
                return (
                    f"❌ **Document Error:** {str(e)}",
                    {}, "", "", "", "", "`#None`", "", "", "```text\nExtraction failed\n```",
                    "", ""
                )

            # Useful extracted file details formatting
            formatted_meta = {
                "Filename": doc_data["filename"],
                "File Format": doc_data["file_type"],
                "File Size": f"{doc_data['file_size_kb']} KB",
                "Page Count": f"{doc_data['page_count']} page(s)",
                "Character Count": f"{doc_data['char_count']:,} characters",
                "Text Truncated": "Yes (Exceeded 15,000 limit)" if doc_data.get("is_truncated") else "No (Complete Text Parsed)"
            }

            # 2. Invoke AI Agent (Langflow / Fallback)
            agent_response = LangflowClient.analyze_document(doc_data, session)

            if not agent_response["success"]:
                return (
                    f"⚠️ **Access Denied / Error:** {agent_response['error']}",
                    formatted_meta, "", "", "", "", "`#None`", "", "", "```text\nAnalysis restricted\n```",
                    file_path, ""
                )

            res = agent_response["data"]
            source = agent_response.get("source", "AI Engine")

            category = res.get("category", "General & Miscellaneous")
            subcategory = res.get("subcategory", "General")
            summary = res.get("summary", "No summary generated.")
            tags = res.get("tags", ["General"])
            suggested_folder = res.get("suggested_folder", "Other/General")
            confidence = f"{res.get('confidence', 85)}%"
            reason = res.get("reason", "Standard classification based on document semantic text.")
            recommended_action = res.get("recommended_action", f"Move document '{doc_data['filename']}' to {suggested_folder}/")

            formatted_tags_md = format_tags(tags)
            tree_view_md = generate_folder_tree(suggested_folder, doc_data["filename"])
            status_msg = f"✨ **Analysis Complete!** (Engine: *{source}*)"

            return (
                status_msg,
                formatted_meta,
                category,
                subcategory,
                confidence,
                summary,
                formatted_tags_md,
                recommended_action,
                f"**Reasoning:** {reason}",
                tree_view_md,
                file_path,
                suggested_folder
            )

        def handle_accept(src_file, folder):
            if not src_file or not folder:
                return "⚠️ **Action Incomplete:** No active recommendation to organize. Please analyze a document first."
            
            res = FileOrganizer.organize_file(src_file, folder)
            if res["success"]:
                return (
                    f"🎉 **Action Executed & File Organized!**\n"
                    f"Successfully moved **`{os.path.basename(src_file)}`** to organized target location:\n"
                    f"`{res['relative_path']}`"
                )
            else:
                return f"❌ **Organization Error:** {res['message']}"

        def handle_reject():
            return "🛑 **Action Rejected:** Recommendation dismissed by user. No changes were made to the filesystem."

        def handle_reset():
            return (
                "ℹ️ Ready for new document.",
                None, "None", {}, "", "", "", "", "`#None`", "", "", "```text\n(Upload a document to preview folder tree)\n```", "", "", ""
            )

        def handle_health_check():
            import requests
            headers = {
                "Bypass-Tunnel-Reminder": "true",
                "User-Agent": "DocuMind-Client"
            }
            base_url = settings.LANGFLOW_URL.rstrip('/')
            for ep in ["/health", "/api/v1/health", ""]:
                try:
                    res = requests.get(f"{base_url}{ep}", headers=headers, timeout=5)
                    if res.status_code in (200, 302, 307):
                        return f"✅ **Langflow Server is Online & Reachable!** (URL: `{settings.LANGFLOW_URL}`)"
                except Exception:
                    pass
            return (
                f"⚠️ **Langflow Server is Offline or Unreachable** (`{settings.LANGFLOW_URL}`).\n"
                f"*(Note: Langflow API will be invoked when server is reachable. Set DEMO_MODE=true for offline fallback testing.)*"
            )


        # Wire Up Event Listeners
        login_btn.click(
            fn=handle_login,
            inputs=[login_user_input, login_pass_input],
            outputs=[session_state, status_markdown, auth_message, session_json_display]
        )

        logout_btn.click(
            fn=handle_logout,
            outputs=[session_state, status_markdown, auth_message, session_json_display]
        )

        sample_selector.change(
            fn=handle_sample_selection,
            inputs=[sample_selector],
            outputs=[file_input]
        )

        analyze_btn.click(
            fn=handle_analysis,
            inputs=[file_input, session_state],
            outputs=[
                analysis_status,
                doc_meta_display,
                res_category,
                res_subcategory,
                res_confidence,
                res_summary,
                res_tags,
                res_action,
                res_reason,
                res_tree,
                active_file_state,
                active_folder_state
            ]
        )

        accept_btn.click(
            fn=handle_accept,
            inputs=[active_file_state, active_folder_state],
            outputs=[action_status]
        )
        
        reject_btn.click(
            fn=handle_reject,
            outputs=[action_status]
        )
        
        reset_btn.click(
            fn=handle_reset,
            outputs=[
                analysis_status,
                file_input,
                sample_selector,
                doc_meta_display,
                res_category,
                res_subcategory,
                res_confidence,
                res_summary,
                res_tags,
                res_action,
                res_reason,
                res_tree,
                action_status,
                active_file_state,
                active_folder_state
            ]
        )


        check_health_btn.click(fn=handle_health_check, outputs=[health_output])

    return app

if __name__ == "__main__":
    app = build_app()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 7861))
    share_flag = os.getenv("SHARE_LINK", "false").lower() in ("true", "1", "t")
    print(f"[DocuMind] Starting Application on http://{host}:{port} (Public Share: {share_flag}) ...")
    app.launch(server_name=host, server_port=port, share=share_flag, css=CUSTOM_CSS, theme=gr.themes.Soft(primary_hue="indigo"))


