import jwt
from datetime import datetime, timedelta
from config import Config

def generate_token(data, expires_in=3600):
    """Generate a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_in)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """Decode a JWT token."""
    return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
