
import os
dataset_path = '../public/acts'


import torch

ucitanalista = []

with open('../neucitanalist.txt', 'r') as f:
    for i in f:
        ucitanalista.append(i)
print(ucitanalista)

with open('../public/acts/../embeddings/berto_embeddings.pt', 'rb') as embeddings_file:
    embeddings = torch.load(embeddings_file)

watever, embeddings = zip(*sorted(zip(ucitanalista, embeddings )))

with open('../public/acts/../embeddings/sorted_berto_embeddings.pt', 'wb') as sorted_embeddings_file:

    torch.save(embeddings, sorted_embeddings_file)


with open('../public/acts/../embeddings/doc2vec_embeddings.dv', 'rb') as embeddings_file:
    embeddings = torch.load(embeddings_file)

watever, embeddings = zip(*sorted(zip(ucitanalista, embeddings )))

with open('../public/acts/../embeddings/sorted_doc2vec_embeddings.dv', 'wb') as sorted_embeddings_file:

    torch.save(embeddings, sorted_embeddings_file)


with open('../public/acts/../embeddings/word2vec_embeddings.wv', 'rb') as embeddings_file:
    embeddings = torch.load(embeddings_file)

watever, embeddings = zip(*sorted(zip(ucitanalista, embeddings )))

with open('../public/acts/../embeddings/sorted_word2vec_embeddings.wv', 'wb') as sorted_embeddings_file:

    torch.save(embeddings, sorted_embeddings_file)
