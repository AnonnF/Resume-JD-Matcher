import os

from dotenv import load_dotenv
from openai import APIError, AuthenticationError, RateLimitError, OpenAI

from prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv() # reads .env in project root

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"

class LLMError(Exception):
    """Raised when the DeepSeek API call fails."""

class MissingAPIKeyError(Exception):
    """Raised when DEEPSEEK_API_KEY is missing or still the placeholder."""

def get_api_key() -> str | None:
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        key = st.secrets.get("DEEPSEEK_API_KEY", None)
        if key and key.strip() != "" and key != "your_api_key_here":
            return key
    except (ImportError, AttributeError):
        pass

    # Fall back to environment variable (for local dev with .env)
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key or key.strip() == "" or key == "your_api_key_here":
        return None
    return key

def generate_match_report(resume_text: str, job_description: str) -> str:
    api_key = get_api_key()
    if not api_key:
        raise MissingAPIKeyError(
            "DEEPSEEK_API_KEY is not set. Set it in .env (local) or Streamlit Cloud Secrets."
        )
    
    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(resume_text, job_description),}
            ],
            temperature=0.3,
            max_tokens=8192,
            extra_body={"thinking": {"type": "disabled"}}
        )
    except AuthenticationError as e:
        raise LLMError("Invalid API key. Check DEEPSEEK_API_KEY in your .env file.") from e
    except RateLimitError as e:
        raise LLMError("Rate limit exceeded. Please try again in a few minutes.") from e
    except APIError as e:
        raise LLMError(f"Analysis failed: {e.message}") from e
    
    content = response.choices[0].message.content
    if not content:
        raise LLMError("The model returned an empty response. Please try again.")
    
    return content
