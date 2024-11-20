from pydantic import BaseModel
from typing import List


class DescriptionSchema(BaseModel):
    gender_output: List[str]
    gender_confidence: List[float]
    subCategory_output: List[str]
    subCategory_confidence: List[float]
    articleType_output: List[str]
    articleType_confidence: List[float]
    baseColour_output: List[str]
    baseColour_confidence: List[float]
    usage_output: List[str]
    usage_confidence: List[float]
    
    class Config:
        from_attributes = True



class DescriptionAttributesSchema(BaseModel):
    description: str
    certain: List[str]
    incertain: List[str]
    
    class Config:
        from_attributes = True


class DescriptionReturnSchema(BaseModel):
    predictions: List[DescriptionAttributesSchema]
    
    class Config:
        from_attributes = True
        


class DescriptionRequestSchema(BaseModel):
    input: str