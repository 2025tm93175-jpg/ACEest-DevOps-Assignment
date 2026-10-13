from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss": {
        "workout": "Full Body HIIT",
        "calories": 1800
    },
    "Muscle Gain": {
        "workout": "Push/Pull/Legs",
        "calories": 2600
    },
    "Beginner": {
        "workout": "Full Body 3x/week",
        "calories": 2000
    }
}

clients = []


@app.route("/")
def home():
    return jsonify({
        "application": "ACEest Fitness & Gym",
        "message": "Welcome to ACEest Fitness & Gym",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/api/programs")
def get_programs():
    return jsonify(PROGRAMS)


@app.route("/api/clients", methods=["GET"])
def get_clients():
    return jsonify(clients)


@app.route("/api/clients", methods=["POST"])
def add_client():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = ["name", "age", "weight", "program"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    if data["program"] not in PROGRAMS:
        return jsonify({
            "error": "Invalid fitness program"
        }), 400

    client = {
        "name": data["name"],
        "age": data["age"],
        "weight": data["weight"],
        "program": data["program"]
    }

    clients.append(client)

    return jsonify({
        "message": "Client added successfully",
        "client": client
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
