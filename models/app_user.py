from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AppUser(Base):
    __tablename__ = 'app_user'
    id_sex = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_email = Column(String(50), nullable=False)

    user_role = relationship("UserRole", back_populates="app_user")
