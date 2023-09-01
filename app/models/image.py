from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.item_id'))
    image_path = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="images")

# If setting up the database, you'd typically have a block of code to create the tables.
# For example:
# if __name__ == '__main__':
#     engine = create_engine('sqlite:///images.db')
#     Base.metadata.create_all(engine)
