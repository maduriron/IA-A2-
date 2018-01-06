from __future__ import print_function
import re
from suds.client import Client
from bs4 import BeautifulSoup as bs

def get_text(filename):
    f = open(filename, 'r', encoding = "utf-8")
    data = f.read()
    f.close()
    data = re.sub('etc.', ' ', data)
    data = re.sub('\n', ' ', data)
    sentences = re.findall('([^\.]+\.)', data)
    return sentences

def test_No_Dict(text):
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = text)
    bsObj = bs(result, "lxml")
    return [(ob.get_text(), ob.attrs['id'].split('.')[0], ob.attrs['id'].split('.')[1]) for ob in bsObj.findAll("w", id = re.compile('1\.\d+')) if \
            'extra' in ob.attrs and ob.attrs['extra'] == 'NotInDict']

def test(filename):
    sentences = get_text(filename)
    result = []
    for sentence in sentences:
        no_dict = test_No_Dict(sentence)
        if len(no_dict) == 0:
            no_dict.append('Totul ok aici')
        result.append((sentence, no_dict))
    return result

if __name__ == "__main__":
    not_acceptable = test('proba.txt')
    for tup in not_acceptable:
        print(tup[0])
        print(tup[1])
        print('\n\n')
    
