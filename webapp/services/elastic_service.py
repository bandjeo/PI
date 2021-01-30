import requests

def formatResult(doc):
    return {
        "fileName": doc['_source']['fileName'],
        'sample': ' '.join(doc['_source']['text'].split()[50:100]),
        'title': doc['_source']['title']
        }
def sorch(query):
    data = {
        "query":{
            "query_string":{
                "query": query
            }
        }
    }

    response = requests.post('http://localhost:9200/dokumenta/_search', json=data)
    retval = list(map(formatResult, response.json()['hits']['hits'][0:10]))
    return retval