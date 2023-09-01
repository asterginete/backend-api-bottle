from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.item_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="comments")
    user = relationship("User")  # This assumes a User model has been defined in user.py

# If setting up the database, you'd typically have a block of code to create the tables.
# For example:
# if __name__ == '__main__':
#     engine = create_engine('sqlite:///comments.db')
#     Base.metadata.create_all(engine)
