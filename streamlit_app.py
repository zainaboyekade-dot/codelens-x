#streamlit run streamlit_app.py

import streamlit as st
import subprocess
import analyzer
import os

st.set_page_config(page_title="CodeLens-X", layout="wide")

st.title("Zaite's CodeLens-X🧠")
st.subheader("Hybrid C/C++ Code Analyzer (clang-tidy + AI)")

# -------------------------
# INPUT SECTION
# -------------------------
code = st.text_area("Paste your C/C++ code here:", height=300)

# -------------------------
# RUN ANALYSIS
# -------------------------
if st.button("📑Analyze Code"):

    if not code.strip():
        st.warning("Please paste some code first.")
        st.stop()

    file_path = "temp.cpp"
    with open(file_path, "w") as f:
        f.write(code)

    status = st.empty()
    status.info("Running clang-tidy + AI analysis...")

    analyzer.run_clang_tidy(file_path)
    issues = analyzer.get_issues(file_path)
    ai_results = analyzer.get_ai_explanations(issues)

    # -------------------------
    # SUMMARY
    # -------------------------
    st.markdown("## 📊 Summary")

    total = len(issues)
    warnings = sum(1 for i in issues if i["severity_tool"] == "warning")
    errors = sum(1 for i in issues if i["severity_tool"] == "error")

    st.write(f"**Total Issues:** {total}")
    st.write(f"**Warnings:** {warnings}")
    st.write(f"**Errors:** {errors}")

    if issues:
        lines = [str(i["location"]["line"]) for i in issues]
        st.write(f"**Issue Lines:** {', '.join(lines)}")
    else:
        st.success("No issues found 🎉")

    st.divider()

    # -------------------------
    # ISSUES + AI EXPLANATIONS
    # -------------------------
    if issues:

        for i, issue in enumerate(issues):

        st.markdown(f"""
    ## ‼️ Issue {i+1} - {issue['issue']}
    """)
    
        rule = issue.get("rule", "g++ compiler")
    
        with st.expander("🔴 clang-tidy details"):
            st.markdown(f"""
    - **Rule:** {rule}
    - **Line:** {issue["location"]["line"]}
    - **Column:** {issue["location"]["column"]}
    - **Severity:** {issue["severity_tool"]}
    """)
            # AI dropdown
            with st.expander("🤖 AI explanation"):
                st.text(ai_results[i])

            st.divider()

    status.success("Analysis complete ✔")

    # -------------------------
    # CLEANUP
    # -------------------------
    if os.path.exists("temp.cpp"):
        os.remove("temp.cpp")
