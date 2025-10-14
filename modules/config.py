import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Diretórios
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGES_DIR = BASE_DIR / "archive" / "images"
RESPONSES_DIR = BASE_DIR / "responses"
FILTERED_DIR = BASE_DIR / "filtered_outfits"
VECTOR_DB_DIR = BASE_DIR / "chroma_db"

# Configurações de Embedding
ATTRIBUTES = ["category", "item_type", "primary_color", "usage", "texture", "print_category"]
ATTR_DIM = 16
PIECE_DIM = len(ATTRIBUTES) * ATTR_DIM

# Configurações de Filtragem
MAX_ITEMS_PER_OUTFIT = 5

# Categorias válidas
VALID_CATEGORIES = ["tops", "bottoms", "shoes", "others"]
VALID_USAGE = ["casual", "formal", "business", "sportswear", "sleepwear", "outerwear", "party", "workwear"]
VALID_TEXTURE = ["cotton", "denim", "leather", "polyester", "wool", "silk", "linen", "knit", "suede", "nylon", "fleece", "velvet", "mesh", "others"]
VALID_PRINT = ["striped", "animal", "floral", "plaid", "plain", "abstract", "logo", "graphic"]

# Prompt para extração de features
FEATURE_EXTRACTION_PROMPT = """
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
{VALID_CATEGORIES}

usage:
{VALID_USAGE}

texture:
{VALID_TEXTURE}

print_category:
{VALID_PRINT}

Output example:
{{
  "1.jpg": {{
    "category": "tops",
    "item_type": "tshirt",
    "primary_color": "blue",
    "usage": "casual",
    "texture": "cotton",
    "print_category": "graphic"
  }}
}}

Images and Filenames to proccess:
"""

# Chave da API Gemini (deve ser movida para variável de ambiente posteriormente)
GEMINI_API_KEY = os.getenv('GEMINI_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente. Crie um arquivo .env com a chave.")

LLM_MODEL = "gemini-2.5-pro"