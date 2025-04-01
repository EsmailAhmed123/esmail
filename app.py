from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esmaildata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class ClassRequest(db.Model):  # Renamed from 'Request' to avoid conflicts
    id = db.Column(db.Integer, primary_key=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id', ondelete='CASCADE'), nullable=False)
    unit_name = db.Column(db.String(100), nullable=False)
    student_count = db.Column(db.Integer, nullable=False)
    room_available = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='Pending')

# Routes
@app.route('/request/create', methods=['POST'])
def create_request():
    data = request.json
    required_fields = ['lecturer_id', 'unit_name', 'student_count', 'room_available']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    lecturer = Lecturer.query.get(data['lecturer_id'])
    if not lecturer:
        return jsonify({"error": "Lecturer not found"}), 404

    new_request = ClassRequest(
        lecturer_id=data['lecturer_id'],
        unit_name=data['unit_name'],
        student_count=data['student_count'],
        room_available=data['room_available']
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Request submitted successfully"}), 201

@app.route('/request/list', methods=['GET'])
def list_requests():
    requests = ClassRequest.query.all()
    result = [
        {"id": req.id, "unit_name": req.unit_name, "students": req.student_count, "room": req.room_available, "status": req.status}
        for req in requests
    ]
    return jsonify(result)

@app.route('/request/approve/<int:id>', methods=['PATCH'])
def approve_request(id):
    req = ClassRequest.query.get(id)
    if not req:
        return jsonify({"message": "Request not found"}), 404
    req.status = 'Approved'
    db.session.commit()
    return jsonify({"message": "Request approved"})

@app.route('/request/reject/<int:id>', methods=['PATCH'])
def reject_request(id):
    req = ClassRequest.query.get(id)
    if not req:
        return jsonify({"message": "Request not found"}), 404
    req.status = 'Rejected'
    db.session.commit()
    return jsonify({"message": "Request rejected"})

if __name__ == '__main__':
    app.run(debug=True)
