from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.helpers import clean_json

parser = StrOutputParser()

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

def generate_estimation(model, standards, story):
    return clean_json(
        (qa_prompt | model | parser).invoke({
            "qa_standards": standards,
            "user_story": story
        })
    )
