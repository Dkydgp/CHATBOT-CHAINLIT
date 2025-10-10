"""
Chainlit + OpenRouter Chatbot
Custom UI: Sky blue background, black avatar
"""

import os
import traceback
import chainlit as cl
from dotenv import load_dotenv
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
    api_key=API_KEY
)

# ------------------------------
# UI Customization
# ------------------------------
cl.UIConfig(
    theme={
        "background": "#87CEEB",  # Sky blue
        "primary": "#4b0082",     # Buttons / accents
        "secondary": "#ff69b4"    # Highlights
    }
)

# ------------------------------
# Chatbot Logic
# ------------------------------
@cl.on_chat_start
async def start_chat() -> None:
    """
    Triggered when the chat starts.
    Sends a welcome message with black avatar.
    """
    await cl.Message(
        content="👋 Hello! Welcome to your AI chatbot. Ask me anything!",
        avatar="⚫"  # Black avatar
    ).send()

    # Optional: send a button
    await cl.Button(
        text="Say Hello",
        action={"type": "message", "value": "Hello!"}
    ).send()

    # Optional: send an image
    await cl.Message(
        content="Here’s a friendly sky image 🌤️",
        image="https://i.imgur.com/9bK0V6T.jpg"
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

        await cl.Message(content=reply, avatar="⚫").send()

    except Exception as error:
        traceback.print_exc()
        await cl.Message(content=f"⚠️ Error: {str(error)}", avatar="⚫").send()
