from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    content = Column(Text, nullable=False)
    status = Column(Enum('Read', 'Unread', name='notification_statuses'), default='Unread')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")  # This assumes a User model has been defined in user.py

# If setting up the database, you'd typically have a block of code to create the tables.
# For example:
# if __name__ == '__main__':
#     engine = create_engine('sqlite:///notifications.db')
#     Base.metadata.create_all(engine)
