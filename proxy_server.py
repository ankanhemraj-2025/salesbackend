from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Apps Script Web App URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxStQQAbpB7-H-G-OKQvJIstiGWh7-wCKZQMVf627dNzTuW5Q6EOoGmnELmI3DJ4nT_/exec"

# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/proxy", methods=["GET", "POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        return "", 204  # Handle preflight

    try:
        if request.method == "GET":
            resp = requests.get(GOOGLE_SCRIPT_URL, params=request.args)
        elif request.method == "POST":
            resp = requests.post(GOOGLE_SCRIPT_URL, json=request.get_json())

        return (resp.text, resp.status_code, {"Content-Type": resp.headers.get("Content-Type", "application/json")})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
