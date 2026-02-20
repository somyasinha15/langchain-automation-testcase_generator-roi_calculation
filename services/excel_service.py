from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from utils.helpers import money
import streamlit as st

def show_dashboard_and_download(estimation_rows, test_cases_rows, what_if_multiplier):
    """
    Display executive dashboard, ROI charts, test cases,
    and provide Excel download.
    """

    roi_df = pd.DataFrame(estimation_rows)
    tc_df = pd.DataFrame(test_cases_rows)

    # Add What-If ROI
    roi_df["what_if_automation_cost"] = roi_df["automation_testing_cost"] * what_if_multiplier
    roi_df["what_if_roi"] = (
        (roi_df["manual_testing_cost"] - roi_df["what_if_automation_cost"])
        / roi_df["what_if_automation_cost"]
    ) * 100

    # Automation recommendation
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
    # Executive Metrics
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
    # ROI Charts
    # -----------------------------
    st.subheader("📌 ROI by User Story")

    # Create labels: US-1, US-2, US-3, ...
    us_labels = [f"US-{i+1}" for i in range(len(roi_df))]

    fig, ax = plt.subplots()
    ax.bar(us_labels, roi_df["roi_percentage"])

    ax.set_ylabel("ROI %")
    ax.set_xlabel("User Stories")

    st.pyplot(fig)


    st.subheader("🔮 What-If ROI (Cost Risk Simulation)")

    # Create labels: US-1, US-2, US-3, ...
    us_labels = [f"US-{i+1}" for i in range(len(roi_df))]

    fig, ax = plt.subplots()
    ax.bar(us_labels, roi_df["what_if_roi"])

    ax.set_ylabel("ROI %")
    ax.set_xlabel("User Stories")

    st.pyplot(fig)


    # -----------------------------
    # AI Explainability
    # -----------------------------
    st.subheader("🧠 AI Estimation Reasoning")
    for _, row in roi_df.iterrows():
        st.info(f"**{row['User Story']}** → {row['estimation_reasoning']}")

    # -----------------------------
    # Suitability & Confidence
    # -----------------------------
    st.subheader("🤖 Automation Suitability & Confidence")
    for _, row in roi_df.iterrows():
        st.write(row["User Story"])
        st.progress(row["automation_suitability_score"])
        st.caption(f"Confidence: {int(row['estimation_confidence'])}%")

    # -----------------------------
    # Automation Decision Table
    # -----------------------------
    st.subheader("✅ Automation Decision Matrix")
    st.dataframe(
        roi_df[["User Story", "roi_percentage",
                "automation_suitability_score",
                "automation_recommended"]]
    )

    # -----------------------------
    # Test Cases
    # -----------------------------
    st.subheader("🧪 Generated Test Cases")
    st.dataframe(tc_df)

    # -----------------------------
    # Excel Export
    # -----------------------------
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        roi_df.to_excel(writer, sheet_name="ROI_Details", index=False)
        tc_df.to_excel(writer, sheet_name="Test_Cases", index=False)
        roi_df[["User Story", "roi_percentage",
                "automation_suitability_score",
                "automation_recommended"]].to_excel(writer, sheet_name="Automation_Decisions", index=False)

        # ROI Summary sheet
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
