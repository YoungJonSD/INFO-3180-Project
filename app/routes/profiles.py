from flask import Blueprint, request, jsonify
from app.models import Profile, Favourite, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_

bp = Blueprint('profiles', __name__, url_prefix='/api')

@bp.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([p.__dict__ for p in profiles])

@bp.route('/profiles', methods=['POST'])
@jwt_required()
def add_profile():
    data = request.get_json()
    user_id = get_jwt_identity()
    profile = Profile(user_id_fk=user_id, **data)
    db.session.add(profile)
    db.session.commit()
    return jsonify(message="Profile added"), 201

@bp.route('/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify(profile.__dict__)

@bp.route('/profiles/<int:user_id>/favourite', methods=['POST'])
@jwt_required()
def favourite_profile(user_id):
    current_user = get_jwt_identity()
    fav = Favourite(user_id_fk=current_user, fav_user_id_fk=user_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(message="User favourited"), 201

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_profiles():
    args = request.args
    filters = []
    if 'name' in args:
        filters.append(User.name.ilike(f"%{args['name']}%"))
    if 'birth_year' in args:
        filters.append(Profile.birth_year == int(args['birth_year']))
    if 'sex' in args:
        filters.append(Profile.sex == args['sex'])
    if 'race' in args:
        filters.append(Profile.race == args['race'])

    matches = Profile.query.join(User).filter(*filters).all()
    current_user = get_jwt_identity()
    result = [m.__dict__ for m in matches if m.user_id_fk != current_user]
    return jsonify(result)

@bp.route('/api/profiles/<int:profile_id>/matches', methods=['GET'])
@jwt_required()
def get_matches(profile_id):
    selected = Profile.query.get(profile_id)
    if not selected:
        return jsonify(message='Profile not found'), 404

    # Get all other profiles (exclude same user)
    candidates = Profile.query.filter(Profile.user_id_fk != selected.user_id_fk).all()

    matches = []
    for p in candidates:
        # 1. Age within 5 years
        age_diff = abs(p.birth_year - selected.birth_year)
        if age_diff > 5:
            continue

        # 2. Height between 3 and 10 inches apart
        height_diff = abs(p.height - selected.height)
        if height_diff < 3 or height_diff > 10:
            continue

        # 3. Count how many of the 6 match fields are equal
        match_fields = [
            p.fav_cuisine == selected.fav_cuisine,
            p.fav_colour == selected.fav_colour,
            p.fav_school_sibject == selected.fav_school_sibject,
            p.political == selected.political,
            p.religious == selected.religious,
            p.family_oriented == selected.family_oriented
        ]
        if sum(match_fields) < 3:
            continue

        matches.append(p)

    # Convert matched profiles to dictionaries
    result = []
    for m in matches:
        result.append({
            'id': m.id,
            'description': m.description,
            'biography': m.biography,
            'photo': m.photo,
            'parish': m.parish,
            'sex': m.sex,
            'birth_year': m.birth_year,
            'race': m.race,
            'height': m.height
        })

    return jsonify(result), 200