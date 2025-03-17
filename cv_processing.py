import os

import matplotlib.pyplot as plt
import numpy as np
import pymupdf
from utils import txt_to_json_dict


def extract_text(blocks):
    """
    Extract the text from the given blocks.

    This function assumes that the CV is divided in two columns and
    uses a histogram to find the threshold of separation between the two
    columns.

    Parameters
    ----------
    blocks: list of pymupdf.Block
        The blocks to extract the text from

    Returns
    -------
    list of pymupdf.Block
        The sorted blocks
    """
    x = [x[0] for x in blocks]
    counts, bins, _ = plt.hist(x)  # bins contains the edges of the bars
    # plt.show()

    # Non zero values of hist
    indexes = np.argwhere(counts != 0).flatten()

    # Midpoint between the two main bars
    threshold = (bins[indexes[0] + 1] + bins[indexes[1]]) / 2

    print(f"Threshold: {threshold}")

    blocks_sorted_left = [x for x in blocks if x[0] < threshold]
    blocks_sorted_right = [x for x in blocks if x[0] >= threshold]

    # Sort blocks vertically
    blocks_sorted_left = sorted(blocks_sorted_left, key=lambda x: x[1])
    blocks_sorted_right = sorted(blocks_sorted_right, key=lambda x: x[1])

    final_sorted_blocks = blocks_sorted_right + blocks_sorted_left
    return final_sorted_blocks


def process_cv(input_path, output_path, sections):
    """
    Process a CV PDF file and extract the information to a JSON file.

    Parameters
    ----------
    input_path : str
        The path to the input PDF file.
    output_path : str
        The path to the output directory.
    sections : list of str
        The sections to extract from the PDF file.

    Notes
    -----
    The sections are extracted using regular expressions so the order is important.
    """
    # open a document
    doc = pymupdf.open(input_path)

    # create a text output
    text_path = open(os.path.join(output_path, "raw_cv_output.txt"), "wb")
    json_path = os.path.join(output_path, "cv_formatted.json")

    # Initializing variables
    dict_info = {"Name": "Marwa HAFSI"}
    string_text = ""

    # Extracting words from pdf
    blocks = []
    # Iterate the document pages
    for page in doc:
        blocks += page.get_text(
            "blocks"
        )  # Liste de tuples (x0, y0, x1, y1, texte, ...)

    #  Extract the text from the given blocks in an ordered manner!
    final_sorted_blocks = extract_text(blocks)

    # Extract text from the sorted blocks and write to output file
    for block in final_sorted_blocks:
        string_text += block[4].encode().decode("utf-8")
        text_path.write(block[4].encode())  # Writing the text (index 4 in the tuple)
        text_path.write(b"\n")  # Adding newlines for separation of lines
    text_path.close()

    txt_to_json_dict(json_path, string_text, sections, dict_info)
