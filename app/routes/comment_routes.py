from bottle import Bottle, request, HTTPError, response
from app.models.comment import Comment
from app.models.item import Item
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///comments.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/items/<item_id:int>/comments', method='POST')
@jwt_required()
def create_comment(item_id):
    session = Session()
    try:
        data = request.json
        content = data['content']

        # Check if item exists
        item = session.query(Item).filter_by(item_id=item_id).first()
        if not item:
            raise HTTPError(400, "Invalid item ID")

        # Create new comment
        new_comment = Comment(item_id=item_id, user_id=get_jwt_identity(), content=content)
        session.add(new_comment)
        session.commit()

        return {"message": "Comment added successfully!", "comment_id": new_comment.comment_id}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/comments/<comment_id:int>', method='GET')
def get_comment(comment_id):
    session = Session()
    try:
        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPError(404, "Comment not found")

        return {
            "comment_id": comment.comment_id,
            "item_id": comment.item_id,
            "user_id": comment.user_id,
            "content": comment.content,
            "created_at": comment.created_at
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/comments/<comment_id:int>', method='PUT')
@jwt_required()
def update_comment(comment_id):
    session = Session()
    try:
        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPError(404, "Comment not found")

        # Ensure the user is the author of the comment
        if comment.user_id != get_jwt_identity():
            raise HTTPError(403, "You are not authorized to edit this comment")

        data = request.json
        comment.content = data.get('content', comment.content)

        session.commit()

        return {"message": "Comment updated successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/comments/<comment_id:int>', method='DELETE')
@jwt_required()
def delete_comment(comment_id):
    session = Session()
    try:
        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPError(404, "Comment not found")

        # Ensure the user is the author of the comment
        if comment.user_id != get_jwt_identity():
            raise HTTPError(403, "You are not authorized to delete this comment")

        session.delete(comment)
        session.commit()

        return {"message": "Comment deleted successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

# Additional comment routes like listing all comments for an item, etc. can be added here.
