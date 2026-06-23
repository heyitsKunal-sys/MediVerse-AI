# Phase_1
# Step-1: Setup the GROQ API key 
from dotenv import load_dotenv
load_dotenv()

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
print("GROQ_API_KEY =", GROQ_API_KEY)

# Step-2: Coverting the  Image into required format
import base64 

import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# Step-3: Setup Multimodal LLM
from groq import Groq

query="Is there something wrong with my face?"
def analyze_image_with_query(query, model, encoded_image):
    client=Groq(
        api_key=GROQ_API_KEY
    ) 
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content



