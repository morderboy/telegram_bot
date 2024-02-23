import openai
import logging
import config

openai.api_key = config.get_OpenAIToken()

async def generate_text(prompt, previous_prompts=None) -> dict:
    try:
        messages = [{"role": "system", "content": msg} for msg in previous_prompts] if previous_prompts else []
        messages.append({"role": "user", "content": prompt})

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response["choices"][0]["message"]["content"], response["usage"]["total_tokens"]
    except Exception as e:
        logging.error(e)

async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            prompt=prompt,
            n=n,
            size=size
        )

        urls = []
        for item in response["data"]:
            urls.append(item["url"])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls