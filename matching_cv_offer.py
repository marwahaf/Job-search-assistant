import json
import os

import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import FlaubertModel, FlaubertTokenizer

pyfile_path = os.path.abspath(__file__)
directory = os.path.dirname(pyfile_path)
output_path = os.path.join(directory, "output")

# Define the offer and the CV content
with open(os.path.join(output_path, "cv_formatted.json"), "r") as file:
    cv_content = json.load(file)
    per_ligne = [
        title + "\n" + "\n".join(content) for title, content in cv_content.items()
    ]
    cv_content = " ".join(per_ligne)

with open(os.path.join(output_path, "job_offer.json"), "r") as file:
    offer = json.load(file)
    per_ligne = [title + "\n" + "\n".join(content) for title, content in offer.items()]
    offer = " ".join(per_ligne)

print("CV:")
print(" ")
print(cv_content)

print("offer:")
print(" ")
print(offer)

## Methode 1 : tf-idf
# import required modules

# merge documents into a single corpus
string = [offer, cv_content]

# create object
tfidf = TfidfVectorizer()

# get tf-df values
result = tfidf.fit_transform(string)

# get idf values
print("\nidf values:")
for ele1, ele2 in zip(tfidf.get_feature_names_out(), tfidf.idf_):
    print(ele1, ":", ele2)

# get indexing
print("\nWord indexes:")
print(tfidf.vocabulary_)

# display tf-idf values
print("\ntf-idf value:")
print(result)

# in matrix form
print("\ntf-idf values in matrix form:")
print(result.toarray())

similarity = cosine_similarity(result[0], result[1])
print(f"Cosine Similarity between documents: {similarity[0][0]}")

## Methode 2 :  Using FlauBERT with Hugging Face's Transformers

# Choose among ['flaubert/flaubert_small_cased', 'flaubert/flaubert_base_uncased',
#               'flaubert/flaubert_base_cased', 'flaubert/flaubert_large_cased']
model_name = "flaubert/flaubert_base_uncased"

# Load pretrained model and tokenizer
model, log = FlaubertModel.from_pretrained(model_name, output_loading_info=True)
tokenizer = FlaubertTokenizer.from_pretrained(model_name, do_lowercase=True)
# do_lowercase=False if using cased models, True if using uncased ones
print("Tokenizer loaded successfully!")

# Ensure the model is on CPU
model = model.to("cpu")

sentence = offer
token_ids = torch.tensor([tokenizer.encode(sentence, max_length=512, truncation=True)])
last_layer = model(token_ids)[0]
offer_embedding = last_layer[:, 0, :]

sentence = cv_content
token_ids = torch.tensor([tokenizer.encode(sentence, max_length=512, truncation=True)])
last_layer = model(token_ids)[0]
cv_embedding = last_layer[:, 0, :]

# Compute cosine similarity
similarity_score = cosine_similarity(
    offer_embedding.detach().numpy(), cv_embedding.detach().numpy()
)
print(f"Cosine Similarity between offer and CV: {similarity_score[0][0]}")
