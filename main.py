import os

from cv_processing import process_cv
from offer_processing import process_job_offer


def main():
    # Paths
    pyfile_path = os.path.abspath(__file__)
    directory = os.path.dirname(pyfile_path)
    input_path = os.path.join(directory, "dataset", "cv_marwa_hafsi.pdf")
    output_path = os.path.join(directory, "output")

    sections = [
        "Marwa HAFSI",
        "Experience Professionnelle",
        "Compétences techniques",
        "Contact",
        "Formation",
        "Compétences",
        "Certifications",
        "Langues",
        "Centres d'intérêts",
    ]

    # Step 1: Process the CV
    process_cv(input_path, output_path, sections)

    # Step 2: Process the Job Offer
    process_job_offer(output_path)

    print("Data Cleaning done!")


if __name__ == "__main__":
    main()
