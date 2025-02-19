from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Sex(Base):
    __tablename__ = 'sex'
    id_sex = Column(Integer, primary_key=True)
    sex_label = Column(String(50), nullable=False)

    patient = relationship("Patient", back_populates="sex")
