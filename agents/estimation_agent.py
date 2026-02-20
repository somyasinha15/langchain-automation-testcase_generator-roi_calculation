from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from utils.helpers import clean_json

# -----------------------------
# Load QA standards
# -----------------------------
def load_txt(path):
    loader = TextLoader(path, encoding="utf-8")
    return loader.load()[0].page_content

qa_standards = load_txt("data/qa_estimation_standards.txt")

# -----------------------------
# QA Prompt Template
# -----------------------------
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

parser = StrOutputParser()

# -----------------------------
# Run Estimation Agent
# -----------------------------
def run_estimation(model, qa_standards, user_story):
    """
    Calls LangChain model to generate QA estimation for a user story.
    Returns Python dict after cleaning AIMessage output.
    """
    raw_output = (qa_prompt | model | parser).invoke({
        "qa_standards": qa_standards,
        "user_story": user_story
    })

    estimation = clean_json(raw_output)
    return estimation
