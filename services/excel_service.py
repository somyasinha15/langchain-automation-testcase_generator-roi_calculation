from io import BytesIO
from openpyxl.chart import BarChart, Reference
import pandas as pd

def generate_excel_report(roi_df, tc_df, totals):
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
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
        ws.append(["Total Manual Cost", totals["manual"]])
        ws.append(["Total Automation Cost", totals["automation"]])
        ws.append(["Net Savings", totals["savings"]])
        ws.append(["Average ROI (%)", totals["avg_roi"]])

        chart = BarChart()
        chart.title = "Manual vs Automation Cost"
        chart.y_axis.title = "Cost"

        data = Reference(ws, min_col=2, min_row=2, max_row=3)
        cats = Reference(ws, min_col=1, min_row=2, max_row=3)

        chart.add_data(data)
        chart.set_categories(cats)
        ws.add_chart(chart, "E2")

    buffer.seek(0)
    return buffer
