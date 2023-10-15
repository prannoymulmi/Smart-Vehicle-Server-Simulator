from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from the server! TEST"

@app.route('/data', methods=['POST'])
def receive_data():
    if not request.json:
        return jsonify({"message": "Bad Request: JSON data expected"}), 400

    data = request.json
    print(data)  # You can process or store the data as required.

    return jsonify({"message": "Data received successfully!"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)