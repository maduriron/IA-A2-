from __future__ import print_function
import re
from suds.client import Client
from bs4 import BeautifulSoup as bs
from EchipaO import parseXMLOutput
from questionGen_1 import convertToList_2,rel_pron
from suds.client import Client
import xml.etree.ElementTree as ET

def get_text(filename):
    f = open(filename, 'r', encoding = "utf8")
    data = f.read()[1:]
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

def getWordType(word):
    if not any(c.isalpha() for c in word):
        return "None"
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = word)
    root = ET.fromstring(result)
    POS = root.find('.//W')
    return POS.attrib['POS']


def generateQuestion2(sentence_list):
    subj_tuples = sentence_list[0]
    pred_tuples = sentence_list[1]
    obj_tuples = sentence_list[2]
    if subj_tuples is None or pred_tuples is None or obj_tuples is None:
        return ""

    subj_list = [list(elem) for elem in subj_tuples if elem is not None]
    pred_list = [list(elem) for elem in pred_tuples if elem is not None]
    obj_list = [list(elem) for elem in obj_tuples if elem is not None]

    if not subj_list or not pred_list or not obj_list:
      bj_poz = -1
    pred_poz = -1
    for i in range(len(pred_list)):
        if pred_list[i][1] == 'ROOT':
            pred_poz = i
    if pred_poz  == -1:
        return ""
    for i in range(len(subj_list)):
        if subj_list[i][1] == 'sbj.':
            subj_poz = i
    #if subj_poz == -1:
        #return ""

    pred_type = getWordType(pred_list[0][0])
    if pred_type != 'VERB':
        return ""

    noun_adj_poz = -1
    for i in range(len(obj_list)):
        word_type = getWordType(obj_list[i][0])
        if word_type == 'ADJECTIVE' or word_type == 'NOUN':
            noun_adj_poz = i
            break
    #if noun_adj_poz == -1:
        #return ""

    word_after_verb = obj_list[noun_adj_poz][0]
    compl_type = None
    for i in range(len(obj_list)):
        if obj_list[i][1] in ['c.d.', 'c.c.l.', 'c.c.m.', 'c.c.c.', 'c.c.s.', 'c.c.t.', 'c.i.', 'n.pred.']:
            compl_type = obj_list[i][1]
            break
    subject = ""
    for x in subj_list:
        subject += x[0]
        subject += " "
    predicate = ""
    for x in pred_list:
        predicate += x[0]
        predicate += " "
    relative_pronoun = rel_pron(compl_type, word_after_verb)
    question = relative_pronoun + " " + predicate  + " " + subject + "?"
    answer = ""
    for x in obj_list:
        answer += x[0]
        answer += " "
    return [question, answer]





if __name__ == "__main__":
    doc_name = 'proba.txt'
    lista_input = parseXMLOutput(doc_name)
    #print (list(lista_input))
    new_list = list(lista_input)[-1]
    for propozitii in new_list:
        print(generateQuestion2(list(propozitii)))

    """
    Apelati functia voastra.
    Va dau si fisierul txt folosit.
    AVeti grija sa va uitati in prop alea din fisier sa aiba toate subiect.
    Nu uitati sa returnati pentru fiecare intrebare si cate doua raspunsuri gresite
    si cel corect. Raspunsurile gresite sa fie alte 2 obiecte din alte 2 tuple.
"""
