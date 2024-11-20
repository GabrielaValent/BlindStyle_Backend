from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.api.v1.schemas.analysis import AnalysisSchema
from app.api.v1.schemas.error import ServiceError
from app.db.entity import ClothingAnalysis as ClothingAnalysisEntity , Analysis as AnalysisEntity
from app.services.item_service import get_clothing_item
from app.core.config import settings
import google.generativeai as genai


def get_last_suggestion(db: Session, item_id: int, user_id: int):
    item = get_clothing_item(db, item_id, user_id)
    clothing_analysis = db.query(ClothingAnalysisEntity).filter(
        (ClothingAnalysisEntity.clothing_id1 == item_id) | 
        (ClothingAnalysisEntity.clothing_id2 == item_id)
    ).order_by(desc(ClothingAnalysisEntity.id)).first()

    if not clothing_analysis:
        raise ServiceError("Clothing Analysis not found")
    
    analysis = db.query(AnalysisEntity).filter(AnalysisEntity.id == clothing_analysis.analysis_id).first()

    if not analysis:
        raise ServiceError("Analysis not found")

    analysis_schema = analysis_entity_to_schema(analysis)
    
    return analysis_schema

def analysis_entity_to_schema(analysis: AnalysisEntity):
    schema = AnalysisSchema(
        analysis = analysis.analysis
    )
    return schema


def post_single_clothing_analysis(db: Session, user_id: int, clothing_id1: int):
    item1 = get_clothing_item(db, clothing_id1, user_id)
    parts = item1.description.split(".")
    first_two_parts = ".".join(parts[:2])
    prompt = f"You are an AI with expertise in clothing styles and combinations. Given the following clothing characteristics: {first_two_parts} generate a response of maximum 300 characters in a single paragraph, not topics, suggesting great style combinations"

    genai.configure(api_key=settings.GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    analysis_description = response.text

    analysis = AnalysisEntity(
        analysis = analysis_description
    )
    db.add(analysis)
    db.flush()

    clothing_analysis = ClothingAnalysisEntity (
        clothing_id1 = clothing_id1,
        clothing_id2 = None,
        analysis_id = analysis.id
    )
    db.add(clothing_analysis)
    db.commit()
    db.refresh(clothing_analysis)   

    return clothing_analysis