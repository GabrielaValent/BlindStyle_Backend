import os
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

# Caminho do diretório
directory = 'responses'

# Inicializa contadores gerais
valid_outfits_count = 0
category_counts = Counter() # total de peças por categoria (tops, bottoms, shoes)
item_type_counts = defaultdict(Counter) # contagem de item_type para cada categoria
invalid_outfits_samples = []

def is_valid_outfit(pieces):
    # pieces é uma lista de dicionários com peças filtradas (sem others)    
    if not (2 <= len(pieces) <= 5):
        return False
    cats = [p['category'] for p in pieces]
    has_top = 'tops' in cats
    has_bottom = 'bottoms' in cats
    has_shoes = 'shoes' in cats
    return (has_top and has_bottom) or (has_top and has_shoes)

for filename in os.listdir(directory):
    if not filename.endswith('.json'):
        continue
    path = os.path.join(directory, filename)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            outfit = json.load(f)
            
        # Verifica se outfit é um dicionário ou uma lista        
        if isinstance(outfit, dict):
            pieces = list(outfit.values())
        elif isinstance(outfit, list):
            pieces = outfit
        else:
            print(f"Formato inesperado no arquivo: {filename}")
            continue
        
        # filtra peças descartando categoria "others"        
        filtered_pieces = [p for p in pieces if isinstance(p, dict) and p.get('category') != 'others']
        
        # verifica se é outfit válido        
        if is_valid_outfit(filtered_pieces):
            valid_outfits_count += 1
            for piece in filtered_pieces:
                category_counts[piece['category']] += 1
                item_type_counts[piece['category']][piece['item_type']] += 1
        else:
            if len(invalid_outfits_samples) < 3:
                # salva para debug                
                invalid_outfits_samples.append({
                    'filename': filename,
                    'piece_count': len(filtered_pieces),
                    'categories': [p['category'] for p in filtered_pieces],
                    'pieces': filtered_pieces
                })
                
    except Exception as e:
        print(f"Erro ao processar o arquivo {filename}: {e}")
        continue
    
print("\nExemplos de outfits inválidos:")
for sample in invalid_outfits_samples:
    print(f"\nArquivo: {sample['filename']}")
    print(f"Número de peças (sem 'others'): {sample['piece_count']}")
    print(f"Categorias encontradas: {sample['categories']}")
    print("Peças:")
    for p in sample['pieces']:
        print(f"  - category: {p['category']}, item_type: {p['item_type']}, usage: {p['usage']}")

print(f'\nTotal de outfits válidos: {valid_outfits_count}')
print('Quantidade de peças por categoria:')
for cat, count in category_counts.items():
    print(f' {cat}: {count}')
    
print('\nContagem de tipos de itens por categoria:')
for cat, counter in item_type_counts.items():
    print(f'Categoria {cat}:')
    for item_type, count in counter.items():
        print(f' {item_type}: {count}')
        
# Gráficos
# 1. Quantidade de peças por categoria (top 10)
top_categories = category_counts.most_common(10)
categories, counts = zip(*top_categories)

plt.figure(figsize=(8, 5))
plt.bar(categories, counts)
plt.title('Quantidade de peças por categoria (Top 10)')
plt.ylabel('Quantidade')
plt.xlabel('Categoria')
plt.show()

# 2. Para cada categoria, gráfico de distribuição de item_type (top 10)
for cat, counter in item_type_counts.items():
    top_items = counter.most_common(10)
    item_types, item_counts = zip(*top_items)
    
    plt.figure(figsize=(10, 5))
    plt.bar(item_types, item_counts)
    plt.title(f'Distribuição de tipos em {cat} (Top 10)')
    plt.ylabel('Quantidade')
    plt.xlabel('Tipo de item')
    plt.xticks(rotation=45)
    plt.show()
