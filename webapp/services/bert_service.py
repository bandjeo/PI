from sentence_transformers import SentenceTransformer, util
import torch
import os
import codecs
import re
import time
import numpy as np
import string

from webapp.services.common import stopwords

from tqdm import tqdm
model = None
corpus = None
dataset = None
embeddings = None
corpus_clans = None

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

def init_bert(dataset_path):
    global embeddings, corpus, dataset, corpus_clans, model
    model_cpu = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')
    model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))

    corpus, dataset, corpus_clans = load_dataset(dataset_path)

    # # #####################################
    # # MANUALLY DOING EMBEDDINGS
    # # #####################################
    # embeddings = []
    # # corpus2 = corpus[:50] + corpus[51:]
    # # zakon_embedding = model.encode(corpus, convert_to_tensor=True, show_progress_bar=True)
    # for counter, zakon in enumerate(tqdm(corpus)):
    # #     print(f"{counter} len: {len(zakon)}, type: {type(zakon)}")
    #     zakon_embedding = model.encode(zakon, convert_to_tensor=True)
    #     embeddings.append(zakon_embedding)
    # # #####################################
    # # LOADING EMBEDDINGS
    # # #####################################
    with open(f'{dataset_path}/../embeddings/sorted_berto_embeddings.pt', 'rb') as embeddings_file:
        embeddings = torch.load(embeddings_file)


def calculate_similarity(X, model, query, top_documents=10, top_sentences=3):
    """ Embeds the `query` via `model` and calculates the cosine similarity of
    the `query` and `X` (all the documents) and returns the `top_k` similar documents."""

    # Vectorize the query to the same length as documents
    query_vec = model.encode(query, convert_to_tensor=True)
    # Compute the cosine similarity between query_vec and all the documents
    scores = np.array([])
    top_sentence_indices = []
    for i,corpus_embedding in enumerate(embeddings):   
        cosine_scores = util.pytorch_cos_sim(query_vec, corpus_embedding)
        scores = np.append(scores, torch.sort(cosine_scores).values[0].numpy()[-1:-top_sentences-1:-1].mean())
        top_sentence_indices.append(torch.sort(cosine_scores).indices[0].numpy()[-1:-top_sentences-1:-1])
    # Sort the similar documents from the most similar to less similar and return the indices
    most_similar_doc_indices = np.argsort(scores, axis=0)[:-top_documents-1:-1].astype(int)
    top_sentence_indices = np.array(top_sentence_indices)
    return (most_similar_doc_indices, scores, top_sentence_indices[most_similar_doc_indices])

def show_similar_documents(df, cosine_similarities, similar_doc_indices, corpus, similar_doc_sentence_indices):
    """ Prints the most similar documents using indices in the `similar_doc_indices` vector."""
    counter = 1
    results = []
    print(similar_doc_indices)
    print(similar_doc_sentence_indices)
    for i, index in enumerate(similar_doc_indices):
        print('Top-{}, Similarity = {}'.format(counter, cosine_similarities[index]))
        print('body: {}, '.format(df[index]))
        print('Most similar articles: ')
        for jandex in similar_doc_sentence_indices[i]:
            print(f'\t\t[{len(corpus[229])}')
            print(f'\t{corpus[index][jandex]}')
        print()
        counter += 1
        results.append(df[index])

    return results
    

def load_dataset(dataset_path):
    clan_re = re.compile("<p>[ \t\n]*Члан[ \t\n]*[0-9]*\..*?<\/p>")
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
    print(len(corpus))
    return corpus, dataset, corpus_clans


def sorch(query):
    search_start = time.time()
    top_documents = 10
    top_sentences = 3
    user_question = [
        query
    ]
    sim_vecs, cosine_similarities, top_sentence_indices = calculate_similarity(embeddings, 
                                                                           model, 
                                                                           user_question, 
                                                                           top_documents=top_documents,
                                                                           top_sentences=top_sentences)
    search_time = time.time() - search_start
    print("search time: {:.2f} ms".format(search_time * 1000))
    print()
    return show_similar_documents(list(dataset.keys()), cosine_similarities, sim_vecs, corpus_clans, top_sentence_indices)