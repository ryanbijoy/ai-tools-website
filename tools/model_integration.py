import openai
from openai import OpenAI
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=openai.api_key)


def assistant_api(assistant, user_message):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    run_response = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant
    )
    run = run_response

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run_status.status in ["completed", "failed"]:
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = messages[0].content[0].text.value

    return messages[-1]['content']

