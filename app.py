import streamlit as st
import os, pandas as pd
from dotenv import load_dotenv
from io import BytesIO
import matplotlib.pyplot as plt

from langchain_openai import AzureChatOpenAI
from utils.helpers import money
from agents.orchestrator_agent import orchestrate

from utils.helpers import load_txt
from services.roi_service import calculate_roi, add_what_if, add_decisions
from services.jira_service import create_test_case

# -----------------------------
# SESSION STATE
# -----------------------------
if "estimation_rows" not in st.session_state:
    st.session_state.estimation_rows = []

if "tc_rows" not in st.session_state:
    st.session_state.tc_rows = []

# -----------------------------
# ENV & MODEL
# -----------------------------
load_dotenv()
model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("OPENAI_ACCESS_TOKEN"),
    api_version=os.getenv("API_VERSION"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    temperature=0.2
)

# -----------------------------
# STANDARDS
# -----------------------------
qa_standards = load_txt("data/qa_estimation_standards.txt")
tc_standards = load_txt("data/testing_standard.txt")

# -----------------------------
# UI
# -----------------------------
st.title("🚀 AI-Powered QA Cost Intelligence Platform")
st.caption("Transforms user stories into test cases, automation decisions, and ROI using explainable AI.")

stories_text = st.text_area("Enter User Stories (separate each story using | )", height=200)
what_if_multiplier = st.sidebar.slider("🔧 Automation Cost What-If Multiplier", 0.5, 2.0, 1.0, 0.1)

# -----------------------------
# GENERATE
# -----------------------------
if st.button("Analyze Impact") and stories_text.strip():
    st.session_state.estimation_rows = []
    st.session_state.tc_rows = []

    stories = [s.strip() for s in stories_text.split("|") if s.strip()]

    for story in stories:
        estimation, test_cases = orchestrate(model, qa_standards, tc_standards, story, what_if_multiplier)
        st.session_state.estimation_rows.append(estimation)
        st.session_state.tc_rows.extend(test_cases)

# -----------------------------
# RESULTS
# -----------------------------
if st.session_state.estimation_rows:
    import services.excel_service as excel_service
    excel_service.show_dashboard_and_download(st.session_state.estimation_rows, st.session_state.tc_rows, what_if_multiplier)

############JIRA INTEGRATION#####################s

st.subheader("📌 Jira Integration")

if st.button("🚀 Create Test Cases in Jira"):
    success = 0
    failed = 0

    for tc in st.session_state.tc_rows:
        try:
            create_test_case(tc)
            success += 1
        except Exception as e:
            failed += 1
            st.error(str(e))

    st.success(f"✅ {success} Test Cases created in Jira")
    if failed:
        st.warning(f"⚠️ {failed} Test Cases failed")
