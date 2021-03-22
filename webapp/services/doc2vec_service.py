import os
import codecs
import re
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from gensim.test.utils import common_texts

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from webapp.services.common import stopwords

X, model, dataset = None, None, {}

TAG_RE = re.compile(r'<[^>]+>')

def init_doc2vec(common_dataset):
    global X, model, dataset
    dataset = common_dataset
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list(x[:] for x in dataset.values()))]
    model = Doc2Vec(documents, vector_size=100, negative=0, window=2, min_count=1, workers=4)

    X = dataset_to_vectors(dataset, model)

def dataset_to_vectors(dataset, model):
    for key, value in dataset.items():
        dataset[key] = model.infer_vector(value)
    X = list(dataset.values())
    return X

def query_to_vec(query, model):
    query = query.lower() #lowercase
    query = TAG_RE.sub('', query) #remove html tags
    query = query.translate(str.maketrans('', '', string.punctuation + "„”")) #remove punctuation
    query_split = query.split() #remove extra whitespaces
    query_split = [word for word in query_split if word not in stopwords and not word.isnumeric()]
    docvec = model.infer_vector(query_split)
    return docvec


def calculate_similarity_word2vec(X, model, query, top_k=10):
    """ Vectorizes the `query` via `query_to_vec` and calculates the cosine similarity of
    the `query` and `X` (all the documents) and returns the `top_k` similar documents."""

    # Vectorize the query to the same length as documents
    query_vec = query_to_vec(query, model)
    query_vec = query_vec.reshape(1,-1)
    # Compute the cosine similarity between query_vec and all the documents
    cosine_similarities = cosine_similarity(X,query_vec).flatten()
    # Sort the similar documents from the most similar to less similar and return the indices
    most_similar_doc_indices = np.argsort(cosine_similarities, axis=0)[:-top_k-1:-1]
    return (most_similar_doc_indices, cosine_similarities)


def show_similar_documents(df, cosine_similarities, similar_doc_indices):
    """ Prints the most similar documents using indices in the `similar_doc_indices` vector."""
    counter = 1
    results = []
    for index in similar_doc_indices:
        print('Top-{}, Similarity = {}'.format(counter, cosine_similarities[index]))
        print('body: {}, '.format(df[index]))
        print()
        counter += 1
        results.append(df[index])

    return results


def sorch(query):
    search_start = time.time()
    sim_vecs, cosine_similarities = calculate_similarity_word2vec(X, model, query)
    search_time = time.time() - search_start
    print("search time: {:.2f} ms".format(search_time * 1000))
    print()
    return show_similar_documents(list(dataset.keys()), cosine_similarities, sim_vecs)