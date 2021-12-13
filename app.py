from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Float, nullable=False)
    photo = db.Column(db.Float, nullable=False)

    def __init__(self, title, body,photo):
        self.title = title
        self.body = body
        self.photo = photo

class NoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "body","photo")

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


@app.route("/note/add", methods=["POST"])
def add_item():

    title = request.json.get("title")
    body = request.json.get("body")
    photo = request.json.get("photo")
    record = Note(title, body,photo)
    db.session.add(record)
    db.session.commit()

    return jsonify(note_schema.dump(record))

@app.route("/note/get", methods=["GET"])
def get_all_items():
    all_items = Note.query.all()
    return jsonify(notes_schema.dump(all_items))


if __name__ == "__main__":
    app.run(debug=True)