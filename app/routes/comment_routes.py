from bottle import Bottle, request, HTTPError, response
from app.models import Comment, Item
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/item/<item_id:int>', method='GET')
def get_comments_for_item(item_id):
    session = Session()
    try:
        comments = session.query(Comment).filter_by(item_id=item_id).all()
        return {
            "comments": [
                {
                    "comment_id": comment.comment_id,
                    "text": comment.text,
                    "user_id": comment.user_id,
                    "item_id": comment.item_id
                } for comment in comments
            ]
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/', method='POST')
@jwt_required()
def create_comment():
    session = Session()
    try:
        data = request.json
        user_id = get_jwt_identity()
        new_comment = Comment(
            text=data['text'],
            user_id=user_id,
            item_id=data['item_id']
        )
        session.add(new_comment)
        session.commit()

        return {"message": "Comment added successfully!", "comment_id": new_comment.comment_id}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<comment_id:int>', method='PUT')
@jwt_required()
def update_comment(comment_id):
    session = Session()
    try:
        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPError(404, "Comment not found")

        user_id = get_jwt_identity()
        if comment.user_id != user_id:
            raise HTTPError(403, "Not authorized to edit this comment")

        data = request.json
        comment.text = data.get('text', comment.text)

        session.commit()

        return {"message": "Comment updated successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<comment_id:int>', method='DELETE')
@jwt_required()
def delete_comment(comment_id):
    session = Session()
    try:
        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPError(404, "Comment not found")

        user_id = get_jwt_identity()
        if comment.user_id != user_id:
            raise HTTPError(403, "Not authorized to delete this comment")

        session.delete(comment)
        session.commit()

        return {"message": "Comment deleted successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()
