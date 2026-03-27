import json
import requests
import time

conversation = []

def chat(user_input):
    # add user message
    conversation.append({
        "role": "user",
        "content": user_input
    })

    res = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": conversation,
            "stream": True
        },
        stream=True
    )

    full_response = ""

    print("\nBot: ", end="", flush=True)

    for line in res.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))

            message = data.get("message", {})
            chunk = message.get("content")

            if chunk:
                print(chunk, end="", flush=True)
                full_response += chunk

    print()

    # add assistant response to memory
    conversation.append({
        "role": "assistant",
        "content": full_response
    })

    return full_response


while True:
    user_input = input("You: ")

    start = time.time()
    reply = chat(user_input)
    end = time.time()

    print(f"(took {end - start:.2f}s)")