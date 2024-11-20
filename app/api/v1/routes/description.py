import io
import cv2
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from PIL import Image
from tensorflow.keras.models import load_model 
import pickle


from app.api.v1.schemas.description import DescriptionRequestSchema, DescriptionSchema
from app.utils.image_utils import preprocess_image

router = APIRouter()

def load_encoders():
    with open('app/encoders.pkl', 'rb') as f:
        return pickle.load(f)

MODEL_PATH = "app\model.keras"
model = load_model(MODEL_PATH, safe_mode=False)
encoders = load_encoders()

def get_output_sizes():
    output_sizes = {}
    for key in encoders:
        output_sizes[key] = len(encoders[key].classes_)
    return output_sizes

def decode_prediction(attribute, pred_probs):
    label = encoders[attribute].classes_[np.argmax(pred_probs)]
    confidence = np.max(pred_probs)
    return label, confidence

def format_predictions(prediction):
    certain = []
    incertain = []
    for field in prediction:
        if '_output' in field:
            output_value = prediction[field][0]
            confidence_key = field.replace('_output', '_confidence')
            confidence_value = float(prediction[confidence_key][0])
            if confidence_value >= 0.6:
                certain.append(output_value.lower())
            else:
                incertain.append(output_value.lower())
    description = f"This clothing article is {', '.join(certain)}. It's also probably {', '.join(incertain)}, but i'm not sure. If you want more precise descriptions, try sending a different photo"
    
    predictions = {
         "predictions": {
            "description": description,
            "certain": certain,
            "incertain": incertain
        }
    }
    return predictions


@router.post("/description")
async def predict(request: DescriptionRequestSchema):
    try:
        preprocessed_image = preprocess_image(request.input)

        image = Image.open(io.BytesIO(preprocessed_image))
        np_array = np.array(image)

        resized_image = cv2.resize(np.array(np_array), (180, 180), interpolation=cv2.INTER_LINEAR)

        new_resized_image_array = np.expand_dims(resized_image, axis=0)

        predictions = model.predict(new_resized_image_array)
        
        decoded_predictions = {
            "gender_output": [],
            "gender_confidence": [],
            "subCategory_output": [],
            "subCategory_confidence": [],
            "articleType_output": [],
            "articleType_confidence": [],
            "baseColour_output": [],
            "baseColour_confidence": [],
            "usage_output": [],
            "usage_confidence": []
        }

        for i, attribute in enumerate(get_output_sizes().keys()):
            pred_probabilities = predictions[i]
            
            label, confidence = decode_prediction(attribute, pred_probabilities)
            
            decoded_predictions[f"{attribute}_output"].append(str(label))
            decoded_predictions[f"{attribute}_confidence"].append(str(confidence))
            
        return format_predictions(decoded_predictions)
                     
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a imagem: {str(e)}")
