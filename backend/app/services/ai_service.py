import logging

from openai import AzureOpenAI

from app.config import settings

logger = logging.getLogger("AIService")


def model_test(prompt="I am going to Paris, what should I see?"):
    endpoint = settings.OPENAI_ENDPOINT
    # model_name = "gpt-4o"
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
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=1024,
        temperature=1.0,
        top_p=1.0,
        model=deployment,
    )

    logger.info(response)

    return response


# def thread_test(prompt):
#     project = AIProjectClient(
#     credential=DefaultAzureCredential(),
#     endpoint=settings.PROJECT_ENDPOINT)
#     logger.info(f"Initialized AIProjectClient with endpoint: {project}")

#     logger.info(f"Agents from project {project.agents}")

#     agent = project.agents.get_agent("asst_yvb2eyYu2hrDialX5YvjMbz6")

#     thread = project.agents.threads.create()
#     logger.info(f"Created thread, ID: {thread.id}")

#     message = project.agents.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content=prompt
#     )
#     logger.info(f"Created message, ID: {message}")

#     run = project.agents.runs.create_and_process(
#         thread_id=thread.id,
#         agent_id=agent.id)

#     if run.status == "failed":
#         return f"Run failed: {run.last_error}"
#     else:
#         messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
#         logger.info(f"Retrieved messages for thread {thread.id}: {messages}")
#         return messages
