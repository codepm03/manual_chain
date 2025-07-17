from flask import Flask, request
from supply_chain_agent import SupplyChainAgent

app = Flask(__name__)

# Initialize the agent
agent = SupplyChainAgent()

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook endpoint to receive messages, process them, and send a response.
    """
    # Get the message from the request
    incoming_msg = request.json.get("message")

    if not incoming_msg:
        return "No message received", 400

    # Process the message using the agent
    response = agent.process_query(incoming_msg)
    print(f"Agent response: {response}")

    # For now, we'll just return the response to the console.
    # In a real application, you'd send this back to the user.
    return response, 200

if __name__ == "__main__":
    app.run(debug=True)
