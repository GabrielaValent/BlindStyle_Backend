from rembg import remove
from PIL import Image, ImageEnhance
import io
import base64
import numpy as np
import cv2

def preprocess_image(base64_image):
    
    if base64_image.startswith("data:image"):
        base64_image = base64_image.split(",")[1]
        
    image_data = base64.b64decode(base64_image)
    
    # Remove o fundo com segmentação
    result = remove(image_data)
    output = Image.open(io.BytesIO(result)).convert("RGBA")

    # Adiciona fundo branco
    white_bg = Image.new("RGBA", output.size, "WHITE")
    final_image = Image.alpha_composite(white_bg, output).convert("RGB")

    # Converte para o formato OpenCV (NumPy array)
    final_image_np = np.array(final_image)

    # Redimensiona e recorta para focar nas roupas
    desired_size = 512
    height, width, _ = final_image_np.shape
    min_dim = min(height, width)

    # Recorte centralizado
    start_x = (width - min_dim) // 2
    start_y = (height - min_dim) // 2
    cropped_image = final_image_np[start_y:start_y + min_dim, start_x:start_x + min_dim]

    # Redimensiona para as dimensões desejadas
    resized_image = cv2.resize(cropped_image, (desired_size, desired_size), interpolation=cv2.INTER_LINEAR)

    # Normaliza os valores de pixel
    normalized_image = cv2.normalize(resized_image, None, 0, 255, cv2.NORM_MINMAX)

    # Reduz o ruído e aplica filtro gaussiano
    denoised_image = cv2.GaussianBlur(normalized_image, (5, 5), 0)

    # Aumenta a nitidez usando um filtro gaussiano
    sharpened_image = cv2.addWeighted(normalized_image, 1.5, denoised_image, -0.5, 0)

    # Converte de volta para PIL
    final_image_pil = Image.fromarray(sharpened_image)

    # Ajusta o brilho e a nitidez
    brightness_enhancer = ImageEnhance.Brightness(final_image_pil)
    final_image_pil = brightness_enhancer.enhance(1.1)
    sharpness_enhancer = ImageEnhance.Sharpness(final_image_pil)
    final_image_pil = sharpness_enhancer.enhance(1.2)
    
    # Converte a imagem processada de volta para Base64
    buffered = io.BytesIO()
    final_image_pil.save(buffered, format="JPEG")
    #processed_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    image_binary = buffered.getvalue()
    return image_binary#processed_image_base64
