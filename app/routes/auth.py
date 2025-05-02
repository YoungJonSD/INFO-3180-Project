from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw,
                name=data['name'], email=data['email'], photo=data.get('photo'))
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify(message="Invalid credentials"), 401

@bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify(message="Logout successful"), 200
