import os
import json
import codecs

engine_results = {}
human_rankings = []
dataset = []


for path in os.listdir('./engine_results'):
    with codecs.open('./engine_results/' + path, 'r', encoding='utf-8') as engine_result_file:
        results = json.loads(engine_result_file.read())
        engine_results[results['query']] = results

for path in os.listdir('./human_rankings'):
    with codecs.open('./human_rankings/' + path, 'r', encoding='utf-8') as human_ranking_file:
        ranking = json.loads(human_ranking_file.read())
        human_rankings.append(ranking)


for ranking in human_rankings:
    entry = engine_results[ranking['query']]
    entry['human_ranking'] = ranking['lista']
    dataset.append(entry)


def spearman_precision(truth, results):
    distances = []
    for i, result in enumerate(results):
        if result in truth:
            distance = abs(truth.index(result) - i)
            distances.append(distance^2)
        else:
            distances.append(len(truth)^2)
    n = len(distances)
    if n <= 1:
        return 0

    return round(3 - (6*sum(distances)/(n * (n^2 - 1))), 2)

engines = ['bert', 'elastic', 'w2v', 'd2v', 'tfidf']
header = ['query', 'bert', 'elastic', 'w2v', 'd2v', 'tfidf']

to_write = [header]
precisions_to_write = [header]

total_numbers_found = {'bert': 0, 'elastic': 0, 'w2v': 0, 'd2v': 0, 'tfidf': 0}
engine_precisions = {'bert': [], 'elastic': [], 'w2v': [], 'd2v': [], 'tfidf': []}

total_results = 0

for entry in dataset:
    row = [entry['query']]
    precisions_row = [entry['query']]
    
    total = len(entry['human_ranking'])

    for engine in engines:
        engine_results = entry['result_' + engine]
        number_found = 0
        for result in engine_results:
            if result['fileName'] in entry['human_ranking']:
                number_found += 1
        row.append(str(round(number_found/total, 2)))
        total_numbers_found[engine] += number_found

        precision = spearman_precision(entry['human_ranking'], [result['fileName'] for result in engine_results])
        precisions_row.append(str(precision))
        engine_precisions[engine].append(precision)
    to_write.append(row)
    precisions_to_write.append(precisions_row)
    total_results += total


recalls_f = codecs.open('recall.csv', 'w', encoding='utf-8')
recalls_f.write('\n'.join([','.join(line) for line in to_write]))
recalls_f.close()

total_recalls_f = codecs.open('total_recall.csv', 'w', encoding='utf-8')
total_recalls_f.write('\n'.join([','.join([engine, str(round(found/total_results, 2))]) for engine, found in total_numbers_found.items()]))
total_recalls_f.close()



precision_f = codecs.open('precision.csv', 'w', encoding='utf-8')
precision_f.write('\n'.join([','.join(line) for line in precisions_to_write]))
precision_f.close()

total_precision_f = codecs.open('total_precision.csv', 'w', encoding='utf-8')
total_precision_f.write('\n'.join([','.join([engine, str(round(sum(precisions)/len(precisions), 2))]) for engine, precisions in engine_precisions.items()]))
total_precision_f.close()

    

