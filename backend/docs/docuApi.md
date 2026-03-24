# API Documentation — Malagasy Editor IA

Base URL : `http://localhost:8000`  
Framework : FastAPI  
Tous les endpoints retournent du JSON.

---

## Sommaire

- [GET `/`](#get-)
- [GET `/lemmatize/{word}`](#get-lemmatizeword)
- [GET `/check`](#get-check)
- [GET `/analyze/{word}`](#get-analyzeword)
- [GET `/autocomplete`](#get-autocomplete)

---

## GET `/`

Endpoint de santé. Vérifie que l'API est bien en ligne.

**Paramètres** : aucun

**Réponse**

```json
{
  "message": "Bienvenue sur l'API de l'Éditeur Malagasy"
}
```

---

## GET `/lemmatize/{word}`

Retourne la racine (lemme) d'un mot malagasy en appliquant les règles de suppression des préfixes et suffixes.

**Paramètre de chemin**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `word` | `string` | Le mot à lemmatiser |

**Exemple de requête**

```
GET /lemmatize/manosika
```

**Réponse**

```json
{
  "original": "manosika",
  "root": "tosika",
  "is_root": false
}
```

**Champs de la réponse**

| Champ | Type | Description |
|-------|------|-------------|
| `original` | `string` | Le mot tel qu'envoyé |
| `root` | `string` | La racine détectée après suppression des affixes |
| `is_root` | `boolean` | `true` si le mot est déjà sa propre racine |

---

## GET `/check`

Vérifie l'orthographe d'un mot. Si le mot est inconnu, retourne des suggestions proches par distance de Levenshtein. Vérifie également les règles phonotactiques du malagasy.

**Paramètre de requête**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `word` | `string` | Le mot à vérifier |

**Exemple de requête**

```
GET /check?word=fahafisaoan
```

**Réponse — mot incorrect**

```json
{
  "word": "fahafisaoan",
  "is_correct": false,
  "suggestions": ["fahafisaoana", "fahafisaovana"],
  "phonotactic_error": false
}
```

**Réponse — mot correct**

```json
{
  "word": "fahafisaoana",
  "is_correct": true,
  "suggestions": [],
  "phonotactic_error": false
}
```

**Réponse — erreur phonotactique**

```json
{
  "word": "nkalo",
  "is_correct": false,
  "suggestions": [],
  "phonotactic_error": true
}
```

**Champs de la réponse**

| Champ | Type | Description |
|-------|------|-------------|
| `word` | `string` | Le mot vérifié |
| `is_correct` | `boolean` | `true` si le mot est dans le dictionnaire |
| `suggestions` | `string[]` | Liste de mots proches (vide si le mot est correct) |
| `phonotactic_error` | `boolean` | `true` si le mot contient une combinaison de lettres impossible en malagasy (ex : `nb`, `mk`, `dt`) |

---

## GET `/analyze/{word}`

Analyse complète d'un mot. Cet endpoint est conçu pour être appelé lors d'un **clic droit** ou d'une sélection dans l'éditeur. Il retourne la racine, la validité orthographique, la conformité phonotactique et des métadonnées sur la structure morphologique du mot.

**Paramètre de chemin**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `word` | `string` | Le mot à analyser |

**Exemple de requête**

```
GET /analyze/mpanoratra
```

**Réponse**

```json
{
  "word": "mpanoratra",
  "root": "soratra",
  "is_valid": true,
  "phonotactic_ok": true,
  "analysis": {
    "structure": "Mot dérivé (Préfixé)",
    "length": 10,
    "prefix_detected": "mpan"
  }
}
```

**Champs de la réponse**

| Champ | Type | Description |
|-------|------|-------------|
| `word` | `string` | Le mot analysé |
| `root` | `string` | La racine du mot |
| `is_valid` | `boolean` | `true` si le mot est dans le dictionnaire |
| `phonotactic_ok` | `boolean` | `true` si la phonotactique est respectée |
| `analysis.structure` | `string` | Type morphologique : `"Racine pure"`, `"Mot dérivé (Préfixé)"` ou `"Inconnue"` |
| `analysis.length` | `integer` | Nombre de caractères du mot |
| `analysis.prefix_detected` | `string \| null` | Le préfixe identifié (`"mpan"`, `"mi"`, `"ma"`…) ou `null` si aucun |

---

## GET `/autocomplete`

Prédit le mot suivant ou propose des corrections selon le contexte. Cet endpoint reçoit le **texte complet** en cours de frappe et analyse le dernier mot pour décider s'il faut corriger ou prédire.

**Logique interne :**
1. Si le dernier mot est mal orthographié → retourne des **corrections**
2. Si le dernier mot est valide → retourne des **prédictions** du mot suivant via le modèle N-gram

**Paramètre de requête**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `text` | `string` | Le texte complet tapé par l'utilisateur jusqu'ici |

**Exemple de requête — dernier mot valide**

```
GET /autocomplete?text=ny%20ankizy%20mani
```

**Réponse — mode prédiction**

```json
{
  "type": "prediction",
  "suggestions": ["maniry", "manidina", "maninjitra"],
  "root_detected": null
}
```

**Exemple de requête — dernier mot incorrect**

```
GET /autocomplete?text=ny%20fahafisaoan
```

**Réponse — mode correction**

```json
{
  "type": "correction",
  "suggestions": ["fahafisaoana", "fahafisaovana"],
  "root_detected": null
}
```

**Réponse — racine détectée (mot dérivé reconnu)**

```json
{
  "type": "prediction",
  "suggestions": ["ny", "ho", "dia"],
  "root_detected": "soratra"
}
```

**Champs de la réponse**

| Champ | Type | Description |
|-------|------|-------------|
| `type` | `string` | `"prediction"` ou `"correction"` selon le cas |
| `suggestions` | `string[]` | Liste ordonnée des mots suggérés (max 5 recommandé) |
| `root_detected` | `string \| null` | La racine utilisée pour la prédiction si différente du mot brut, sinon `null` |

---

## Codes de statut HTTP

| Code | Signification |
|------|---------------|
| `200` | Requête traitée avec succès |
| `422` | Paramètre manquant ou invalide (erreur de validation FastAPI) |
| `500` | Erreur interne du serveur |

---

## Notes pour le frontend

- Appeler `/check` à chaque **fin de mot** (détection de l'espace ou de la ponctuation) pour le soulignement en temps réel.
- Appeler `/autocomplete` à chaque **frappe de caractère** avec un debounce de **300ms** pour éviter de surcharger l'API.
- Appeler `/analyze` uniquement sur **clic droit ou sélection explicite** d'un mot.
- Appeler `/lemmatize` si l'équipe souhaite afficher la racine dans un panneau d'information dédié.