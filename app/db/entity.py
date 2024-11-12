from sqlalchemy import Column, Integer, LargeBinary, String, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    clothing_items = relationship("ClothingItem", back_populates="owner")

class ClothingItem(Base):
    __tablename__ = "clothing_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    ownership = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    clothing_analysis_id = Column(Integer, ForeignKey("clothing_analysis.id"), nullable=True)
    image_url = Column(LargeBinary, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(Boolean, default=True)

    owner = relationship("User", back_populates="clothing_items")
    analysis = relationship("ClothingAnalysis", back_populates="clothing_item")

class ClothingAnalysis(Base):
    __tablename__ = "clothing_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    clothing_id1 = Column(Integer)  
    clothing_id2 = Column(Integer)  

    clothing_item = relationship("ClothingItem", back_populates="analysis")
    analyses = relationship("Analysis", back_populates="clothing_analysis")

class Analysis(Base):
    __tablename__ = "analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis = Column(Text, nullable=False)
    clothing_analysis_id = Column(Integer, ForeignKey("clothing_analysis.id"), nullable=False)
    
    clothing_analysis = relationship("ClothingAnalysis", back_populates="analyses")
