# DocuMind Architecture Specification

## 1. System Overview

DocuMind is an intelligent document organization assistant powered by an **AI Agent architecture** integrated with **Gradio** and **Langflow**. It enables users to perceive, analyze, classify, and organize unstructured documents (`.pdf`, `.docx`, `.txt`) into clean folder hierarchies with explanatory reasoning and confidence metrics.

```
+-----------------------------------------------------------------------+
|                              GRADIO GUI                               |
|   +--------------------------+     +------------------------------+   |
|   |  JWT Authentication Tab  |     | Document Organization Tab    |   |
|   +--------------------------+     +------------------------------+   |
+-----------------------------------||----------------------------------+
                                    || (File Upload & Session Token)
                                    \/
+-----------------------------------------------------------------------+
|                            BACKEND SERVICES                           |
|  +------------------------+  +-------------------+  +--------------+  |
|  |  document_processor.py |  |    auth.py        |  |  helpers.py  |  |
|  |  (PyMuPDF / docx / txt)|  |  (JWT Management) |  |  (Tree View) |  |
|  +------------------------+  +-------------------+  +--------------+  |
+-----------------------------------||----------------------------------+
                                    || (REST API Request with Token / Key)
                                    \/
+-----------------------------------------------------------------------+
|                            LANGFLOW AGENT                             |
|  Input Node -> Prompt Template -> LLM Model -> JSON Schema Parser     |
+-----------------------------------------------------------------------+
```

## 2. AI Agent Loop Architecture

Unlike static prompt-reply tools, DocuMind implements an **autonomous agent feedback loop**:

1. **PERCEIVE**: Extracts raw text, character metrics, and structural data from PDF, DOCX, and TXT files using native parsers (`fitz`, `python-docx`).
2. **REASON**: Evaluates extracted text against semantic taxonomy rules via the Langflow prompt workflow.
3. **DECIDE**: Selects primary category (Education, Career, Research, Finance, Personal, Other), sub-category, tags, and target folder path (`suggested_folder`).
4. **EXPLAIN**: Generates explicit classification rationale (`reason`) alongside a quantitative confidence score (`confidence: 0-100%`).
5. **RECOMMEND**: Synthesizes a visual directory tree structure (`generate_folder_tree()`) for visual preview.
6. **HUMAN-IN-THE-LOOP APPROVAL**: Waits for human verification (`[Accept] / [Reject]`) before confirming organization actions.

## 3. Authentication & JWT Session Architecture

Security is built into DocuMind using **JWT (JSON Web Tokens)** and Langflow authentication mechanisms:

- **Token Generation**: User credentials are validated against the Langflow `/api/v1/login` backend endpoint (or local superuser JWT key derivation).
- **Session Payload**: Stores subject claims, role attributes, creation timestamp (`iat`), and expiration (`exp`).
- **API Protection**: Authorization headers (`Authorization: Bearer <jwt_token>` or `x-api-key`) protect downstream agent invocation endpoints.
- **Environment Isolation**: Secrets (`LANGFLOW_SECRET_KEY`, `LANGFLOW_API_KEY`) are managed via `.env` files and excluded from repository commits using `.gitignore`.
