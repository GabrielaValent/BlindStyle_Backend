import os
import json
import re
from pathlib import Path
from PIL import Image
import google.generativeai as genai
from typing import List, Dict, Union, Optional
from .config import (
    IMAGES_DIR, 
    RESPONSES_DIR, 
    FEATURE_EXTRACTION_PROMPT,
    GEMINI_API_KEY,
    LLM_MODEL
)

class FeatureExtractor:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(LLM_MODEL)
        self.prompt = FEATURE_EXTRACTION_PROMPT

    def _numeric_sort_key(self, filename: str) -> Union[int, str]:
        base = os.path.splitext(filename)[0]
        try:
            return int(base)
        except ValueError:
            return base

    def _load_images_with_names(self, folder: Path) -> List:
        parts = [self.prompt]
        files = [f for f in os.listdir(folder) if f.lower().endswith(".jpg")]
        for file in sorted(files, key=self._numeric_sort_key):
            image_path = os.path.join(folder, file)
            try:
                img = Image.open(image_path)
                parts.append(f"Filename of the image below: {file} image:")
                parts.append(img)
            except Exception as e:
                print(f"Erro ao carregar imagem {file}: {e}")
        return parts

    def _extract_clean_json(self, text: str) -> str:
        match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text

    def extract_features(self, folder_path: Union[str, Path]) -> Optional[Dict]:
        """
        Extrai features de todas as imagens em uma pasta usando o Gemini.
        
        Args:
            folder_path: Caminho para a pasta contendo as imagens JPG
            
        Returns:
            Dict: Dicionário com as features extraídas ou None em caso de erro
        """
        folder_path = Path(folder_path)
        folder_name = folder_path.name
        output_file_path = RESPONSES_DIR / f"{folder_name}.json"

        try:
            content_parts = self._load_images_with_names(folder_path)
            if len(content_parts) <= 1:
                print(f"⚠️ Sem imagens válidas em {folder_name}")
                return None

            response = self.model.generate_content(content_parts)

            try:
                cleaned_text = self._extract_clean_json(response.text)
                response_json = json.loads(cleaned_text)
            except json.JSONDecodeError:
                print(f"❌ JSON inválido retornado por {folder_name}")
                response_json = {
                    "error": "Invalid JSON from model",
                    "raw_response": response.text
                } #trazer o limpeza json pra ser executado aqui

            # Salva o resultado
            os.makedirs(RESPONSES_DIR, exist_ok=True)
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(response_json, f, indent=2, ensure_ascii=False)

            print(f"✅ JSON salvo em {output_file_path}")
            return response_json

        except Exception as e:
            error_info = {"error": str(e)}
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(error_info, f, indent=2, ensure_ascii=False)
            print(f"❌ Erro ao processar {folder_name}: {e}")
            return None

    def process_all_folders(self) -> None:
        """
        Processa todas as pastas de imagens no diretório base.
        """
        for folder in Path(IMAGES_DIR).iterdir():
            if folder.is_dir():
                output_file = RESPONSES_DIR / f"{folder.name}.json"
                if output_file.exists():
                    print(f"⏩ Pulando {folder.name}, já existe {output_file}")
                    continue
                self.extract_features(folder)