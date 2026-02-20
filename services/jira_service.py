import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_ISSUE_TYPE = os.getenv("JIRA_ISSUE_TYPE", "Task")

def to_adf(text: str):
    """
    Convert plain text to Atlassian Document Format (ADF)
    """
    if not text:
        text = ""

    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": line
                    }
                ]
            }
            for line in text.split("\n") if line.strip()
        ]
    }


def create_test_case(tc: dict):

    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    steps = "\n".join([f"- {s}" for s in tc.get("Steps", [])])

    description_text = f"""
Description:
{tc.get("Description")}

Preconditions:
{tc.get("Preconditions")}

Steps:
{steps}

Expected Result:
{tc.get("Expected Result")}

Priority:
{tc.get("Priority")}
"""

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": tc.get("Title"),
            "description": to_adf(description_text),  # 🔥 KEY FIX
            "issuetype": {"name": JIRA_ISSUE_TYPE},
            "labels": ["AI_Generated", "QA_Automation"]
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=auth
    )

    if response.status_code not in (200, 201):
        raise Exception(response.text)

    return response.json()
