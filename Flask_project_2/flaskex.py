from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to Flask!"

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        data = request.json  # Extract JSON from request body
        return jsonify({"received_data": data})  # Return JSON response

    return jsonify({"message": "Hello, JSON!"})  # Response for GET requests

if __name__ == "__main__":
    app.run(debug=True)