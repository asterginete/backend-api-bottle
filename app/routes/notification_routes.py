from bottle import Bottle, request, HTTPError, response
from app.models import Notification
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/', method='GET')
@jwt_required()
def get_all_notifications():
    session = Session()
    try:
        user_id = get_jwt_identity()
        notifications = session.query(Notification).filter_by(user_id=user_id).all()
        return {
            "notifications": [
                {
                    "notification_id": notification.notification_id,
                    "text": notification.text,
                    "is_read": notification.is_read
                } for notification in notifications
            ]
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<notification_id:int>/read', method='PUT')
@jwt_required()
def mark_notification_as_read(notification_id):
    session = Session()
    try:
        user_id = get_jwt_identity()
        notification = session.query(Notification).filter_by(notification_id=notification_id, user_id=user_id).first()
        if not notification:
            raise HTTPError(404, "Notification not found")

        notification.is_read = True
        session.commit()

        return {"message": "Notification marked as read!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<notification_id:int>', method='DELETE')
@jwt_required()
def delete_notification(notification_id):
    session = Session()
    try:
        user_id = get_jwt_identity()
        notification = session.query(Notification).filter_by(notification_id=notification_id, user_id=user_id).first()
        if not notification:
            raise HTTPError(404, "Notification not found")

        session.delete(notification)
        session.commit()

        return {"message": "Notification deleted successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()
