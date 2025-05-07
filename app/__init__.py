from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from sqlalchemy import func, desc
from dotenv import load_dotenv
from app.config import Config
from app.models import db, User, Profile, Favourite


load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    jwt = JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080", "http://localhost:5173"]}})
    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    
    @app.before_first_request
    def create_tables():
        db.create_all()

    
    @app.route('/')
    def index():
        return jsonify({
        'message': 'Welcome to Jam-Date API',
        'status': 'online',
        'version': '1.0'
    })
    
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.json
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        new_user = User(
            username=data['username'],
            name=data['name'],
            email=data['email'],
            photo=data.get('photo', '')
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201


    @app.route('/api/auth/login', methods=['POST'])
    def login():
        try:
            data = request.json
            user = User.query.filter_by(username=data['username']).first()
        
            if not user or not user.check_password(data['password']):
                return jsonify({'error': 'Invalid username or password'}), 401
        
            access_token = create_access_token(identity=user.id)
        
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        except Exception as e:
            error_message = str(e)
            print(f"Login error: {error_message}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Internal server error', 'details': error_message}), 500
        
    @app.route('/api/auth/logout', methods=['POST'])
    @jwt_required()
    def logout():
       
        return jsonify({'message': 'Logout successful'}), 200

   
   
    @app.route('/api/profiles', methods=['GET'])
    @jwt_required()
    def get_all_profiles():
        current_user_id = get_jwt_identity()
    

        include_own = request.args.get('include_own', 'false').lower() == 'true'
    
 
        print(f"Getting profiles with include_own={include_own}")
    
   
        user_profiles = Profile.query.filter_by(user_id_fk=current_user_id).all()
    
        if not user_profiles and not include_own:
            return jsonify({'error': 'You must create a profile first'}), 403
    
    
        if include_own:
            profiles = Profile.query.all()
        else:
            profiles = Profile.query.filter(Profile.user_id_fk != current_user_id).all()
    
   
        print(f"Found {len(profiles)} profiles")
        for profile in profiles:
            print(f"Profile ID: {profile.id}, User ID: {profile.user_id_fk}")
    
        return jsonify({
            'profiles': [profile.to_dict() for profile in profiles]
        }), 200

    @app.route('/api/profiles', methods=['POST'])
    @jwt_required()
    def add_profile():
        current_user_id = get_jwt_identity()
        data = request.json
       
        profile_count = Profile.query.filter_by(user_id_fk=current_user_id).count()
        if profile_count >= 3:
            return jsonify({'error': 'You can have at most 3 profiles'}), 400
        
       
        new_profile = Profile(
            user_id_fk=current_user_id,
            description=data['description'],
            parish=data['parish'],
            biography=data['biography'],
            sex=data['sex'],
            race=data['race'],
            birth_year=data['birth_year'],
            height=data['height'],
            fav_cuisine=data['fav_cuisine'],
            fav_colour=data['fav_colour'],
            fav_school_sibject=data['fav_school_sibject'],
            political=data['political'],
            religious=data['religious'],
            family_oriented=data['family_oriented']
        )
        
        db.session.add(new_profile)
        db.session.commit()
        
        return jsonify({
            'message': 'Profile added successfully',
            'profile': new_profile.to_dict()
        }), 201

   
    @app.route('/api/profiles/<int:profile_id>', methods=['GET'])
    @jwt_required()
    def get_profile(profile_id):
        profile = Profile.query.get_or_404(profile_id)
        
        return jsonify({
            'profile': profile.to_dict()
        }), 200

   
    @app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
    @jwt_required()
    def add_to_favourites(user_id):
        current_user_id = get_jwt_identity()
      
        User.query.get_or_404(user_id)
        
       
        existing = Favourite.query.filter_by(
            user_id_fk=current_user_id,
            fav_user_id_fk=user_id
        ).first()
        
        if existing:
            return jsonify({'message': 'User already in favorites'}), 200
        
      
        new_favourite = Favourite(
            user_id_fk=current_user_id,
            fav_user_id_fk=user_id
        )
        
        db.session.add(new_favourite)
        db.session.commit()
        
        return jsonify({
            'message': 'User added to favorites successfully'
        }), 201

    
    @app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
    @jwt_required()
    def get_matches(profile_id):
        current_user_id = get_jwt_identity()
        
       
        profile = Profile.query.get_or_404(profile_id)
        
        
        if profile.user_id_fk != current_user_id:
            return jsonify({'error': 'Unauthorized access to profile'}), 403
        
      
        current_year = datetime.now().year
        current_age = current_year - profile.birth_year
        min_birth_year = current_year - (current_age + 5)
        max_birth_year = current_year - (current_age - 5)
        
        
        matches_query = Profile.query.filter(
            Profile.user_id_fk != current_user_id,  
            Profile.birth_year.between(min_birth_year, max_birth_year), 
            Profile.height.between(profile.height - 10, profile.height + 10)
        ).all()
        
        
        matches = []
        for match in matches_query:
            matching_fields = 0
            
            if match.fav_cuisine == profile.fav_cuisine:
                matching_fields += 1
            if match.fav_colour == profile.fav_colour:
                matching_fields += 1
            if match.fav_school_sibject == profile.fav_school_sibject:
                matching_fields += 1
            if match.political == profile.political:
                matching_fields += 1
            if match.religious == profile.religious:
                matching_fields += 1
            if match.family_oriented == profile.family_oriented:
                matching_fields += 1
            
            if matching_fields >= 3:
                matches.append(match)
        
        return jsonify({
            'matches': [match.to_dict() for match in matches]
        }), 200

 
    @app.route('/api/search', methods=['GET'])
    @jwt_required()
    def search_profiles():
        current_user_id = get_jwt_identity()
    
 
        name = request.args.get('name', '')
        birth_year = request.args.get('birth_year', type=int)
        sex = request.args.get('sex', '')
        race = request.args.get('race', '')
        parish = request.args.get('parish', '')  
    
   
        query = Profile.query.join(User).filter(Profile.user_id_fk != current_user_id)
    
   
        if name:
         query = query.filter(User.name.like(f'%{name}%'))
        if birth_year:
            query = query.filter(Profile.birth_year == birth_year)
        if sex:
            query = query.filter(Profile.sex == sex)
        if race:
            query = query.filter(Profile.race == race)
        if parish:
            query = query.filter(Profile.parish == parish)  
    
   
        results = query.all()
    
        return jsonify({
        'results': [profile.to_dict() for profile in results]
    }), 200

  
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        
        return jsonify({
            'user': user.to_dict()
        }), 200

    
    @app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
    @jwt_required()
    def get_user_favourites(user_id):
        current_user_id = get_jwt_identity()
        
       
        if user_id != current_user_id:
          
            return jsonify({'error': 'Unauthorized'}), 403
        
       
        favourites = Favourite.query.filter_by(user_id_fk=user_id).all()
        fav_user_ids = [fav.fav_user_id_fk for fav in favourites]
        
       
        fav_users = User.query.filter(User.id.in_(fav_user_ids)).all()
        
        
        sort_by = request.args.get('sort_by', 'name')
        
        if sort_by == 'name':
            fav_users.sort(key=lambda x: x.name)
        elif sort_by == 'parish':
           
            fav_users_with_profile = []
            for user in fav_users:
                profile = Profile.query.filter_by(user_id_fk=user.id).first()
                if profile:
                    fav_users_with_profile.append((user, profile.parish))
            fav_users_with_profile.sort(key=lambda x: x[1])
            fav_users = [item[0] for item in fav_users_with_profile]
        elif sort_by == 'age':
           
            fav_users_with_age = []
            current_year = datetime.now().year
            for user in fav_users:
                profile = Profile.query.filter_by(user_id_fk=user.id).first()
                if profile:
                    age = current_year - profile.birth_year
                    fav_users_with_age.append((user, age))
            fav_users_with_age.sort(key=lambda x: x[1])
            fav_users = [item[0] for item in fav_users_with_age]
        
        return jsonify({
            'favourites': [user.to_dict() for user in fav_users]
        }), 200

    @app.route('/api/users/favourites/<int:n>', methods=['GET'])
    @jwt_required()
    def get_top_favourites(n):
        
        fav_counts = db.session.query(
            Favourite.fav_user_id_fk, 
            func.count(Favourite.id).label('count')
        ).group_by(Favourite.fav_user_id_fk).order_by(desc('count')).limit(n).all()
        
       
        top_users = []
        for user_id, count in fav_counts:
            user = User.query.get(user_id)
            if user:
                user_dict = user.to_dict()
                user_dict['fav_count'] = count
                top_users.append(user_dict)
        
       
        sort_by = request.args.get('sort_by', 'count')
        
        if sort_by == 'name':
            top_users.sort(key=lambda x: x['name'])
        elif sort_by == 'parish':
           
            users_with_parish = []
            for user in top_users:
                profile = Profile.query.filter_by(user_id_fk=user['id']).first()
                if profile:
                    user['parish'] = profile.parish
                    users_with_parish.append(user)
            users_with_parish.sort(key=lambda x: x.get('parish', ''))
            top_users = users_with_parish
        elif sort_by == 'age':
            
            users_with_age = []
            current_year = datetime.now().year
            for user in top_users:
                profile = Profile.query.filter_by(user_id_fk=user['id']).first()
                if profile:
                    age = current_year - profile.birth_year
                    user['age'] = age
                    users_with_age.append(user)
            users_with_age.sort(key=lambda x: x.get('age', 0))
            top_users = users_with_age
        
        return jsonify({
            'top_favourites': top_users
        }), 200

    return app


