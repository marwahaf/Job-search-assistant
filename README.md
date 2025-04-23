# Job Search Assistant

Une application Python conçue pour automatiser le traitement de CV et d'offres d'emploi, facilitant ainsi le processus de recherche d'emploi.

## Fonctionnalités

- **Extraction de texte** : Utilisation de PyMuPDF pour extraire le contenu textuel des fichiers PDF (CV et offres d'emploi).
- **Nettoyage et prétraitement** : Nettoyage des textes extraits pour éliminer les caractères spéciaux et les informations non pertinentes.
- **Vectorisation TF-IDF** : Transformation des textes en vecteurs numériques à l'aide de la méthode TF-IDF pour permettre la comparaison.
- **Matching CV-offre** : Calcul de la similarité entre les vecteurs de CV et d'offres d'emploi pour identifier les correspondances les plus pertinentes.
- **Analyse des résultats** : Génération de scores de correspondance et classement des offres en fonction de leur pertinence par rapport au CV.

## Structure du projet

- `main.py` : Point d'entrée principal de l'application.
- `cv_processing.py` : Fonctions pour le traitement et la vectorisation des CV.
- `offer_processing.py` : Fonctions pour le traitement et la vectorisation des offres d'emploi.
- `matching_cv_offer.py` : Fonctions pour le calcul de similarité et le matching entre CV et offres.
- `utils.py` : Fonctions utilitaires pour le nettoyage et le prétraitement des textes.
- `dataset/` : Répertoire contenant les fichiers de CV et d'offres d'emploi à analyser.
- `output/` : Répertoire pour stocker les résultats de l'analyse.

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/marwahaf/Job-search-assistant.git
   cd Job-search-assistant
   ```
2. Créer un environnement virtuel (optionnel mais recommandé) :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```


## Utilisation

1. Placer les fichiers PDF des CV dans le répertoire `dataset/cv/`.
2. Placer les fichiers PDF des offres d'emploi dans le répertoire `dataset/offers/`.
3. Exécuter le script principal :
   ```bash
   python main.py
   ```
4. Les résultats seront générés dans le répertoire `output/`, avec des scores de correspondance pour chaque paire CV-offre.
   
## Concepts techniques
### 📄 Extraction PDF avec PyMuPDF

[PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) est une bibliothèque Python performante pour :
- l’extraction de texte,
- la manipulation de documents PDF (et autres formats),
- l’analyse et la conversion de contenu.

Elle permet d’accéder finement au contenu textuel des CV et offres, même dans des mises en page complexes.

> 📌 PyMuPDF est disponible sur [PyPI](https://pypi.org/project/PyMuPDF/) et [GitHub](https://github.com/pymupdf/PyMuPDF).

---
### 🔎 Nettoyage de texte avec Regex

Les expressions régulières (Regex) sont utilisées pour :
- nettoyer les caractères spéciaux,
- standardiser le contenu textuel.

📚 Référence officielle : [Howto Regex – Python](https://docs.python.org/3/howto/regex.html)

---
### 🧠 Vectorisation des textes avec TF-IDF

TF-IDF (Term Frequency – Inverse Document Frequency) est une méthode courante pour représenter des documents texte sous forme de vecteurs pondérés.

**1. Term Frequency (TF)**  
Mesure la fréquence d’un mot dans un document.  
Plus un mot est fréquent, plus il est considéré comme pertinent pour ce document.  
> ⚠️ Limite : ne reflète pas l'importance globale du mot dans le corpus.

**2. Inverse Document Frequency (IDF)**  
Réduit l’importance des mots courants (comme “le”, “et”) en pondérant davantage les mots rares.  
> ⚠️ Limite : ne tient pas compte de la fréquence locale du mot dans le document.

**TF-IDF = TF × IDF**  
Une combinaison qui équilibre pertinence locale et spécificité globale.

---
### 📊 Clustering pour structurer les CV

Plutôt que de supposer une structure fixe dans les CV (ex : 2 sections), une approche non supervisée comme le **clustering** permet de :
- grouper les blocs de texte similaires,
- détecter automatiquement des parties comme les expériences, les compétences, etc.

Technique explorée : [Unsupervised Clustering](https://builtin.com/articles/unsupervised-clustering)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com/marwahaf/Job-search-assistant/blob/main/LICENSE) pour plus de détails.
