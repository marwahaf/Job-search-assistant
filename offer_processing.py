import os
import re
import sys
from textwrap import dedent

from deep_translator import GoogleTranslator
from utils import clean_data, txt_to_json_dict

# Liste des sections possibles à extraire (thnks ChatGPT!)
titres_sections = [
    "Descriptif du poste",
    "Mission",
    "L'entreprise",
    "Profil recherche",
    "Contact",
    "Technologies",
    "Stack",
    "Competences",
    "Salaire",
    "Deroulement des entretiens",
    "Suite",
    "Lieu",
    "Avantages",
    "Type de contrat",
    "Niveau d'experience",
    "Profil souhaite",
    "Caracteristiques du poste",
    "Environnement de travail",
    "Evolution possible",
    "Processus de recrutement",
    "Langues requises",
    "Documents à fournir",
    "Date de debut souhaitee",
    "Remuneration",
    "Debut",
    "Lieu",
    "Experience",
]


def content_extraction(offer, dict_pos, sorted_dict):
    """
    Take a job offer as a string and extract the contents between each section title.

    Parameters
    ----------
    offer : str
        The job offer as a string.
    dict_pos : dict
        A dictionary with the section title as key and the position of the title as value.
    sorted_dict : list
        A list of section titles in the order they appear in the text.

    Returns
    -------
    dict
        A dictionary with the section title as key and the content between the section
        title and the next title as value.
    """
    offer_info = {}
    for i in range(len(sorted_dict) - 1):
        start_title = sorted_dict[i]
        end_title = sorted_dict[i + 1]

        # Récupérer les positions de départ et de fin
        # Ajoute la longueur du titre pour ne pas inclure le titre lui-même
        start_pos = dict_pos[start_title] + len(start_title)
        end_pos = dict_pos[end_title]

        # Extraire le contenu entre les positions
        content = offer[start_pos:end_pos].strip()

        # Clean the content
        content = clean_data(content)

        # Stocker le contenu dans le dictionnaire
        offer_info[start_title] = content.split("\n")

    # Extraire le contenu après le dernier titre
    last_title = sorted_dict[-1]
    last_start_pos = dict_pos[last_title] + len(last_title)
    last_content = offer[last_start_pos:].strip()

    offer_info[last_title] = last_content.split("\n")
    return offer_info


def offer_cleaning(offer):
    """
    Clean an offer text by removing special characters, translating any non-French text into French, and normalizing accents.

    Args:
        offer (str): The offer text to be cleaned.

    Returns:
        str: The cleaned offer text.
    """
    offer = dedent(offer)
    offer = "\n".join(
        re.sub(r"[^a-zA-Z0-9éèàùâêîôûçëïüœæÉÈÀÙÂÊÎÔÛÇËÏÜŒÆ€$£#+\-_\s’']", " ", word)
        for word in offer.split("\n")
    )

    # Remove unwanted space before punctuation
    offer = re.sub(r"[.,;!?()] ", "", offer)

    # Cheking the offer for other languages other than french and translating it
    segments = re.split("\n", offer)
    offer = " ".join(
        GoogleTranslator(source="auto", target="fr").translate(segment)
        for segment in segments
        if segment
    )
    offer = re.sub(r"[éè]", "e", offer)
    return offer


def process_job_offer(output_path):
    """
    Read a job offer from stdin, clean it, extract the contents between sections based on a predefined list of titles, and write the result to a JSON file.

    Parameters
    ----------
    output_path : str
        The path where the JSON file will be written.

    Returns
    -------
    None
    """
    print(
        "Collez le texte, puis appuyez sur Ctrl+D (Linux/macOS) ou Ctrl+Z puis Entrée (Windows) :"
    )
    offer = sys.stdin.read()

    # First Formatting of the offer
    offer = offer_cleaning(offer)

    # Finding titles of section based on the list given  - might need to be modified dynamically ?
    dict_pos = {}
    for titre in titres_sections:
        # pattern = re.compile(rf"(^|\n){re.escape(titre)}(\s*:)?", re.MULTILINE)
        match = re.search(titre, offer)
        if match:
            found_title = match.group()
            start_pos = match.start()
            dict_pos[found_title] = start_pos

    # Sort the titles of section based on their position in the text
    sorted_dict = list(dict(sorted(dict_pos.items(), key=lambda item: item[1])).keys())

    # Extract the contents between the titles
    offer_info = content_extraction(offer, dict_pos, sorted_dict)

    # Create a JSON file
    offer_path = os.path.join(output_path, "job_offer.json")
    txt_to_json_dict(offer_path, offer, sorted_dict, offer_info)
