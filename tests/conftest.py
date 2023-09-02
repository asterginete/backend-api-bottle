import pytest
from app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

@pytest.fixture(scope='session')
def init_database():
    # Create the database and the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: Drop the database tables
    Base.metadata.drop_all(bind=engine)
