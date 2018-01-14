
from suds.client import Client
import xml.etree.ElementTree as ET

def convertToList(sentence):
    sentence_list = []
    aux_list = list(list(sentence)[0])
    for x in aux_list:
        for y in x:
            sentence_list.append(list(y))
    return sentence_list


def convertToList_2(sentence):
    sentence_list = []
    for x in sentence:
        for y in x:
            if isinstance(y, tuple):
                sentence_list.append(list(y))
    return sentence_list

def getWordType(word):
    if not any(c.isalpha() for c in word):
        return "None"
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = word)
    root = ET.fromstring(result)
    POS = root.find('.//W')
    #print (result)
    #print (POS.attrib['POS'])
    return POS.attrib['POS']

def rel_pron(x, word_after_verb):
    if x != 'n.pred.':
        return {
            'c.d.' : 'Ce',
            'c.c.l.': 'Unde',
            'c.c.m.': 'Cum',
            'c.c.c.': 'Din ce cauza',
            'c.c.s.': 'De ce', #cu ce scop
            'c.c.t.': 'Cand',
            'c.i.' : 'Cui'
        }.get(x,'Ce')
    else:
        if getWordType(word_after_verb) == 'ADJECTIVE':
            return 'Cum'
        else:
            return 'Ce'

def generateQuestion(sentence_list):
    #det poz primului subst sau adj dupa predicat
    pred_poz = -1
    subj_poz = -1
    noun_adj_poz = -1
    for i in range(len(sentence_list)):
        if sentence_list[i][1] == 'sbj.':
            subj_poz = i
    for i in range(len(sentence_list)):
        if sentence_list[i][1] == 'ROOT':
            pred_poz = i
    for i in range(pred_poz,len(sentence_list)):
        word_type = getWordType(sentence_list[i][0])
        if word_type == 'ADJECTIVE' or word_type == 'NOUN':
            noun_adj_poz = i
            break
    #print (noun_adj_poz)
    prop_type = sentence_list[noun_adj_poz][1]
    #print (prop_type)

    relative_pronoun = rel_pron(sentence_list[pred_poz + 1][1], sentence_list[noun_adj_poz][0])
    return relative_pronoun + " " + sentence_list[pred_poz][0] + " " + sentence_list[subj_poz][0] + "?"

'''
sentence1 = [([('Neurochirurgia', 'sbj.', '1.1')], [('este', 'ROOT', '1.2')], [('o', 'det.', '1.3'), ('ramură', 'n.pred.', '1.4'), \
                ('a', 'det.', '1.5'), ('științelor', 'a.subst.', '1.6'), ('medicale', 'a.adj.', '1.7')])]
sentence2 = [([('Băiatul', 'sbj.', '1.1')], [('este', 'ROOT', '1.2')], [('deștept', 'n.pred.', '1.3')])]
sentence3 = [([('Sebastian', 'sbj.', '1.1')], [('devine', 'ROOT', '1.2')], [('aviator', 'n.pred.', '1.3')])]
sentence4 = [([('Câinele', 'sbj.', '1.1'), ('rătăcit', 'a.adj.', '1.2')], [('latră', 'ROOT', '1.3')], [('la', 'c.c.l.', '1.4'), ('lună', 'prep.', '1.5')])]

sentence_list = convertToList(sentence1)
print(generateQuestion(sentence_list))
print(generateQuestion(convertToList(sentence2)))
print(generateQuestion(convertToList(sentence3)))
print(generateQuestion(convertToList(sentence4)))
'''
