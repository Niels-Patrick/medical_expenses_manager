from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserRole(Base):
    __tablename__ = 'user_role'
    id_sex = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)

    app_user = relationship("AppUser", back_populates="user_role")
