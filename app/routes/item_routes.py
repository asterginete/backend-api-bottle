from bottle import Bottle, request, HTTPError, response
from app.models.item import Item, Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///items.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/items', method='POST')
@jwt_required()
def create_item():
    session = Session()
    try:
        data = request.json
        name = data['name']
        description = data.get('description', None)
        category_id = data['category_id']

        # Check if category exists
        category = session.query(Category).filter_by(category_id=category_id).first()
        if not category:
            raise HTTPError(400, "Invalid category ID")

        # Create new item
        new_item = Item(name=name, description=description, category_id=category_id, user_id=get_jwt_identity())
        session.add(new_item)
        session.commit()

        return {"message": "Item created successfully!", "item_id": new_item.item_id}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/items/<item_id:int>', method='GET')
def get_item(item_id):
    session = Session()
    try:
        item = session.query(Item).filter_by(item_id=item_id).first()
        if not item:
            raise HTTPError(404, "Item not found")

        return {
            "item_id": item.item_id,
            "name": item.name,
            "description": item.description,
            "category_id": item.category_id,
            "created_at": item.created_at
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/items/<item_id:int>', method='PUT')
@jwt_required()
def update_item(item_id):
    session = Session()
    try:
        item = session.query(Item).filter_by(item_id=item_id).first()
        if not item:
            raise HTTPError(404, "Item not found")

        data = request.json
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.category_id = data.get('category_id', item.category_id)

        session.commit()

        return {"message": "Item updated successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/items/<item_id:int>', method='DELETE')
@jwt_required()
def delete_item(item_id):
    session = Session()
    try:
        item = session.query(Item).filter_by(item_id=item_id).first()
        if not item:
            raise HTTPError(404, "Item not found")

        session.delete(item)
        session.commit()

        return {"message": "Item deleted successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

# Additional item routes like search, filter, etc. can be added here.
