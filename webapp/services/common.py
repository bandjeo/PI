import os
import codecs
import re
import string

stopwords = ["баш","без","биће","био","бити","близу","број","дана","данас","доћи","добар","добити","док","доле","дошао","други","дуж","два","често","чији","где","горе","хвала","и","ићи","иако","иде","има","имам","имао","испод","између","изнад","изван","изволи","један","једини","једном","јесте","још","јуче","кад","како","као","кога","која","које","који","кроз","мали","мањи","мисли","много","моћи","могу","мора","морао","на","наћи","наш","негде","него","некад","неки","немам","нешто","није","ниједан","никада","нисмо","ништа","њега","његов","њен","њих","њихов","око","около","она","онај","они","оно","осим","остали","отишао","овако","овамо","овде","ове","ово","о","питати","почетак","поједини","после","поводом","правити","пре","преко","према","први","пут","радије","сада","смети","шта","ствар","стварно","сутра","сваки","све","свим","свугде","тачно","тада","тај","такође","тамо","тим", "у", "учинио","учинити","умало","унутра","употребити","узети","ваш","већина","веома","видео","више","захвалити","зашто","због","желео","жели","знати"]
dataset_path = './public/acts'
def find_law_title(file_name):
    
    TAG_RE = re.compile(r'<[^>]+>')

    with codecs.open('./public/acts/' + file_name, 'r', encoding='utf-8') as f:
        text = f.read()

    try:
        zakon_index = text.index('ЗАКОН')
        title="ЗАКОН "
    except:
        zakon_index = text.index('ПРАВИЛНИК')
        title="ПРАВИЛНИК "

    p_tag_index = text.index('<p>', zakon_index)
    p_close_index = text.index('</p>', p_tag_index)

    title += ' '.join(text[p_tag_index+3:p_close_index].split())

    text = TAG_RE.sub('', text)
    sample = ' '.join(text.split()[50:100])
    return (title, sample)

def load_dataset():
    dataset_path = './public/acts'
    dataset = {}
    TAG_RE = re.compile(r'<[^>]+>')
    for file_path in os.listdir(dataset_path):
        with codecs.open(os.path.join(dataset_path, file_path), 'r', encoding='utf-8') as f:
            data = f.read()
            data = data.lower() #lowercase
            data = TAG_RE.sub('', data) #remove html tags
            data = data.translate(str.maketrans('', '', string.punctuation + "„”")) #remove punctuation
            data_split = data.split() #remove extra whitespaces
            data_split = [word for word in data_split if word not in stopwords and not word.isnumeric()]
            dataset[file_path] = data_split

    return dataset
