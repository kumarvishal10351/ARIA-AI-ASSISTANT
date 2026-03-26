from voice import take_voice_command
from speaker import speak
from ai_brain import generate_system_command
import subprocess

# 🚨 Safety block list
BLOCKED = ["rm", "del", "format", "shutdown", "rmdir"]

def is_safe(cmd):
    for word in BLOCKED:
        if word in cmd.lower():
            return False
    return True

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        output = result.stdout if result.stdout else result.stderr

        return output[:300]  # limit output

    except Exception as e:
        return str(e)

from voice import take_voice_command
from speaker import speak
from ai_brain import agent_decision, generate_system_command, chat_response
from rag.retriever import get_relevant_docs
import subprocess

BLOCKED = ["rm", "del", "format", "shutdown"]

def is_safe(cmd):
    for word in BLOCKED:
        if word in cmd.lower():
            return False
    return True

def execute_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout if result.stdout else result.stderr

def main():
    speak("Hello, I am your intelligent assistant")

    while True:
        user_input = take_voice_command()

        if user_input == "":
            speak("I did not catch that")
            continue

        decision = agent_decision(user_input)
        print("Decision:", decision)

        # 💻 COMMAND
        if decision == "COMMAND":
            cmd = generate_system_command(user_input)
            print("Command:", cmd)

            if not is_safe(cmd):
                speak("Command blocked for safety")
                continue

            speak("Executing")
            output = execute_command(cmd)
            print(output)
            speak("Done")

        # 📚 QUESTION (RAG)
        elif decision == "QUESTION":
            docs = get_relevant_docs(user_input)
            context = "\n".join([doc.page_content for doc in docs])

            response = chat_response(context + "\n\nQuestion: " + user_input)
            speak(response)

        # 💬 CHAT
        else:
            response = chat_response(user_input)
            speak(response)

if __name__ == "__main__":
    main()