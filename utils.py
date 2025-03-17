import json
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("wordnet")


def clean_data(content):
    # Convert to lowercase
    content = content.lower()

    # No stopwords ("the", "a", "is"…)
    stop_words = set(stopwords.words("french"))

    # Lemmatisation/stemmatisation
    lemmatizer = WordNetLemmatizer()
    content = " ".join(
        [
            lemmatizer.lemmatize(word)
            for word in content.split(" ")
            if word not in stop_words
        ]
    )

    return content


def txt_to_json_dict(output_path, string_text, sections, dict_info):
    """
    Take a string of text and output a JSON file with the extracted info.

    Parameters
    ----------
    output_path : str
        The path to the output file.
    string_text : str
        The string of text to extract the information from.

    Notes
    -----
    The sections are extracted using regular expressions so the order is important.
    """

    for section in sections:
        dict_info[section] = []

    # Utilisation des regex pour extraire les sections
    for i in range(len(sections) - 1):
        # Capture entre deux sections
        pattern = rf"{sections[i]}(.*?){sections[i + 1]}"
        match = re.search(pattern, string_text, re.DOTALL)
        if match:
            content = match.group(1).strip().split("\n")
            dict_info[sections[i]] = [
                clean_data(line).strip() for line in content if line.strip()
            ]

    # Récupération de la dernière section (pas de sections[i + 1])
    last_section = sections[-1]
    pattern = rf"{last_section}(.*)"
    match = re.search(pattern, string_text, re.DOTALL)
    if match:
        content = match.group(1).strip().split("\n")
        dict_info[last_section] = [
            clean_data(line).strip() for line in content if line.strip()
        ]

    # Convert and write JSON object to file
    with open(output_path, "w") as outfile:
        json.dump(dict_info, outfile, indent=4, ensure_ascii=False)
