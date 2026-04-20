🧠 CodeLens-X

Hybrid C/C++ Code Analysis System using clang-tidy + AI Explanations

👉 Live Demo: https://codelens-x.streamlit.app

🚀 Overview

CodeLens-X is a hybrid code analysis system that combines static analysis (clang-tidy) with AI-based reasoning (LLMs) to provide structured, human-readable debugging reports for C/C++ code.

Instead of simply showing raw compiler warnings, CodeLens-X transforms them into:

Clear explanations
Severity classification
Real-world impact insights
Actionable fixes
💡 Core Idea

Traditional static analysis tools are accurate but hard to interpret.
AI tools are easy to understand but unreliable for detection.

CodeLens-X bridges this gap:

clang-tidy detects issues → AI explains them → system presents structured reports

🧱 System Architecture
User Code (C/C++)
        ↓
Streamlit UI (input interface)
        ↓
Temporary file generation (temp.cpp)
        ↓
clang-tidy (static analysis engine)
        ↓
Python parser (structured extraction)
        ↓
OpenAI GPT (issue explanation engine)
        ↓
Streamlit UI (formatted report)
⚙️ Features
🔍 Static Code Analysis
Uses clang-tidy
Detects:
Memory issues
Syntax problems
Code quality issues
🧩 Structured Parsing
Extracts:
File name
Line & column
Rule ID
Severity
Message
Converts raw output into structured data
🤖 AI Explanation Engine
Explains each issue clearly
Provides:
Why it matters
Real-world impact
Suggested fixes
Enforced strict output format for consistency
🖥️ Interactive UI (Streamlit)
Paste C/C++ code
Run full analysis in one click
View structured results:
📊 Summary
🔴 Issues
🤖 AI explanations
📊 Output Structure
📌 Summary
Total issues
Warnings / Errors
Affected lines
🧾 Issue Breakdown

Each issue includes:

Location (line & column)
clang-tidy rule
Severity
AI explanation
Impact
Fix
🧠 Design Philosophy

CodeLens-X is built on a simple principle:

Deterministic detection + AI interpretation = reliable and understandable code analysis

System roles are strictly separated:

clang-tidy → detection
Python parser → structuring
LLM → explanation
Streamlit → presentation
🔧 Tech Stack
Python
clang-tidy (LLVM)
OpenAI GPT-4.1-mini
Streamlit
Regex-based parsing system
⚠️ Challenges Solved
PowerShell output corruption (stderr handling issues)
Missing compilation context for clang-tidy
Regex mismatches with real-world output formats
AI response inconsistency → fixed with strict prompting
Multi-layer pipeline debugging (CLI → parser → AI → UI)
🧪 Evaluation

The system was tested on:

✔ Syntax Errors
Missing semicolons
Invalid declarations
✔ Memory Issues
Uninitialized pointers
Unsafe memory usage
✔ Clean Code Inputs
Style suggestions
Best practice warnings
📈 Key Insight

Static analysis tools are highly accurate but not human-readable, while AI improves interpretability but must be strictly controlled to remain reliable.

CodeLens-X demonstrates that combining both creates a more usable developer tool.

🎥 Demo

👉 https://codelens-x.streamlit.app

🚀 Future Improvements
Multi-file project analysis
AST-based deeper parsing
Batch issue processing
Improved AI deduplication logic
Performance optimization for large codebases
🏁 Final Statement

CodeLens-X is a hybrid system that successfully integrates static analysis and AI reasoning to provide accurate, structured, and human-readable debugging assistance for C/C++ developers.
