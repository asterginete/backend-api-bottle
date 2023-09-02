from bottle import Bottle, request, HTTPError, response
from app.models.notification import Notification
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///notifications.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/notifications', method='GET')
@jwt_required()
def get_notifications():
    session = Session()
    try:
        user_id = get_jwt_identity()
        notifications = session.query(Notification).filter_by(user_id=user_id).all()

        return {
            "notifications": [
                {
                    "notification_id": n.notification_id,
                    "content": n.content,
                    "status": n.status,
                    "created_at": n.created_at
                } for n in notifications
            ]
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/notifications/<notification_id:int>', method='PUT')
@jwt_required()
def mark_notification_as_read(notification_id):
    session = Session()
    try:
        user_id = get_jwt_identity()
        notification = session.query(Notification).filter_by(notification_id=notification_id, user_id=user_id).first()
        if not notification:
            raise HTTPError(404, "Notification not found")

        notification.status = "Read"
        session.commit()

        return {"message": "Notification marked as read!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/notifications/<notification_id:int>', method='DELETE')
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

# Additional notification routes like marking all as read, etc. can be added here.
