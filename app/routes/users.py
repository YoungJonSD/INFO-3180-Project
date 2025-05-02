from flask import Blueprint, jsonify
from app.models import User, Favourite
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

bp = Blueprint('users', __name__, url_prefix='/api')

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.__dict__)

@bp.route('/users/<int:user_id>/favourites', methods=['GET'])
@jwt_required()
def get_user_favourites(user_id):
    favourites = Favourite.query.filter_by(user_id_fk=user_id).all()
    result = [User.query.get(f.fav_user_id_fk).__dict__ for f in favourites]
    return jsonify(result)

@bp.route('/users/favourites/<int:N>', methods=['GET'])
@jwt_required()
def get_top_favourites(N):
    from sqlalchemy import func
    top_users = db.session.query(
        Favourite.fav_user_id_fk, func.count(Favourite.fav_user_id_fk).label("count")
    ).group_by(Favourite.fav_user_id_fk).order_by(func.count(Favourite.fav_user_id_fk).desc()).limit(N).all()

    results = []
    for uid, count in top_users:
        user = User.query.get(uid)
        data = user.__dict__
        data['fav_count'] = count
        results.append(data)

    return jsonify(results)
