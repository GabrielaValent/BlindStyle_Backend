import os
import random
import json
from PIL import Image
import google.generativeai as genai
import re

# Configurar a API Gemini
genai.configure(api_key="AIzaSyCiHIAFGQCmMHlpFouxWCWWUTiRmF52CSI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Prompt fornecido
prompt = """
Context:
From a given set of images, information about compatible outfit compositions is to be extracted. Each valid image represents a single clothing item that makes up these outfits. The goal is to generate objective descriptions for each piece, based on predefined characteristics, in order to facilitate future combination and analysis of these clothes from a structured dataset.

Each image will be preceded by a line containing its filename (e.g., "image1.jpg"). Use this filename as the key in the resulting JSON.
Task:
Classify each image into one of the following categories:

tops
bottoms
shoes
others (if the image contains multiple items or a single item cannot be clearly identified)

For images classified as tops, bottoms, or shoes, identify and describe the following characteristics using the specified values below:

item_type: type of the piece (free text, based on the image observation, generalize to avoid outliers)
primary_color: predominant color (free text, generalize to avoid outliers )
usage: intended use (see enum below)
texture: type of fabric or material (see enum below)
print_category: main pattern or print (see enum below)

Return the results in JSON format, where the key is the filename of the image and the value is an object with the classification and attributes.

Available enums:

category:
["tops", "bottoms", "shoes", "others"]

usage:
["casual", "formal", "business", "sportswear", "sleepwear", "outerwear", "party", "workwear"]

texture:
["cotton", "denim", "leather", "polyester", "wool", "silk", "linen", "knit", "suede", "nylon", "fleece", "velvet", "mesh", "others"]

print_category:
["striped", "animal", "floral", "plaid", "plain", "abstract", "logo", "graphic"]

Output example:
{
    "1.jpg": {
        "category": "tops",
        "item_type": "tshirt",
        "primary_color": "blue",
        "usage": "casual",
        "texture": "cotton",
        "print_category": "graphic"
    }
}

Images and Filenames to proccess:

"""
base_folder = "archive/images"
output_base = "responses"

def numeric_sort_key(filename):
    base = os.path.splitext(filename)[0]
    try:
        return int(base)
    except ValueError:
        return base
    
# Cria a pasta de saída se não existir
os.makedirs(output_base, exist_ok=True)

def clean_json_text(text):
    # Remove bloco markdown    
    text = re.sub(r"```json\n(.*?)\n```", r"\1", text, flags=re.DOTALL)

    # Remove vírgulas extras antes de } ou ]    
    text = re.sub(r",\s*([}\]])", r"\1", text)

    return text

def load_images_with_names(folder):
    parts = [prompt] # certifique-se de que 'prompt' está definido antes    
    files = [f for f in os.listdir(folder) if f.lower().endswith(".jpg")]
    for file in sorted(files, key=numeric_sort_key):
        image_path = os.path.join(folder, file)
        try:
            img = Image.open(image_path)
            parts.append(f"Filename of the image below: {file} image:")
            parts.append(img)
        except Exception as e:
            print(f"Erro ao carregar imagem {file}: {e}")
        return parts
    
# Seleciona pastas aleatórias
all_folders = [
    os.path.join(base_folder, name)
    for name in os.listdir(base_folder)
    if os.path.isdir(os.path.join(base_folder, name))
]

selected_folders = all_folders

# Processa cada pasta
for folder in selected_folders:
    folder_name = os.path.basename(folder)
    #output_folder = os.path.join(output_base, folder_name)
    os.makedirs(output_base, exist_ok=True)

    output_file_path = os.path.join(output_base, f"{folder_name}.json")
    if os.path.exists(output_file_path):
        print(f" Pulando {folder_name}, já existe {output_file_path}")
        continue

    try:
        content_parts = load_images_with_names(folder)
        if len(content_parts) <= 1:
            print(f" Sem imagens válidas em {folder_name}")
            continue

        response = model.generate_content(content_parts)

        # Tenta converter para JSON

        def extract_clean_json(text):
            # Remove blocos markdown ```json ... ```            
            match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
            if match:
                return match.group(1)
            return text # fallback: retorna o texto inteiro
        
        try:
            cleaned_text = extract_clean_json(response.text)
            response_json = json.loads(cleaned_text)
        except json.JSONDecodeError:
            print(f" JSON inválido retornado por {folder_name}")
            response_json = {"error": "Invalid JSON from model", "raw_response": response.text}


        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(response_json, f, indent=2, ensure_ascii=False)

        print(f" JSON salvo em {output_file_path}")

    except Exception as e:
        error_info = {"error": str(e)}
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(error_info, f, indent=2, ensure_ascii=False)
        print(f" Erro ao processar {folder_name}: {e}")


