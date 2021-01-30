import os
import codecs
import re
import time
import requests


dataset_path = '../webapp/public/acts'
dataset = []

# DATA_RE = re.compile(r'[0-9]* од [0-9]*. (јануара|фебруара|марта|априла|маја|јуна|јула|августа|септембра|октобра|новембра|децембра) [0-9]*')
TAG_RE = re.compile(r'<[^>]+>')


for file_path in os.listdir(dataset_path):
    with codecs.open(os.path.join(dataset_path, file_path), 'r', encoding='utf-8') as f:
        data = f.read()
        # dates = []
        # for i in DATA_RE.finditer(data):
        #     dates.append({'rbr': })
        try:
            zakon_index = data.index('ЗАКОН')
            title="ЗАКОН "
        except:
            zakon_index = data.index('ПРАВИЛНИК')
            title="ПРАВИЛНИК "
        p_tag_index = data.index('<p>', zakon_index)
        p_close_index = data.index('</p>', p_tag_index)
        title += ' '.join(data[p_tag_index+3:p_close_index].split())

        data = TAG_RE.sub('', data)
        data = " ".join(data.split())
        
        dataset.append({'fileName': file_path, 'text': data, 'title': title})

requests.delete('http://localhost:9200/dokumenta')
requests.put('http://localhost:9200/dokumenta')
curid = 1
for i in dataset:
    x = requests.post('http://localhost:9200/dokumenta/_doc/'+str(curid), json = i)
    # print(str(x.text))
    print(str(curid) + "/" + str(len(dataset)) + " has finished creating itself inside of the esdbmrcmon!...!")
    curid+=1
