import streamlit as st
import os, json, re
import pandas as pd
from dotenv import load_dotenv
from io import BytesIO
import matplotlib.pyplot as plt
from openpyxl.chart import BarChart, Reference

from langchain_community.document_loaders import TextLoader
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools.roi_tools import calculate_automation_testing_roi

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "estimation_rows" not in st.session_state:
    st.session_state.estimation_rows = []

if "tc_rows" not in st.session_state:
    st.session_state.tc_rows = []

# -------------------------------------------------
# ENV
# -------------------------------------------------
load_dotenv()

model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("OPENAI_ACCESS_TOKEN"),
    api_version=os.getenv("API_VERSION"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    temperature=0.2
)

# -------------------------------------------------
# LOAD STANDARDS
# -------------------------------------------------
def load_txt(path):
    loader = TextLoader(path, encoding="utf-8")
    return loader.load()[0].page_content

qa_standards = load_txt("data/qa_estimation_standards.txt")
tc_standards = load_txt("data/testing_standard.txt")

# -------------------------------------------------
# PROMPTS
# -------------------------------------------------
qa_prompt = PromptTemplate(
    template="""
You are a Principal QA Automation Architect.

Follow standards:
{qa_standards}

USER STORY:
{user_story}

Return STRICT JSON ONLY:

{{
  "total_test_cases": int,
  "manual_execution_time_per_test_hrs": float,
  "automation_dev_time_per_test_hrs": float,
  "automation_maintenance_time_per_cycle_hrs": float,
  "manual_cost_per_hour": float,
  "automation_cost_per_hour": float,
  "tooling_cost_per_year": float,
  "execution_cycles_per_year": int,
  "estimation_reasoning": "Short explanation"
}}
""",
    input_variables=["qa_standards", "user_story"]
)

tc_prompt = PromptTemplate(
    template="""
Follow testing standards:
{tc_standards}

USER STORY:
{user_story}

Return STRICT JSON ARRAY ONLY.
""",
    input_variables=["tc_standards", "user_story"]
)

parser = StrOutputParser()

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def clean_json(text):
    return json.loads(re.sub(r"```json|```", "", text).strip())

def money(v):
    return f"${v:,.2f}"

def automation_suitability(est):
    score = 100 - (
        est["automation_dev_time_per_test_hrs"] * 10 +
        est["automation_maintenance_time_per_cycle_hrs"] * 15
    )
    return max(0, min(100, round(score)))

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🚀 AI-Powered QA Cost Intelligence Platform")
st.caption(
    "Transforms user stories into test cases, automation decisions, and ROI using explainable AI."
)

stories_text = st.text_area(
    "Enter User Stories (one per line)",
    height=200
)

what_if_multiplier = st.sidebar.slider(
    "🔧 Automation Cost What-If Multiplier",
    0.5, 2.0, 1.0, 0.1
)
st.sidebar.caption(
    "Simulates automation cost risk (overruns, tooling changes, AI acceleration)."
)

# -------------------------------------------------
# GENERATE
# -------------------------------------------------
if st.button("Analyze Impact") and stories_text.strip():

    st.session_state.estimation_rows = []
    st.session_state.tc_rows = []

    stories = [s.strip() for s in stories_text.split("\n") if s.strip()]

    for story in stories:

        estimation = clean_json(
            (qa_prompt | model | parser).invoke({
                "qa_standards": qa_standards,
                "user_story": story
            })
        )

        roi = calculate_automation_testing_roi.run({
            "total_test_cases": estimation["total_test_cases"],
            "manual_execution_time_per_test_hrs": estimation["manual_execution_time_per_test_hrs"],
            "manual_cost_per_hour": estimation["manual_cost_per_hour"],
            "automation_dev_time_per_test_hrs": estimation["automation_dev_time_per_test_hrs"],
            "automation_cost_per_hour": estimation["automation_cost_per_hour"],
            "automation_maintenance_time_per_cycle_hrs": estimation["automation_maintenance_time_per_cycle_hrs"],
            "number_of_test_cycles": estimation["execution_cycles_per_year"],
            "tool_license_cost": estimation["tooling_cost_per_year"]
        })

        estimation.update(roi)
        estimation["automation_suitability_score"] = automation_suitability(estimation)
        estimation["User Story"] = story

        st.session_state.estimation_rows.append(estimation)

        for tc in clean_json(
            (tc_prompt | model | parser).invoke({
                "tc_standards": tc_standards,
                "user_story": story
            })
        ):
            tc["User Story"] = story
            st.session_state.tc_rows.append(tc)

# -------------------------------------------------
# RESULTS
# -------------------------------------------------
if st.session_state.estimation_rows:

    roi_df = pd.DataFrame(st.session_state.estimation_rows)
    tc_df = pd.DataFrame(st.session_state.tc_rows)

    # -----------------------------
    # WHAT-IF ROI
    # -----------------------------
    roi_df["what_if_automation_cost"] = (
        roi_df["automation_testing_cost"] * what_if_multiplier
    )

    roi_df["what_if_roi"] = (
        (roi_df["manual_testing_cost"] - roi_df["what_if_automation_cost"])
        / roi_df["what_if_automation_cost"]
    ) * 100

    # -----------------------------
    # DECISION + CONFIDENCE
    # -----------------------------
    roi_df["automation_recommended"] = (
        (roi_df["roi_percentage"] > 0)
        & (roi_df["automation_suitability_score"] >= 60)
    )

    roi_df["estimation_confidence"] = (
        100
        - (roi_df["automation_maintenance_time_per_cycle_hrs"] * 10)
        - (roi_df["automation_dev_time_per_test_hrs"] * 5)
    ).clip(50, 95)

    # -----------------------------
    # EXEC KPIs
    # -----------------------------
    st.markdown("## 📊 Executive Business Impact")

    total_manual = roi_df["manual_testing_cost"].sum()
    total_auto = roi_df["automation_testing_cost"].sum()
    net_savings = total_manual - total_auto
    avg_roi = roi_df["roi_percentage"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Manual Cost", money(total_manual))
    c2.metric("Automation Cost", money(total_auto))
    c3.metric("Net Savings", money(net_savings))
    c4.metric("Avg ROI", f"{avg_roi:.2f}%")

    # -----------------------------
    # CHARTS
    # -----------------------------
    st.subheader("📌 ROI by User Story")
    fig, ax = plt.subplots()
    ax.bar(roi_df["User Story"], roi_df["roi_percentage"])
    ax.set_ylabel("ROI %")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    st.subheader("🔮 What-If ROI (Cost Risk Simulation)")
    fig, ax = plt.subplots()
    ax.bar(roi_df["User Story"], roi_df["what_if_roi"])
    ax.set_ylabel("ROI %")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # -----------------------------
    # EXPLAINABILITY
    # -----------------------------
    st.subheader("🧠 AI Estimation Reasoning")
    for _, row in roi_df.iterrows():
        st.info(f"**{row['User Story']}** → {row['estimation_reasoning']}")

    # -----------------------------
    # SUITABILITY
    # -----------------------------
    st.subheader("🤖 Automation Suitability & Confidence")
    for _, row in roi_df.iterrows():
        st.write(row["User Story"])
        st.progress(row["automation_suitability_score"])
        st.caption(f"Confidence: {int(row['estimation_confidence'])}%")

    # -----------------------------
    # DECISION MATRIX
    # -----------------------------
    st.subheader("✅ Automation Decision Matrix")
    st.dataframe(
        roi_df[
            ["User Story", "roi_percentage",
             "automation_suitability_score",
             "automation_recommended"]
        ]
    )

    # -----------------------------
    # TEST CASES
    # -----------------------------
    st.subheader("🧪 Generated Test Cases")
    st.dataframe(tc_df)

    # -----------------------------
    # EXCEL EXPORT
    # -----------------------------
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:

        roi_df.to_excel(writer, sheet_name="ROI_Details", index=False)
        tc_df.to_excel(writer, sheet_name="Test_Cases", index=False)

        roi_df[
            ["User Story", "roi_percentage",
             "automation_suitability_score",
             "automation_recommended"]
        ].to_excel(writer, sheet_name="Automation_Decisions", index=False)

        wb = writer.book
        ws = wb.create_sheet("ROI_Summary")

        ws.append(["Metric", "Value"])
        ws.append(["Total Manual Cost", total_manual])
        ws.append(["Total Automation Cost", total_auto])
        ws.append(["Net Savings", net_savings])
        ws.append(["Average ROI (%)", avg_roi])

        chart = BarChart()
        chart.title = "Manual vs Automation Cost"
        chart.y_axis.title = "Cost"

        data = Reference(ws, min_col=2, min_row=2, max_row=3)
        cats = Reference(ws, min_col=1, min_row=2, max_row=3)

        chart.add_data(data)
        chart.set_categories(cats)
        ws.add_chart(chart, "E2")

    excel_buffer.seek(0)

    st.download_button(
        "📥 Download AI QA ROI Report (Excel)",
        excel_buffer,
        "AI_QA_ROI_Report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
