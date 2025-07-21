from google import genai
from dotenv import load_dotenv
import os
import requests
from fastapi import FastAPI

app = FastAPI()


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key)


async def get_affirmation() -> str:
    response = await client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Generate a daily motivational affirmation that inspires someone to pursue a career in the UK tech industry by learning Python, machine learning, AI, and DevOps. The affirmation should be encouraging, positive, and focused on skill growth and career success.(write in short not more than 30-40 words)",
    )
    return response.text


token = os.getenv("VOICEMONKEY_TOKEN")


@app.get("/affirmation")
async def affirmation():
    response = await get_affirmation()
    try:
        r = requests.get(
            f"https://api-v2.voicemonkey.io/announcement?token={token}&device=echo-dot&text={response.text}"
        )
        print(r.status_code)
    except Exception as e:
        print(f"An error occurred: {e}")
