import os
import json

responses_folder = "responses"

for filename in os.listdir(responses_folder):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(responses_folder, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Verifica se é o erro de quota        
        if (
            isinstance(data, dict)
            and "error" in data
            and "429 You exceeded your current quota" in data["error"]
        ):
            os.remove(file_path)
            print(f" Arquivo removido por erro 429: {filename}")
    except Exception as e:
        print(f" Erro ao ler {filename}: {e}")
