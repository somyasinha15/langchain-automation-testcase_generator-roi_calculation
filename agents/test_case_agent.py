# agents/test_case_agent.py
import json
import re
from utils.helpers import clean_json

# -----------------------------
# PROMPT DEFINITION
# -----------------------------
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

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

# -----------------------------
# FUNCTIONS
# -----------------------------
def run_test_case_gen(model, tc_standards, user_story):
    """
    Runs the Test Case Generation LLM and returns a JSON array of test cases.
    Handles AIMessage outputs from LangChain.
    """

    # Invoke LLM
    raw = (tc_prompt | model | parser).invoke({
        "tc_standards": tc_standards,
        "user_story": user_story
    })

    # Convert AIMessage or string into Python object
    return clean_json(raw)

