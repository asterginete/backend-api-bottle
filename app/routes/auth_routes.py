from bottle import Bottle, request, HTTPError, response
from app.models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import generate_token, decode_token
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from app.services.email_service import send_email

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# For generating secure tokens for password reset
s = URLSafeTimedSerializer('my_secret_key')  # Ideally, this should be set from environment variables or config

@app.route('/register', method='POST')
def register():
    session = Session()
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']

        # Check if username already exists
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            raise HTTPError(400, "Username already exists")

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()

        return {"message": "User registered successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/login', method='POST')
def login():
    session = Session()
    try:
        data = request.json
        username = data['username']
        password = data['password']

        user = session.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            raise HTTPError(401, "Invalid username or password")

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/request-password-reset', method='POST')
def request_password_reset():
    session = Session()
    try:
        data = request.json
        email = data['email']

        user = session.query(User).filter_by(email=email).first()
        if not user:
            raise HTTPError(404, "User not found")

        token = s.dumps(email, salt='password-reset-salt')
        reset_url = f'http://frontendurl.com/reset-password/{token}'
        send_email("Password Reset Request", [email], f"Click here to reset your password: {reset_url}")

        return {"message": "Password reset link sent to email!"}
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/reset-password/<token>', method='POST')
def reset_password(token):
    session = Session()
    try:
        data = request.json
        new_password = data['new_password']

        email = s.loads(token, salt='password-reset-salt', max_age=3600)
        user = session.query(User).filter_by(email=email).first()
        if not user:
            raise HTTPError(404, "User not found")

        hashed_password = generate_password_hash(new_password, method='sha256')
        user.password = hashed_password
        session.commit()

        return {"message": "Password reset successfully!"}
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/profile', method='GET')
@jwt_required()
def get_profile():
    session = Session()
    try:
        username = get_jwt_identity()
        user = session.query(User).filter_by(username=username).first()
        if not user:
            raise HTTPError(404, "User not found")

        return {
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/profile', method='PUT')
@jwt_required()
def update_profile():
    session = Session()
    try:
        username = get_jwt_identity()
        user = session.query(User).filter_by(username=username).first()
        if not user:
            raise HTTPError(404, "User not found")

        data = request.json
        user.email = data.get('email', user.email)  # Update email if provided

        session.commit()

        return {"message": "Profile updated successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()
