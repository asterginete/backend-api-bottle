from bottle import Bottle, request, HTTPError, response
from app.models import Item, Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/', method='GET')
def get_all_items():
    session = Session()
    try:
        items = session.query(Item).all()
        return {
            "items": [
                {
                    "item_id": item.item_id,
                    "name": item.name,
                    "description": item.description,
                    "category_id": item.category_id
                } for item in items
            ]
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<item_id:int>', method='GET')
def get_single_item(item_id):
    session = Session()
    try:
        item = session.query(Item).filter_by(item_id=item_id).first()
        if not item:
            raise HTTPError(404, "Item not found")

        return {
            "item_id": item.item_id,
            "name": item.name,
            "description": item.description,
            "category_id": item.category_id
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/', method='POST')
@jwt_required()
def create_item():
    session = Session()
    try:
        data = request.json
        new_item = Item(
            name=data['name'],
            description=data['description'],
            category_id=data['category_id']
        )
        session.add(new_item)
        session.commit()

        return {"message": "Item created successfully!", "item_id": new_item.item_id}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<item_id:int>', method='PUT')
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

@app.route('/<item_id:int>', method='DELETE')
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
