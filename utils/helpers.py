import json, re

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
