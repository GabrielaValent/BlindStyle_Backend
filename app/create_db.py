# app/create_db.py
from app.db.base import Base, engine
from app.db.entity import User, ClothingItem, ClothingAnalysis, Analysis  # Certifique-se de que os modelos estão importados


Base.metadata.create_all(bind=engine)

#python -m app.create_db