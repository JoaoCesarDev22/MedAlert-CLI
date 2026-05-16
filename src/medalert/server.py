from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "MedAlert CLI",
        "status": "online",
        "message": "Deploy ativo no Render",
        "usage": "Execute localmente com python src/medalert/app.py"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
