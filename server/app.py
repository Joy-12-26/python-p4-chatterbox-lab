from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([{
        "id": m.id,
        "body": m.body,
        "username": m.username,
        "created_at": m.created_at.isoformat(),
        "updated_at": m.updated_at.isoformat()
    } for m in messages])


@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data.get("body"),
        username=data.get("username")
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at.isoformat(),
        "updated_at": new_message.updated_at.isoformat()
    }), 201


@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if "body" in data:
        message.body = data["body"]
    db.session.commit()
    return jsonify({
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at.isoformat(),
        "updated_at": message.updated_at.isoformat()
    })


@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(port=5000, debug=True)
 