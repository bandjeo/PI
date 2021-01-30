import os
import codecs
import re

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
