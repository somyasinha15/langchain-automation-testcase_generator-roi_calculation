from tools.roi_tool import calculate_automation_testing_roi

def calculate_roi(estimation):
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
    return roi

def add_what_if(estimation, multiplier=1.0):
    estimation["what_if_automation_cost"] = estimation["automation_testing_cost"] * multiplier
    estimation["what_if_roi"] = (estimation["manual_testing_cost"] - estimation["what_if_automation_cost"]) / estimation["what_if_automation_cost"] * 100
    return estimation

def calc_suitability(est):
    score = 100 - (
        est["automation_dev_time_per_test_hrs"] * 10 +
        est["automation_maintenance_time_per_cycle_hrs"] * 15
    )
    return max(0, min(100, round(score)))

def add_decisions(roi_df):
    """Add automation recommendation and estimation confidence."""
    roi_df["automation_recommended"] = (
        (roi_df["roi_percentage"] > 0)
        & (roi_df["automation_suitability_score"] >= 60)
    )
    roi_df["estimation_confidence"] = (
        100
        - (roi_df["automation_maintenance_time_per_cycle_hrs"] * 10)
        - (roi_df["automation_dev_time_per_test_hrs"] * 5)
    ).clip(50, 95)
    return roi_df

def add_what_if(df, multiplier: float):
    """
    Adds What-If ROI based on Automation Cost multiplier.
    """
    df["what_if_automation_cost"] = df["automation_testing_cost"] * multiplier
    df["what_if_roi"] = (
        (df["manual_testing_cost"] - df["what_if_automation_cost"])
        / df["what_if_automation_cost"]
    ) * 100
    return df

