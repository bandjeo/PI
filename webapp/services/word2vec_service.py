import os
import codecs
import re
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from gensim.test.utils import common_texts
from webapp.services.common import stopwords
import torch

from gensim.models import Word2Vec

corpus = None
model = None
embeddings = None
corpus_clans = None
dataset = {}
TAG_RE = re.compile(r'<[^>]+>')

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

def init_word2vec(dataset_path):
    global model, dataset, corpus, embeddings, corpus_clans

    corpus, dataset, corpus_clans = load_dataset(dataset_path)
    sentences = [clan.split(" ") for zakon in corpus for clan in zakon]
    model = Word2Vec(sentences=sentences, size=300, window=5, min_count=1, workers=4)
    
    # # #####################################
    # # MANUALLY DOING EMBEDDINGS
    # # #####################################
    embeddings = dataset_to_vectors(dataset, model)
    # # #####################################
    # # LOADING EMBEDDINGS
    # # #####################################
    # with open(f'{dataset_path}/../embeddings/sorted_word2vec_embeddings.wv', 'rb') as embeddings_file:
    #     embeddings = torch.load(embeddings_file)

def dataset_to_vectors(dataset, model):
    """Returns dataset vectorized. Doesn't change the dataset"""
    X = []
    from tqdm import tqdm
    for key, clans in tqdm(dataset.items()):
        try:
            clans_embedding = [query_to_vec(clan, model) for clan in clans]
        except ValueError:
            clans_embedding = [[]]
        X.append(clans_embedding)
    print(len(X))
    return X

def query_to_vec(query, model):
    query = query.lower() #lowercase
    query = TAG_RE.sub('', query) #remove html tags
    query = query.translate(str.maketrans('', '', string.punctuation + "„”")) #remove punctuation
    query_split = query.split() #remove extra whitespaces
    query_split = [word for word in query_split if word not in stopwords and not word.isnumeric()]
    wordvecs = []
    for word in query_split:
        try:
            wordvecs.append(model.wv[word])
        except KeyError:
#             print(f'{word} not in vocabulary')
            continue
    if wordvecs:
        wordvecs_mean = np.array(wordvecs).sum(axis=0) / float(len(wordvecs))
        return wordvecs_mean
    else:
        raise ValueError('No words from the query are present in the model vocabulary') 


def calculate_similarity(embeddings, model, query, top_documents=10, top_sentences=3):
    """ Embeds the `query` via `model` and calculates the cosine similarity of
    the `query` and `X` (all the documents) and returns the `top_k` similar documents."""

    # Vectorize the query to the same length as sentences in documents
    query_vec = query_to_vec(query, model)
    query_vec = query_vec.reshape(1,-1)
    # Compute the cosine similarity between query_vec and all the documents
    scores = np.array([])
    top_sentence_indices = []
    for i, zakon_embedding in enumerate(embeddings):
        if len(zakon_embedding[0]) > 0:
            cosine_scores = cosine_similarity(query_vec, zakon_embedding)[0]
        else:
            cosine_scores = np.array([0.])
        indices_best = cosine_scores.argsort()[-1:-top_sentences-1:-1]
        scores = np.append(scores, cosine_scores[indices_best].mean())
        top_sentence_indices.append(indices_best)
    # Sort the similar documents from the most similar to less similar and return the indices
    most_similar_doc_indices = np.argsort(scores, axis=0)[-1:-top_documents-1:-1].astype(int)
    top_sentence_indices = np.array(top_sentence_indices)[most_similar_doc_indices]
    return (most_similar_doc_indices, scores, top_sentence_indices)

def show_similar_documents(df, cosine_similarities, similar_doc_indices, corpus, similar_doc_sentence_indices):
    """ Prints the most similar documents using indices in the `similar_doc_indices` vector."""
    counter = 1
    results = []

    for i, index in enumerate(similar_doc_indices):
        print('Top-{}, Similarity = {}'.format(counter, cosine_similarities[index]))
        print('body: {}, '.format(df[index]))
        print('Most similar articles: ')
        for jandex in similar_doc_sentence_indices[i]:
            print(f'\t{corpus[index][jandex]}')
        print()
        counter += 1        
        results.append(df[index])
    return results


def load_dataset(dataset_path):
    clan_re = re.compile("<p>[ \t\n]*Члан[ \t\n]*[0-9]*\..*?<\/p>")
    #using this one to load the dataset instead
    start = time.time()
    dataset = {}
    TAG_RE = re.compile(r'<[^>]+>')
    corpus_clans = []
    for file_path in sorted(os.listdir(dataset_path)):
        with codecs.open(os.path.join(dataset_path, file_path), 'r', encoding='utf-8') as f:
            data = f.read()
            clans = clan_re.split(data)
            clans_no_html = [TAG_RE.sub('', clan) for clan in clans] #remove html tags
            clans_no_white_spaces = [' '.join(clan.split()) for clan in clans_no_html]
            corpus_clans.append(clans_no_white_spaces)
            clans_no_punc = (clan.translate(str.maketrans('', '', string.punctuation + "„”–vi")) for clan in clans_no_white_spaces) #remove punctuation
            clans_lower = [clan.lower() for clan in clans_no_punc] #lowercase
            clans_no_stopwords = []
            for i, clan in enumerate(clans_lower):
                new_clan = clan.split()
                new_clan = [word for word in new_clan if word not in stopwords and not hasNumbers(word)]
                new_clan = ' '.join(new_clan)
                clans_no_stopwords.append(new_clan)
    #         data = [row_clean for row in data if (row_clean := " ".join(row.split())) != ''] #remove extra whitespaces
            clans_clean = [" ".join(clan.split()) for clan in clans_no_stopwords] #remove extra whitespaces
            clans_cut = [clan[:500000] for clan in clans_clean]
            dataset[file_path] = clans_cut
    end = time.time()
    corpus = list(dataset.values())
    return corpus, dataset, corpus_clans

def sorch(query):
    top_documents = 10
    top_sentences = 3
    search_start = time.time()
    sim_vecs, cosine_similarities, top_sentence_indices = calculate_similarity(embeddings, 
                                                                           model, 
                                                                           query, 
                                                                           top_documents=top_documents,
                                                                           top_sentences=top_sentences)    
    search_time = time.time() - search_start
    print("search time: {:.2f} ms".format(search_time * 1000))
    print()
    return show_similar_documents(list(dataset.keys()), cosine_similarities, sim_vecs, corpus_clans, top_sentence_indices)