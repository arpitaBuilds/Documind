import json
import re

def generate_folder_tree(suggested_folder: str, filename: str) -> str:
    """
    Generates a visual ASCII tree structure for the proposed folder path.
    Example:
    Education/
        └── DBMS/
              └── DBMS_Unit3.pdf
    """
    parts = [p.strip() for p in suggested_folder.strip("/\\").split("/") if p.strip()]
    if not parts:
        parts = ["Unorganized"]
    
    tree_lines = []
    indent = ""
    for idx, part in enumerate(parts):
        if idx == 0:
            tree_lines.append(f"📁 {part}/")
        else:
            indent += "    "
            tree_lines.append(f"{indent}└── 📁 {part}/")
    
    indent += "    "
    tree_lines.append(f"{indent}└── 📄 {filename}")
    
    return "```text\n" + "\n".join(tree_lines) + "\n```"

def format_tags(tags: list) -> str:
    """Formats a list of tag strings into hashtag chips for display."""
    if not tags:
        return "`#General`"
    formatted = []
    for tag in tags:
        tag_clean = tag.strip().replace("#", "").replace(" ", "")
        formatted.append(f"`#{tag_clean}`")
    return " ".join(formatted)

def parse_json_from_llm(response_text: str) -> dict:
    """
    Robustly extracts and parses JSON output from LLM string responses,
    handling markdown backticks or extra text.
    """
    if isinstance(response_text, dict):
        return response_text
    
    clean_text = str(response_text).strip()
    
    # Try direct json load
    try:
        return json.loads(clean_text)
    except Exception:
        pass
    
    # Try finding markdown ```json ... ``` blocks
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except Exception:
            pass
            
    # Try finding any {...} pattern
    brace_match = re.search(r"(\{.*\})", clean_text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(1))
        except Exception:
            pass
            
    raise ValueError(f"Could not parse valid JSON from response: {clean_text[:150]}...")
