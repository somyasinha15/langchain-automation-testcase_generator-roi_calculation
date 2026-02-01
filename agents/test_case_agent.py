from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.helpers import clean_json

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

def generate_test_cases(model, standards, story):
    return clean_json(
        (tc_prompt | model | parser).invoke({
            "tc_standards": standards,
            "user_story": story
        })
    )
