import re
from yd_dict import query
from enum import Enum

class NameStyle(Enum):
    UPPER = 1
    LOWER = 2
    UNDERLINE = 3

def translate(word : str) -> str:
    result = query(word)
    meaning = result['translation']
    if meaning:
        meaning = meaning[0]
    else:
        meaning = 'null'
    return meaning

def cn_to_en(word : str, nameStyle : NameStyle) -> str:
    result = translate(word).lower()
    if nameStyle == NameStyle.LOWER:
        result = result[0] + result.title().replace(' ', '')[1:]
    elif nameStyle == NameStyle.UPPER:
        result = result.title().replace(' ', '')
    elif nameStyle == NameStyle.UNDERLINE:
        result = result.replace(' ', '_')
    return result

def en_to_cn(word : str) -> str:
    if word.find('_') != -1:
        word = word.replace('_', ' ')
    else:
        word = re.sub(r'([A-Z])', r' \1', word)
        word = word.lower().strip()
    result = translate(word)
    return result

if __name__ == '__main__':
    print(cn_to_en('聊天板块', NameStyle.LOWER))
    print(en_to_cn('night_cat_bbs'))