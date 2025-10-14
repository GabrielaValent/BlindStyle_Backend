from pathlib import Path
import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional, Any
from .config import VECTOR_DB_DIR

class VectorDB:
    def __init__(self):
        """Inicializa conexão com ChromaDB"""
        self.client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR),
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
    def create_collection(self, name: str, metadata: Optional[Dict] = None) -> Any:
        """
        Cria uma nova coleção
        
        Args:
            name: Nome da coleção
            metadata: Metadados da coleção (opcional)
        """
        return self.client.create_collection(
            name=name,
            metadata=metadata or {"hnsw:space": "cosine"}
        )
    
    def get_collection(self, name: str) -> Any:
        """Obtém uma coleção existente"""
        return self.client.get_collection(name)
    
    def get_or_create_collection(self, name: str, metadata: Optional[Dict] = None) -> Any:
        """Obtém ou cria uma coleção"""
        try:
            return self.get_collection(name)
        except:
            return self.create_collection(name, metadata)
    
    def delete_collection(self, name: str) -> None:
        """Deleta uma coleção"""
        self.client.delete_collection(name)
    
    def list_collections(self) -> List[str]:
        """Lista todas as coleções existentes"""
        return [col.name for col in self.client.list_collections()]
    
    def add_items(
        self,
        collection_name: str,
        embeddings: List[List[float]],
        ids: List[str],
        metadatas: Optional[List[Dict]] = None

    ) -> None:
        """
        Adiciona itens a uma coleção
        
        Args:
            collection_name: Nome da coleção
            embeddings: Lista de embeddings
            metadatas: Lista de metadados
            ids: Lista de IDs únicos
        """
        collection = self.get_collection(collection_name)
        collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
    def add_item(
        self,
        collection_name: str,
        embedding: List[float],
        id: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Adiciona itens a uma coleção
        
        Args:
            collection_name: Nome da coleção
            embeddings: Lista de embeddings
            metadatas: Lista de metadados
            ids: Lista de IDs únicos
        """
        collection = self.get_collection(collection_name)
        collection.upsert(
            embeddings=embedding,
            metadatas=metadata,
            ids=id
        )
    
    def search_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> Dict:
        """
        Busca itens similares em uma coleção
        
        Args:
            collection_name: Nome da coleção
            query_embedding: Embedding de consulta
            n_results: Número de resultados
            filter_dict: Filtros a aplicar
        """
        collection = self.get_collection(collection_name)
        return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_dict or {}
        )
    
    def get_by_id(self, collection_name: str, key: str):
        """
        Fetch an item by its key (id) from the given collection.
        Returns the embedding, metadata, and id if found.
        """
        collection = self.get_collection(collection_name)
        res = collection.get(ids=[key], include=["embeddings"])
        if not res["ids"]:
            return None
        return {
            "id": res["ids"][0],
            "embedding": res["embeddings"][0],
        }
    
    def delete_items(self, collection_name: str, ids: List[str]) -> None:
        """Deleta itens de uma coleção por IDs"""
        collection = self.get_collection(collection_name)
        collection.delete(ids=ids)