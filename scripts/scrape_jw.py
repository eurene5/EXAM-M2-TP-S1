import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from scrape_wiki import is_valid_malagasy 

def scrape_jw_malagasy():
    base_url = "https://www.jw.org/mg/zavatra-misy/boky-gazety/"
    headers = {'User-Agent': 'Projet_IA_ISPM_Etudiant/1.0 (ispm.mg)'}
    
    new_words = set()

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On récupère les liens vers les derniers articles pour extraire du texte nouveau
        links = [a['href'] for a in soup.find_all('a', href=True) if '/mg/' in a['href']][:10]

        for link in links:
            full_url = "https://www.jw.org" + link if link.startswith('/') else link
            print(f"Extraction de : {full_url}")
            
            page = requests.get(full_url, headers=headers)
            page_soup = BeautifulSoup(page.text, 'html.parser')
            
            paragraphs = page_soup.find_all('p')
            for p in paragraphs:
                words = re.findall(r'\b\w+\b', p.text)
                for w in words:
                    if is_valid_malagasy(w):
                        new_words.add(w.lower())
            
            time.sleep(1) 

        return new_words
    except Exception as e:
        print(f"Erreur sur JW.org: {e}")
        return set()

def merge_with_main_dict(new_set):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, 'data', 'dictionnaire_riche.json')
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            existing = set(json.load(f))
    else:
        existing = set()

    updated = existing.union(new_set)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(sorted(list(updated)), f, ensure_ascii=False, indent=4)
    print(f"Mise à jour terminée. Total : {len(updated)} mots.")

if __name__ == "__main__":
    mots_jw = scrape_jw_malagasy()
    if mots_jw:
        merge_with_main_dict(mots_jw)