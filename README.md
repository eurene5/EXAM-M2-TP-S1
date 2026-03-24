# Éditeur de Texte Augmenté par l'IA pour le Malagasy
> **Projet TP Machine Learning** — Institut Supérieur Polytechnique de Madagascar (ISPM)  
> Master 2 — Semestre 1

---

## 👥 Membres du groupe et Rôles
| Nom | Rôle | Responsabilités principales |
|:--- |:--- |:--- |
| **[Nom]** |gestion du projet / Backend | Architecture FastAPI, Logicielle IA, API Design |
| **[Nom]** | NLP / Data Scientist | Scraping Wikipedia/Teny, Modèles N-grams, Lemmatisation |
| **[Nom]** | Frontend / UX Designer | Intégration Quill.js, Interface React, Expérience Utilisateur |
| **[Nom]** | DevOps / Intégration | Déploiement, Docker, Qualité de code |

---

## 📝 Présentation du projet
Ce projet est un éditeur de texte web intelligent conçu pour assister les rédacteurs malagasy. Le Malagasy étant une langue à faibles ressources numériques (*Low Resource Language*), l'outil combine des approches symboliques (règles), algorithmiques et data-driven pour pallier le manque de données massives.

---

## 🤖 Fonctionnalités IA (Description)

### 1. Correction & Validation
* **Correcteur Orthographique** : Analyse en temps réel via un dictionnaire hybride (Scraping + Levenshtein).
* **Vérification Phonotactique** : Détection automatique des combinaisons de lettres interdites en Malagasy (`nb`, `mk`, `sz`, etc.) via REGEX.

### 2. Analyse Linguistique
* **Lemmatisation intelligente** : Algorithme de réduction à la racine basé sur les préfixes (`mi-`, `man-`) et suffixes malagasy, gérant les mutations consonantiques.
* **Analyse de Sentiment** : Détection de la tonalité du texte (positif/négatif) via un lexique de mots-clés malagasy.

### 3. Assistance à la Rédaction
* **Autocomplétion (N-gram)** : Prédiction du mot suivant basée sur un modèle statistique de Trigrammes entraîné sur Wikipedia MG et la Bible.
* **Reconnaissance d'Entités (NER)** : Identification des lieux, institutions et personnalités malagasy.
* **Synthèse Vocale (TTS)** : Lecture à haute voix du texte pour faciliter la relecture.

---

## 🛠️ Stack Technique Résumée
* **Backend** : Python 3.10+, FastAPI, RapidFuzz, NLTK.
* **Frontend** : React.js, Quill.js, TailwindCSS.
* **Données** : Dictionnaire JSON, Corpus TXT, Modèles sérialisés (.pkl).

---

## 📚 Bibliographie & Sources
* **Sources de données** :
    * Wikipedia Malagasy (mg.wikipedia.org) - Corpus principal.
    * Tenymalagasy.org - Dictionnaire de référence.
    * Bible Malagasy - Corpus de texte formel.
* **Documentations & Outils** :
    * *N-gram Models & Markov Chains* - Documentation NLTK.
    * *FastAPI Framework* - Documentation officielle.
    * *Quill Rich Text Editor* - Guide d'intégration.
    * *Phonologie du Malagasy* - Règles de formation des mots.

---

## 📖 Documentation Technique
> *Pour les détails d'installation, l'arborescence complète et le fonctionnement interne des scripts de données, veuillez vous référer au fichier :* `DOCUMENTATION_TECHNIQUE.md`