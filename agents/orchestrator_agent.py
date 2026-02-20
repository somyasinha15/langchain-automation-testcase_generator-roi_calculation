from agents.estimation_agent import run_estimation
from agents.test_case_agent import run_test_case_gen
from services.roi_service import calculate_roi, add_what_if, add_decisions
from utils.helpers import calc_suitability


def orchestrate(model, qa_standards, tc_standards, user_story, what_if_multiplier=1.0):
    """
    Orchestrates the multi-agent flow:
    1. Estimation
    2. Test case generation
    3. ROI calculation
    4. What-If & decisions
    """

    # Step 1: QA Estimation
    estimation = run_estimation(model, qa_standards, user_story)

    # Step 2: ROI calculation
    roi_data = calculate_roi(estimation)
    estimation.update(roi_data)

    # Step 3: Automation suitability and user story
    estimation["automation_suitability_score"] = calc_suitability(estimation)
    estimation["User Story"] = user_story

    # Step 4: Test cases
    test_cases = run_test_case_gen(model, tc_standards, user_story)
    for tc in test_cases:
        tc["User Story"] = user_story

    # Step 5: What-If and decisions
    estimation = add_what_if(estimation, what_if_multiplier)

    return estimation, test_cases
