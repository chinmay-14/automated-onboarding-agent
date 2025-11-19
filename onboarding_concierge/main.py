# File: main.py
import json
from parser import parse_user_request
from agent import app

print("--- PROGRAM STARTED ---") # I added this to debug

if __name__ == "__main__":
    print("\n🤖 AI CONCIERGE IS READY")
    print("Type something like: 'Onboard Alice (alice@test.com) who is a Python Dev'")
    
    user_input = input("\n> Your Request: ")

    print("\n🧠 Gemini is processing...")
    
    # This calls the function in parser.py
    json_str = parse_user_request(user_input)
    
    # This converts text to data
    data = json.loads(json_str)
    print(f"📝 Extracted Data: {data}\n")

    print("🚀 Agent Starting Workflow...")
    initial_state = {"details": data, "logs": []}
    
    # This runs the agent
    result = app.invoke(initial_state)

    print("\n--- FINAL RESULTS ---")
    for log in result['logs']:
        print(log)
    print("---------------------")