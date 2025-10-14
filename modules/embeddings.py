import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
from modules.config import (
    FILTERED_DIR,
    VALID_CATEGORIES,
    VALID_USAGE,
    ATTRIBUTES,
    ATTR_DIM,
    VALID_TEXTURE,
    VALID_PRINT
)
from .vector_db import VectorDB

class EmbeddingGenerator:
    def __init__(self, vector_db: Optional[VectorDB] = None):
        """Inicializa o gerador de embeddings"""
        self.attribute_values = {
            "category": VALID_CATEGORIES,
            "usage": VALID_USAGE,
            "texture": VALID_TEXTURE,
            "print_category": VALID_PRINT
        }
        self.vector_db = vector_db
    
    def _hash_embedding(self, text: str, dim: int = 16) -> np.ndarray:
        # Create a deterministic seed from md5 hash
        md5 = hashlib.md5(text.encode("utf-8")).hexdigest()
        seed = int(md5[:8], 16)  # use first 8 hex digits as integer

        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(dim)
        return vec / np.linalg.norm(vec)
    
    

    def _generate_piece_embedding(self, piece_data: Dict) -> np.ndarray:
        """Gera embedding para uma peça de roupa"""
        embeddings = []
        
        # Processa cada atributo definido
        for attr in ATTRIBUTES:
            if attr in self.attribute_values:
                # Usa one-hot para atributos categóricos
                value = piece_data.get(attr, "UNK")
                encoding = self._hash_embedding(f"{attr}:{value}", ATTR_DIM)
            
            embeddings.append(encoding)
        
        # Concatena todos os embeddings de atributos
        return np.concatenate(embeddings)

    def _process_outfit(self, outfit_data: Dict, file_name: str) -> Tuple[List[np.ndarray], List[str]]:
        """Processa um outfit gerando embeddings e metadados para cada peça"""
        embeddings = []
        ids = []
        outfit_name = file_name.replace(".json", "")
        
        for piece_id, piece_data in outfit_data.items():
            try:
                # Gera embedding da peça
                piece_embedding = self._generate_piece_embedding(piece_data)
                embeddings.append(piece_embedding)
                ids.append(f"{outfit_name}/{piece_id}")
                
            except Exception as e:
                print(f"❌ Erro ao processar peça {piece_id} do outfit {file_name}: {e}")
                continue
                
        return embeddings, ids

    def process_and_store(self, collection_name: str, limit: Optional[int] = None) -> List[str]:
        """
        Processa outfits filtrados e armazena no banco vetorial
        
        Args:
            collection_name: Nome da coleção onde salvar
            limit: Número máximo de arquivos a processar
        """
        processed_files = []
        db = self.vector_db or VectorDB()
        
        for count, file_path in enumerate(Path(FILTERED_DIR).glob("*.json")):
            if limit is not None and count >= limit:
                break
                
            try:
                # Carrega dados do outfit
                with open(file_path, "r", encoding="utf-8") as f:
                    outfit_data = json.load(f)
                
                # Processa outfit
                embeddings, ids = self._process_outfit(outfit_data, file_path.name)
                
                if embeddings and ids: 
                    # Adiciona ao banco vetorial
                    db.add_items(
                        collection_name=collection_name,
                        embeddings=[e.tolist() for e in embeddings],
                        ids=ids
                    )
                    
                    processed_files.append(file_path.name)
                    print(f"✅ Outfit {file_path.name} adicionado à coleção {collection_name}")
                
            except Exception as e:
                print(f"❌ Erro ao processar {file_path.name}: {e}")
                continue
        
        return processed_files