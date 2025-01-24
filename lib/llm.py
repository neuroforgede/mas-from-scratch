from openai import AzureOpenAI
from dotenv import load_dotenv
from typing import Any, List, Optional
import os

load_dotenv()

open_ai_key = os.getenv("AZURE_OPENAI_API_KEY")
open_ai_model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
embedding_model = None

if open_ai_key is not None and len(open_ai_key) > 0:
    client = AzureOpenAI(
        azure_deployment=azure_deployment,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )
else:
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = AzureOpenAI(
        azure_deployment=azure_deployment,
        azure_ad_token_provider=token_provider,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

def query_llm(messages: List[Any], max_tokens: int = 300, temperature: float = 0.7) -> Optional[str]:
    response = client.chat.completions.create(
        model=open_ai_model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content