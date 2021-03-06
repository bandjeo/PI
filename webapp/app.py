from flask import Flask, request, send_from_directory
import webapp.services.tfidf_service as tfidf_service
import webapp.services.elastic_service as elastic_service
import webapp.services.word2vec_service as word2vec_service
import webapp.services.doc2vec_service as doc2vec_service
import webapp.services.bert_service as bert_service
from webapp.services.common import find_law_title
from webapp.services.common import load_dataset
from webapp.services.common import dataset_path
app = Flask(__name__,  static_url_path='')

# dataset = load_dataset()

# print("Initializing bert model")
# bert_service.init_bert(dataset_path)
print("Initializing doc2vec model")
doc2vec_service.init_doc2vec(dataset_path)
# print("Initializing tfidf model")
# tfidf_service.init_tfidf(load_dataset())
# print("Initializing word2vec model")
# word2vec_service.init_word2vec(dataset_path)

@app.route('/')
def hello_world():
    return send_from_directory('public', 'index.html')

@app.route('/public/<path:path>')
def send_js(path):
    return send_from_directory('public', path)

@app.route('/tfidf/<query>')
def tfidf(query):
    file_names = tfidf_service.sorch([query])
    data = []
    for file_name in file_names:
        title, sample = find_law_title(file_name)
        data.append({
            'fileName': file_name,
            'title': title,
            'sample': sample
        })

    return { 'data': data}

@app.route('/word2vec/<query>')
def word2vec(query):
    file_names = word2vec_service.sorch(query)
    data = []
    for file_name in file_names:
        title, sample = find_law_title(file_name)
        data.append({
            'fileName': file_name,
            'title': title,
            'sample': sample
        })

    return { 'data': data}

@app.route('/doc2vec/<query>')
def doc2vec(query):
    file_names = doc2vec_service.sorch(query)
    data = []
    for file_name in file_names:
        title, sample = find_law_title(file_name)
        data.append({
            'fileName': file_name,
            'title': title,
            'sample': sample
        })

    return { 'data': data}

@app.route('/bert/<query>')
def bert(query):
    file_names = bert_service.sorch(query)
    data = []
    for file_name in file_names:
        title, sample = find_law_title(file_name)
        data.append({
            'fileName': file_name,
            'title': title,
            'sample': sample
        })

    return { 'data': data}

@app.route('/elastic/<query>')
def elastic(query):
    return { 'data': elastic_service.sorch(query) }


if __name__ == "__main__":
    app.run(debug=True)
