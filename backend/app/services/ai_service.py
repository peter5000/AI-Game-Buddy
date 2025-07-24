import os
from openai import AzureOpenAI
from app.config import settings
import logging

logger = logging.getLogger("CosmosService")

def test(prompt="I am going to Paris, what should I see?"):
    endpoint = settings.OPENAI_ENDPOINT
    model_name = "gpt-4o"
    deployment = "gpt-4o"

    subscription_key = settings.OPENAI_API_KEY
    api_version = "2024-12-01-preview"

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an unhelpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=1024,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )

    logger.info(response)
