from bottle import run
from app.routes import app  # Import the Bottle app instance from the routes module

if __name__ == '__main__':
    run(app, host='localhost', port=8080)
