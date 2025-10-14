import os
import json
import random
from pathlib import Path
from typing import Dict, Optional, List
from .config import (
    RESPONSES_DIR,
    FILTERED_DIR,
    MAX_ITEMS_PER_OUTFIT
)

class OutfitFilter:
    @staticmethod
    def filter_outfit(outfit: Dict, file_name: str) -> Optional[Dict]:
        """
        Filtra um outfit removendo itens inválidos e limitando o número de peças.
        
        Args:
            outfit: Dicionário contendo as peças do outfit
            file_name: Nome do arquivo para logging
            
        Returns:
            Dict: Outfit filtrado ou None se inválido
        """
        # Remove "others"
        filtered_items = {k: v for k, v in outfit.items() if v.get("category") != "others"}

        if not filtered_items:
            print(f"❌ Outfit inválido, todas as peças classificadas como others: {file_name}")
            return None

        # Agrupa por categoria
        tops = [k for k, v in filtered_items.items() if v["category"] == "tops"]
        bottoms = [k for k, v in filtered_items.items() if v["category"] == "bottoms"]
        shoes = [k for k, v in filtered_items.items() if v["category"] == "shoes"]

        # Regras de validação do outfit
        valid = (tops and shoes) or (tops and bottoms)
        if not valid:
            print(f"❌ Outfit inválido, faltam categorias necessárias: {file_name}")
            return None

        selected = {}

        # Seleciona uma peça de cada categoria necessária
        if tops:
            t = random.choice(tops)
            selected[t] = filtered_items[t]
        if bottoms:
            b = random.choice(bottoms)
            selected[b] = filtered_items[b]
        if shoes:
            s = random.choice(shoes)
            selected[s] = filtered_items[s]

        # Pool de peças restantes
        remaining = {k: v for k, v in filtered_items.items() if k not in selected}

        # Preenche até MAX_ITEMS aleatoriamente
        if remaining:
            extras = random.sample(
                list(remaining.items()),
                k=min(MAX_ITEMS_PER_OUTFIT - len(selected), len(remaining))
            )
            selected.update(dict(extras))

        print(f"✅ Outfit válido: {file_name}")
        return selected

    def process_responses(self, limit: Optional[int] = None) -> List[str]:
        """
        Processa todos os arquivos JSON de resposta e gera outfits filtrados.
        
        Args:
            limit: Número máximo de arquivos a processar (opcional)
            
        Returns:
            List[str]: Lista de arquivos processados com sucesso
        """
        processed_files = []
        
        os.makedirs(FILTERED_DIR, exist_ok=True)
        
        for count, file_path in enumerate(Path(RESPONSES_DIR).glob("*.json")):
            if limit is not None and count >= limit:
                break
                
            try:
                output_path = FILTERED_DIR / file_path.name
                if output_path.exists():
                    print(f"⏩ Pulando {output_path}, já existe {file_path.name}")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as f:
                    outfit = json.load(f)

                filtered = self.filter_outfit(outfit, file_path.name)

                if filtered:
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(filtered, f, indent=2, ensure_ascii=False)
                    processed_files.append(file_path.name)

            except Exception as e:
                print(f"❌ Erro ao processar {file_path.name}: {e}")

        print(f"✅ Filtragem concluída. Resultados salvos em: {FILTERED_DIR}")
        return processed_files