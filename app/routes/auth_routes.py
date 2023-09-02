from bottle import Bottle, request, HTTPError, response
from app.models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import create_access_token
import bcrypt

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/register', method='POST')
def register():
    session = Session()
    try:
        data = request.json
        username = data['username']
        email = data['email']
        plaintext_password = data['password']

        # Check if user already exists
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            raise HTTPError(400, "Username already exists")

        # Hash the password
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())

        # Create new user
        new_user = User(username=username, email=email, _password=hashed_password.decode('utf-8'))
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
        plaintext_password = data['password']

        user = session.query(User).filter_by(username=username).first()
        if not user:
            raise HTTPError(401, "Invalid username or password")

        # Verify password
        if not bcrypt.checkpw(plaintext_password.encode('utf-8'), user._password.encode('utf-8')):
            raise HTTPError(401, "Invalid username or password")

        # Create JWT token
        access_token = create_access_token(identity=username)
        response.set_cookie("access_token", access_token, httponly=True)

        return {"message": "Logged in successfully!", "access_token": access_token}
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

# Additional auth routes like logout, password reset, etc. can be added here.
