# Job-search-assistant


PyMuPDF is a high-performance Python library for data extraction, analysis, conversion & manipulation of PDF (and other) documents.

PyMuPDF is hosted on GitHub and registered on PyPI.

REGEX : 
https://docs.python.org/3/howto/regex.html

How TF-IDF Works?

TF-IDF combines two components: Term Frequency (TF) and Inverse Document Frequency (IDF).

Term Frequency (TF): Measures how often a word appears in a document. A higher frequency suggests greater importance. If a term appears frequently in a document, it is likely relevant to the document’s content. Formula:
The-TF-Formula ==

Term Frequency (TF)

Limitations of TF Alone:

    TF does not account for the global importance of a term across the entire corpus.
    Common words like “the” or “and” may have high TF scores but are not meaningful in distinguishing documents.

Inverse Document Frequency (IDF): Reduces the weight of common words across multiple documents while increasing the weight of rare words. If a term appears in fewer documents, it is more likely to be meaningful and specific. Formula:
IDF-Formula ==

Inverse Document Frequency (IDF)

    The logarithm is used to dampen the effect of very large or very small values, ensuring the IDF score scales appropriately.
    It also helps balance the impact of terms that appear in extremely few or extremely many documents.

Limitations of IDF Alone:

    IDF does not consider how often a term appears within a specific document.
    A term might be rare across the corpus (high IDF) but irrelevant in a specific document (low TF).


ANalysing the PDF cv by clustering it ! instead of assuming it has 2 secytions 
https://builtin.com/articles/unsupervised-clustering

