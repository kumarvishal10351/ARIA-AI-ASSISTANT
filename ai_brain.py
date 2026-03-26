import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")


# 🧠 Decide intent
def agent_decision(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"

    prompt = f"""
    Classify user input into:
    COMMAND (system control)
    QUESTION (document/data related)
    CHAT (general)

    Return ONLY one word.

    User: {user_input}
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()["choices"][0]["message"]["content"].strip()


# ⚙️ Generate command
def generate_system_command(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"

    prompt = f"""
    Convert to Windows command.

    Only return command. No formatting.

    User: {user_input}
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    cmd = response.json()["choices"][0]["message"]["content"].strip()

    # Clean output
    cmd = cmd.replace("```", "").replace("cmd", "").replace("bash", "").strip()
    cmd = cmd.split("\n")[0]

    return cmd


# 💬 Chat with memory
def chat_response(user_input, history=None):
    url = "https://api.mistral.ai/v1/chat/completions"

    messages = []

    if history:
        for msg in history[-6:]:
            role = "assistant" if msg["role"] == "assistant" else "user"
            messages.append({"role": role, "content": msg["content"]})

    messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small-latest",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()["choices"][0]["message"]["content"]