#python analyzer.py test_code.cpp

import sys
import os
import re
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# 1. RUN CLANG-TIDY
# ---------------------------
def run_clang_tidy(file_path):
    os.system(f'cmd /c "clang-tidy {file_path} -- -std=c++17 > output.txt 2>&1"')

# ---------------------------
# 2. PARSE ISSUES
# ---------------------------
def get_issues(file_path):

    if not os.path.exists("output.txt"):
    return []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    pattern = r'([A-Za-z]:\\.*?\.cpp):(\d+):(\d+):\s*(warning|error):\s*(.*?)\s*\[(.*?)\]'

    matches = re.finditer(pattern, text)

    issues = []

    for m in matches:
        issue_obj = {
            "language": "cpp",
            "code": code.strip(),
            "issue": m.group(5).strip(),
            "rule": m.group(6),
            "severity_tool": m.group(4),
            "location": {
                "line": int(m.group(2)),
                "column": int(m.group(3))
            }
        }

        issues.append(issue_obj)

    return issues


# ---------------------------
# 3. AI PROCESSING
# ---------------------------
def get_ai_explanations(issues):
    ai_results = []

    if issues:

        system_prompt = """
    You are ONLY an explainer inside a code analysis system.

    You do NOT detect issues, guess problems, or add new information.
    You are a deterministic formatting engine.

    You are a function, not a personality.

    INPUT FORMAT (JSON):
    - language = programming language
    - code = full code context
    - issue = detected problem
    - rule = clang-tidy rule that triggered this issue
    - severity_tool = original tool severity (warning/error)
    - location = exact line and column

    ABSOLUTE OUTPUT RULES:
    You MUST output ONLY in the format below.
    You MUST NOT output JSON.
    You MUST NOT add extra fields.
    You MUST NOT change order, labels, or wording.
    You MUST NOT include commentary.

    OUTPUT FORMAT:

    Location:
    Line: <line>, Column: <column>

    Code:
    <original snippet>

    Issue:
    <short label>

    Severity:
    <low | medium | high>

    Explanation:
    <simple explanation>

    Impact:
    <what can go wrong in real systems>

    Fix:
    <corrected code or steps>

    SEVERITY RULE:
    - error → HIGH
    - warning → MEDIUM (unless critical → HIGH)
    """

    for issue in issues:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(issue, indent=2)
                }
            ]
        )

        ai_results.append(response.choices[0].message.content)

    return ai_results

# ---------------------------
# 4. SUMMARY + REPORT
# ---------------------------
def print_report(issues, ai_results):

    total = len(issues)

    warning_count = sum(1 for i in issues if i["severity_tool"] == "warning")
    error_count = sum(1 for i in issues if i["severity_tool"] == "error")

    lines = [i["location"]["line"] for i in issues]

    print("\n=== CodeLens-X Report ===\n")
    print("--- Summary ---")
    print(f"Total Issues: {total} | Warnings: {warning_count} | Errors: {error_count}")
    print(f"Issue Lines: {', '.join(map(str, lines))}")
    print("\n" + "="*60 + "\n")

    for i, result in enumerate(ai_results, 1):
        print(f"Issue {i}:\n")
        print(result)
        print("\n" + "="*60 + "\n")

# ---------------------------
# 5. MAIN FLOW
# ---------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <file.cpp>")
        return
    file_path = sys.argv[1]
    run_clang_tidy(file_path)
    issues = get_issues(file_path)

    if not issues:
        print("\n=== CodeLens-X Report ===\n")
        print("Summary: No issues found 🎉")
        return

    ai_results = get_ai_explanations(issues)
    print_report(issues, ai_results)

if __name__ == "__main__":
    main()
