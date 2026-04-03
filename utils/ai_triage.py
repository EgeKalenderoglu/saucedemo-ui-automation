import anthropic
import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import re

load_dotenv()

def analyze_failure(test_name, exception_message, current_url, page_title, page_source):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f""" You are a QA automation expert analyzing a Selenium test failure.

Test name: {test_name}
Exception: {exception_message}
URL at failure: {current_url}
Page title: {page_title}
Page source snippet (first 2000 chars): {page_source[:2000]}
    
Analyze this failure and respond with a JSON object with these exact fields:
- failure_type: one of [locator_issue, timeout, assertion_failure, navigation_error, application_bug, environment_issue, unknown]
- confidence: one of [high, medium, low]
- likely_cause: a single sentence explaining what likely went wrong
- suggested_fix: a single sentence suggesting what to check or fix
- summary: a two sentence summary of the failure
    
Respond with only the JSON object, no other text."""

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_response = message.content[0].text
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
        else:
            raise ValueError(f"No JSON found in response: {raw_response}")
        os.makedirs("artifacts", exist_ok=True)
        ts =datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = test_name.replace("/", "_").replace("::", "__")
        output_path = f"artifacts/{safe_name}_{ts}_triage.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

        logging.info(f"AI triage complete: {output_path}")
        logging.info(f"Failure type: {analysis['failure_type']} | Confidence: {analysis.get('confidence')}")

        return analysis

    except Exception as e:
        logging.error(f"AI triage failed: {e}")
        return None