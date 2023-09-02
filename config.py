import os

class Config:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')  # Ideally, this should be set from environment variables
    DEBUG = False

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')  # Defaulting to SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Config
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Image Upload Config
    UPLOADED_PHOTOS_DEST = os.path.join('static', 'uploads')
