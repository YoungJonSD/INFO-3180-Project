# Import required modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Profile, User

# Create a blueprint
bp = Blueprint('profiles', __name__)

# GET all profiles
@bp.route('/profiles', methods=['GET'])
@jwt_required()
def get_profiles():
    try:
        # Get all profiles
        profiles = Profile.query.all()
        
        # Convert to list of dictionaries
        result = []
        for profile in profiles:
            result.append({
                'id': profile.id,
                'description': profile.description,
                'parish': profile.parish,
                # Add other fields as needed
            })
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Error retrieving profiles: {str(e)}")
        return jsonify({"message": f"Error retrieving profiles: {str(e)}"}), 500

# POST a new profile
@bp.route('/profiles', methods=['POST'])
@jwt_required()
def add_profile():
    try:
        # Get JSON data from request
        data = request.json
        
        # Get user ID from token
        user_id = get_jwt_identity()
        
        # Create and save profile
        profile = Profile(user_id_fk=user_id, **data)
        db.session.add(profile)
        db.session.commit()
        
        # Return ID with success message
        return jsonify({
            "message": "Profile added successfully",
            "id": profile.id
        }), 201
    except Exception as e:
        # Rollback on error
        db.session.rollback()
        print(f"Error creating profile: {str(e)}")
        return jsonify({"message": f"Error creating profile: {str(e)}"}), 500

# GET a specific profile
@bp.route('/profiles/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    try:
        # Find profile by ID
        profile = Profile.query.get(profile_id)
        
        # Check if profile exists
        if not profile:
            return jsonify({"message": "Profile not found"}), 404
        
        # Convert to dictionary
        result = {
            "id": profile.id,
            "description": profile.description,
            "parish": profile.parish,
            "biography": profile.biography,
            "sex": profile.sex,
            "race": profile.race,
            "birth_year": profile.birth_year,
            "height": profile.height,
            "fav_cuisine": profile.fav_cuisine,
            "fav_colour": profile.fav_colour,
            "fav_school_sibject": profile.fav_school_sibject,
            "political": profile.political,
            "religious": profile.religious,
            "family_oriented": profile.family_oriented,
            "user_id_fk": profile.user_id_fk
        }
        
        # Add photo if it exists
        if hasattr(profile, 'photo') and profile.photo:
            result["photo"] = profile.photo
            
        return jsonify(result), 200
    except Exception as e:
        print(f"Error retrieving profile: {str(e)}")
        return jsonify({"message": f"Error retrieving profile: {str(e)}"}), 500

# POST to add a profile to favourites
@bp.route('/profiles/<int:profile_id>/favourite', methods=['POST'])
@jwt_required()
def add_to_favourites(profile_id):
    try:
        # Get user ID from token
        user_id = get_jwt_identity()
        
        # Check if profile exists
        profile = Profile.query.get(profile_id)
        if not profile:
            return jsonify({"message": "Profile not found"}), 404
        
        # Check if already in favourites
        from app.models import Favourite
        existing = Favourite.query.filter_by(
            user_id_fk=user_id, 
            fav_user_id_fk=profile.user_id_fk
        ).first()
        
        if existing:
            return jsonify({"message": "Already in favourites"}), 200
        
        # Add to favourites
        favourite = Favourite(
            user_id_fk=user_id,
            fav_user_id_fk=profile.user_id_fk
        )
        db.session.add(favourite)
        db.session.commit()
        
        return jsonify({"message": "Added to favourites"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding to favourites: {str(e)}")
        return jsonify({"message": f"Error adding to favourites: {str(e)}"}), 500