from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import openai
import io
import base64
import requests
import os

app = FastAPI()

# Cho phép CORS để frontend kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are a helpful assistant that generates detailed and imaginative descriptions of images for creative use."
USER_PROMPT = "Describe this image in rich, vivid, and detailed English, like a professional art critic."

@app.post("/generate-prompt")
async def generate_prompt(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": USER_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=500,
        )

        english_caption = response.choices[0].message.content

        # Dịch sang tiếng Việt bằng mô hình dịch Hugging Face
        translation = requests.post(
            "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-vi",
            headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN', '')}"},
            json={"inputs": english_caption},
        )
        vi_caption = translation.json()[0]['translation_text'] if translation.ok else ""

        return {
            "english": english_caption,
            "vietnamese": vi_caption
        }

    except Exception as e:
        return {"error": str(e)}
