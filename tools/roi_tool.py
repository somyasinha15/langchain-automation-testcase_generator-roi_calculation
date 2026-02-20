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
    tool_license_cost: float = 0.0,
    automation_execution_cost_per_cycle: float = 0.0
) -> dict:
    """
    Calculates Automation Testing ROI (%) using standard formula.
    """

    manual_testing_cost = (
        total_test_cases
        * manual_execution_time_per_test_hrs
        * manual_cost_per_hour
        * number_of_test_cycles
    )

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

    total_automation_cost = (
        automation_development_cost
        + automation_maintenance_cost
        + (automation_execution_cost_per_cycle * number_of_test_cycles)
        + tool_license_cost
    )

    roi_percentage = (
        (manual_testing_cost - total_automation_cost)
        / total_automation_cost
    ) * 100

    break_even_cycles = (
        automation_development_cost / (manual_testing_cost / number_of_test_cycles)
        if number_of_test_cycles else 0
    )

    return {
        "manual_testing_cost": round(manual_testing_cost, 2),
        "automation_testing_cost": round(total_automation_cost, 2),
        "roi_percentage": round(roi_percentage, 2),
        "break_even_cycles": round(break_even_cycles, 2)
    }
