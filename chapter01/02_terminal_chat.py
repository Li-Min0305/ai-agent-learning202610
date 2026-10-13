import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

client = OpenAI(api_key=api_key, base_url=base_url)

messages = [
    {"role" : "system", "content" : "是一位耐心幽默的 Python 编程导师。回答要简明扼要，多用生动的比喻"}
]

while True:
    user_input = input("\nUser: (Type 'exit' or 'quit' to end the chat)\n").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("Bye!")
        break

    if not user_input:
        continue

    messages.append(
        {"role" : "user", "content" : user_input}
    )

    print("\n AI", end = "", flush = True)

    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = messages,
        stream = True
    )

    full_response = ""

    for chunk in response:
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            full_response += delta_content
            print(delta_content, end="", flush=True)

    print()

    messages.append(
        {"role" : "assistant", "content" : full_response}
    )