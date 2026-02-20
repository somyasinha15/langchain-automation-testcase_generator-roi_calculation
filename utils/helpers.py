# agents/helpers.py
import json
import re
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# -----------------------------
# JSON CLEANER
# -----------------------------
def clean_json(raw):
    """
    Converts raw output from LangChain into a Python object.
    Handles strings, AIMessage objects, and JSON fences (```json).
    """
    # If it's an AIMessage, get the content
    if isinstance(raw, AIMessage):
        raw_text = raw.content
    else:
        raw_text = str(raw)

    # Remove ```json or ``` fences
    raw_text = re.sub(r"```json|```", "", raw_text).strip()

    # Convert to Python object
    return json.loads(raw_text)

# -----------------------------
# MONEY FORMATTING
# -----------------------------
def money(value):
    """
    Formats a float as a USD currency string.
    """
    return f"${value:,.2f}"

# -----------------------------
# AUTOMATION SUITABILITY SCORE
# -----------------------------
def calc_suitability(estimation):
    """
    Calculates a simple automation suitability score (0-100) 
    based on dev time and maintenance time.
    """
    score = 100 - (
        estimation.get("automation_dev_time_per_test_hrs", 0) * 10 +
        estimation.get("automation_maintenance_time_per_cycle_hrs", 0) * 15
    )
    return max(0, min(100, round(score)))

# -----------------------------
# FILE LOADER
# -----------------------------
def load_txt(path):
    """
    Reads a text file and returns its content as string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
