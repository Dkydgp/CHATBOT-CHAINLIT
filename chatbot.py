"""
Chainlit + OpenRouter Chatbot
Follows PEP 8 guidelines for clean, readable Python code.
"""

import os
import traceback
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI


# ------------------------------
# Environment Setup
# ------------------------------
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


# ------------------------------
# Chatbot Logic
# ------------------------------
@cl.on_chat_start
async def start_chat() -> None:
    """
    Triggered when the chat starts.
    Sends a welcome message to the user.
    """
    await cl.Message(
        content="👋 Hello! I'm your AI Q&A assistant. Ask me anything!"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message) -> None:
    """
    Triggered when the user sends a message.
    Handles user input and sends a response.
    """
    try:
        print(f"📩 User asked: {message.content}")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant who answers clearly and politely."
                },
                {"role": "user", "content": message.content},
            ],
        )

        reply = completion.choices[0].message.content
        print(f"✅ Reply: {reply}")

        await cl.Message(content=reply).send()

    except Exception as error:
        traceback.print_exc()
        await cl.Message(content=f"⚠️ Error: {str(error)}").send()
