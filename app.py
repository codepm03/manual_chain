import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supply_chain_agent import SupplyChainAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the agent
agent = SupplyChainAgent()

# Webhook verification endpoint
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Facebook webhook verification
        verify_token = os.getenv("VERIFY_TOKEN")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == verify_token:
                return challenge, 200
            else:
                return "Verification token mismatch", 403
        return "Invalid request", 400

    elif request.method == "POST":
        data = request.get_json()
        if data and "entry" in data and data["entry"]:
            changes = data["entry"][0].get("changes")
            if changes and changes[0].get("value"):
                messages = changes[0]["value"].get("messages")
                if messages and messages[0].get("text"):
                    incoming_msg = messages[0]["text"].get("body")
                    if incoming_msg:
                        response = agent.process_query(incoming_msg)
                        return jsonify({"response": response}), 200
        return "Invalid request", 400

if __name__ == "__main__":
    app.run(debug=True)
