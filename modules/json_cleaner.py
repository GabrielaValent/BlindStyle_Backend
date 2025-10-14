import os
import json
from pathlib import Path
from typing import List
from .config import RESPONSES_DIR

class JsonCleaner:
    @staticmethod
    def clean_error_responses(responses_dir: Path = RESPONSES_DIR) -> List[str]:
        """
        Remove arquivos JSON que contêm erros de quota ou outros erros do Gemini.
        
        Args:
            responses_dir: Diretório contendo os arquivos JSON de resposta
            
        Returns:
            List[str]: Lista de arquivos removidos
        """
        removed_files = []
        
        for file_path in responses_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Verifica se é o erro de quota ou outros erros
                if (
                    isinstance(data, dict) and
                    "error" in data
                ):
                    os.remove(file_path)
                    removed_files.append(file_path.name)
                    print(f"🗑️ Arquivo removido por erro: {file_path.name}")
            except Exception as e:
                print(f"⚠️ Erro ao ler {file_path.name}: {e}")
        
        return removed_files