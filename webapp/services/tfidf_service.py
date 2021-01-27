import os
import codecs
import re
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataset_path = './public/acts'

def sorch(query):
    dataset = {}
    TAG_RE = re.compile(r'<[^>]+>')
    for file_path in os.listdir(dataset_path):
        with codecs.open(os.path.join(dataset_path, file_path), 'r', encoding='utf-8') as f:
            data = f.read()
            data = TAG_RE.sub('', data)
            data = " ".join(data.split())
            dataset[file_path] = data

    corpus = list(dataset.values())
    X, tf_idf_vectorizer = create_tfidf_features(corpus)

    
    search_start = time.time()
    sim_vecs, cosine_similarities = calculate_similarity(X, tf_idf_vectorizer, query)
    search_time = time.time() - search_start
    print("sorch time: {:.2f} ms".format(search_time * 1000))
    print()
    return show_similar_documents(list(dataset.keys()), cosine_similarities, sim_vecs)
     

def create_tfidf_features(corpus, max_features=5000):
    """ Creates a tf-idf matrix for the `corpus` using sklearn. """
    tfidf_vectorizor = TfidfVectorizer(decode_error='strict', 
                                       analyzer='word', encoding='utf-8', norm='l2', 
                                       use_idf=True, smooth_idf=True, sublinear_tf=True,
                                       )
    X = tfidf_vectorizor.fit_transform(corpus)
    print('tfidf matrix successfully created.')
    return X, tfidf_vectorizor

def calculate_similarity(X, vectorizor, query, top_k=10):
    """ Vectorizes the `query` via `vectorizor` and calculates the cosine similarity of
    the `query` and `X` (all the documents) and returns the `top_k` similar documents."""

    # Vectorize the query to the same length as documents
    query_vec = vectorizor.transform(query)
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