from app import app
from bottle import run
from config import Config
from flask_mail import Mail
from app.services.image_upload_service import photos
from flask_uploads import configure_uploads

# Configure app from the Config class
app.config.from_object(Config)

# Configure mail
mail = Mail(app)

# Configure image uploads
configure_uploads(app, photos)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
