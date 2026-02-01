from langchain.tools import tool

@tool
def calculate_automation_testing_roi(
    total_test_cases: int,
    manual_execution_time_per_test_hrs: float,
    manual_cost_per_hour: float,
    automation_dev_time_per_test_hrs: float,
    automation_cost_per_hour: float,
    automation_maintenance_time_per_cycle_hrs: float,
    number_of_test_cycles: int,
    tool_license_cost: float
) -> dict:
    """
    LangChain Tool:
    Calculates Automation Testing ROI, cost savings, and break-even cycles.
    """

    # -----------------------------
    # Manual testing cost
    # -----------------------------
    manual_testing_cost = (
        total_test_cases
        * manual_execution_time_per_test_hrs
        * manual_cost_per_hour
        * number_of_test_cycles
    )

    # -----------------------------
    # Automation costs
    # -----------------------------
    automation_development_cost = (
        total_test_cases
        * automation_dev_time_per_test_hrs
        * automation_cost_per_hour
    )

    automation_maintenance_cost = (
        automation_maintenance_time_per_cycle_hrs
        * automation_cost_per_hour
        * number_of_test_cycles
    )

    automation_testing_cost = (
        automation_development_cost
        + automation_maintenance_cost
        + tool_license_cost
    )

    # -----------------------------
    # ROI
    # -----------------------------
    roi_percentage = (
        (manual_testing_cost - automation_testing_cost)
        / automation_testing_cost
    ) * 100

    # -----------------------------
    # Break-even cycles
    # -----------------------------
    per_cycle_manual_cost = manual_testing_cost / number_of_test_cycles

    break_even_cycles = (
        automation_development_cost / per_cycle_manual_cost
        if per_cycle_manual_cost > 0 else 0
    )

    # -----------------------------
    # Return contract (DO NOT CHANGE)
    # -----------------------------
    return {
        "manual_testing_cost": round(manual_testing_cost, 2),
        "automation_testing_cost": round(automation_testing_cost, 2),
        "roi_percentage": round(roi_percentage, 2),
        "break_even_cycles": round(break_even_cycles, 1)
    }
