from bottle import Bottle, request, HTTPError, response
from app.models import Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Bottle()

# Assuming you're using SQLite for this example
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/', method='GET')
def get_all_categories():
    session = Session()
    try:
        categories = session.query(Category).all()
        return {
            "categories": [
                {
                    "category_id": category.category_id,
                    "name": category.name,
                    "description": category.description
                } for category in categories
            ]
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<category_id:int>', method='GET')
def get_single_category(category_id):
    session = Session()
    try:
        category = session.query(Category).filter_by(category_id=category_id).first()
        if not category:
            raise HTTPError(404, "Category not found")

        return {
            "category_id": category.category_id,
            "name": category.name,
            "description": category.description
        }
    except Exception as e:
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/', method='POST')
@jwt_required()
def create_category():
    session = Session()
    try:
        data = request.json
        new_category = Category(
            name=data['name'],
            description=data['description']
        )
        session.add(new_category)
        session.commit()

        return {"message": "Category created successfully!", "category_id": new_category.category_id}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<category_id:int>', method='PUT')
@jwt_required()
def update_category(category_id):
    session = Session()
    try:
        category = session.query(Category).filter_by(category_id=category_id).first()
        if not category:
            raise HTTPError(404, "Category not found")

        data = request.json
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)

        session.commit()

        return {"message": "Category updated successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()

@app.route('/<category_id:int>', method='DELETE')
@jwt_required()
def delete_category(category_id):
    session = Session()
    try:
        category = session.query(Category).filter_by(category_id=category_id).first()
        if not category:
            raise HTTPError(404, "Category not found")

        session.delete(category)
        session.commit()

        return {"message": "Category deleted successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPError(500, str(e))
    finally:
        session.close()
