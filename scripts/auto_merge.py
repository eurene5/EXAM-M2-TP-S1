import json
import csv
import os
from scrape_wiki import is_valid_malagasy 

def load_data(file_path):
    words = set()
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list): words.update(data)
                elif isinstance(data, dict): words.update(data.keys())
        elif ext == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row: words.add(row[0])
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word: words.add(word)
    except Exception as e:
        print(f"Ignoré : {file_path} (Erreur: {e})")
    return words

def auto_merge_folder():
    # Chemins relatifs vers la racine du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    main_dict_path = os.path.join(data_dir, 'dico.json')

    final_lexicon = set()

    # 1. Charger le dico principal s'il existe déjà
    if os.path.exists(main_dict_path):
        with open(main_dict_path, 'r', encoding='utf-8') as f:
            final_lexicon.update(json.load(f))
        print(f"Dictionnaire actuel chargé : {len(final_lexicon)} mots.")

    # 2. Scanner le dossier 'data' pour trouver d'autres fichiers
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        
        if filename == 'dico.json':
            continue
            
        if filename.endswith(('.json', '.csv', '.txt')):
            print(f"Fusion automatique de : {filename}...")
            new_words = load_data(file_path)
            
            for w in new_words:
                clean_w = str(w).lower().strip()
                if is_valid_malagasy(clean_w):
                    final_lexicon.add(clean_w)

    # 3. Sauvegarde finale
    with open(main_dict_path, 'w', encoding='utf-8') as f:
        json.dump(sorted(list(final_lexicon)), f, ensure_ascii=False, indent=4)
    
    print(f"\n--- TERMINÉ ---")
    print(f"Le dictionnaire maître contient maintenant {len(final_lexicon)} mots valides.")

if __name__ == "__main__":
    auto_merge_folder()