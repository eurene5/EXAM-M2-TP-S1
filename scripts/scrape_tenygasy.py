import requests
from bs4 import BeautifulSoup
import json
import os

from scrape_wiki import is_valid_malagasy 

def scrape_official_lexicon():
    # Exemple pour une section du dictionnaire
    url = "http://tenymalagasy.org/bins/teny2/A" 
    headers = {'User-Agent': 'Projet_IA_ISPM_Etudiant/1.0'}
    
    new_words = set()
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraction des mots (dans des balises spécifiques sur ce site)
        for entry in soup.find_all('b'): # À ajuster selon l'inspection HTML du site
            word = entry.text.strip()
            if is_valid_malagasy(word):
                new_words.add(word.lower())
                
        return new_words
    except Exception as e:
        print(f"Erreur sur TenyMalagasy: {e}")
        return set()

import os

def merge_and_save(new_data):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    data_dir = os.path.join(root_dir, 'data')
    path = os.path.join(data_dir, 'dico.json')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Dossier créé : {data_dir}")

    # Chargement de l'existant
    existing_data = set()
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = set(json.load(f))

    # Fusion et sauvegarde
    existing_data.update(new_data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(sorted(list(existing_data)), f, ensure_ascii=False, indent=4)
    
    print(f"Succès ! {len(existing_data)} mots sont maintenant dans {path}")

if __name__ == "__main__":
    mots_officiels = scrape_official_lexicon()
    merge_and_save(mots_officiels)