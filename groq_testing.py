from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GROQ_API_KEY")

print("KEY:", key[:15] + "..." if key else None)

client = Groq(api_key=key)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    print(e)