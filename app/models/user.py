from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    _password = Column("password", String(255), nullable=False)  # hashed password
    role = Column(Enum('Admin', 'User', name='user_roles'), default='User')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

    def set_password(self, plaintext_password):
        """Hash a plaintext password and store its hashed version."""
        self._password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plaintext_password):
        """Check the password against its hashed version."""
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self._password.encode('utf-8'))

# if __name__ == '__main__':
#     engine = create_engine('sqlite:///users.db')
#     Base.metadata.create_all(engine)
