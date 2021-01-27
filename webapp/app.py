from flask import Flask, request, send_from_directory
import webapp.services.tfidf_service as tfidf_service
from webapp.services.common import find_law_title
app = Flask(__name__,  static_url_path='')

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

if __name__ == "__main__":
    app.run(debug=True)
