import requests
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/auto-post', methods=['POST'])
def auto_post():
    data = request.get_json()
    token = data.get("token")
    channel_id = data.get("channelId")
    message = data.get("message")
    delay = data.get("delay")

    if not (token and channel_id and message and delay):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return jsonify({"success": True, "message": "Message sent successfully!"}), 200
        else:
            return jsonify({"success": False, "message": f"Failed to send message: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
