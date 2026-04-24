from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Personaje(Base):
    __tablename__ = 'personajes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    color_piel = Column(String(30))
    raza = Column(String(30))
    fuerza = Column(Integer)
    agilidad = Column(Integer)
    magia = Column(Integer)
    conocimiento = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)