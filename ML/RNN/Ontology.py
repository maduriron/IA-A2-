
"""
Aveti nevoie sa instalati suds

Pe pagina http://nlptools.info.uaic.ro/WebFdgRo/ in dreapta butonului Parse
apare un link WSDL...dati click pe el...
ei bine(sau rau) asta e un document wsdl in care sunt descrise servicii web
Vedeti ce servicii web puteti folosi apeland functia get_description_Fdg_Parser()
Uitati va la ea si apoi la test_Fdg_Parser
E treaba voastra sa va interesati cum trasnformati output ul functiei test_Fdg_Parser
ca sa il puteti prelucra mai apoi...maine pe la amiaza ne gandim cu totii cum am vrea
sa il prelucram.
Tot pana maine la amiaza vreau sa vad cealalata functie testata

POATE aruncati un ochi peste urmatoarele tool uri de pe nlptools uaic:
 * Part of speech Tagger
 * Noun Phrase Chuner

"""

from suds.client import Client
from suds.sudsobject import asdict
from bs4 import BeautifulSoup as bs
import re

class MyResult(object):
    def __init__(self, tag1, tag2, tag3, tag4, tag11, tag12 ):
        self.index_prop = tag1
        self.leg_head = tag2
        self.head = tag3
        self.pos = tag4
        self.lemma = tag11
        self.deprel = tag12

    def __hash__(self):
        return hash((self.index_prop, self.leg_head))


    def __eq__(self, other):
        return (self.index_prop, self.leg_head) == (other.index_prop, other.leg_head)


    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        res = "{ index_prop: "  + self.index_prop + ', leg_head : ' + self.leg_head +\
              ' , head : ' + self.head + ', pos: ' + self.pos + ' lemma: ' + self.lemma + \
              ' deprel: ' + self.deprel + '}'
        return res
def get_description_Fdg_parser():
    """
    Functia asta afiseaza ce servicii web ofera Fdg Parser ul
    Va rog, ca dupa rulare sa va uitati la methods ca acolo apar
        functiile oferite de serv web, insotite de parametri
    """
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    print(client)

def test_Fdg_Parser(text):
    """
    Aici am apelat functia parseText, care are ca output un xml.
    TO DO // DE AICI lucrati cu ce returneaza functia...care e
    un obiect de tip <class 'suds.sax.text.Text'>...pare a fi un xml 
    
    
    Chiar daca nu mergeti pe strategia asta in final...vreau ca pana
    luni sa fie implementat partea de gasire a subiectului predicatului
    si a complementului. Discutam maine seara daca se poate sau nu.
    TO DO // Vedeti ce face si a doua metoda a serviciului web
    parsePosTaggedXML(xs:string posTaggedXML, )
    """
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = text)
    return result

def test_Fdg_Pos_Parser(res):
    """
    Aici am apelat functia parseText, care are ca output un xml.
    TO DO // DE AICI lucrati cu ce returneaza functia...care e
    un obiect de tip <class 'suds.sax.text.Text'>...pare a fi un xml 
    
    
    Chiar daca nu mergeti pe strategia asta in final...vreau ca pana
    luni sa fie implementat partea de gasire a subiectului predicatului
    si a complementului. Discutam maine seara daca se poate sau nu.
    TO DO // Vedeti ce face si a doua metoda a serviciului web
    parsePosTaggedXML(xs:string posTaggedXML, )
    """
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parsePosTaggedXML(posTaggedXML = res)
    return result

def test_No_Dict(text):
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = text)
    bsObj = bs(result, "lxml")
    print(bsObj)
    return [(ob.get_text(), ob.attrs['id'].split('.')[0], ob.attrs['id'].split('.')[1]) for ob in bsObj.findAll("w", id = re.compile('1\.\d+')) if \
            'extra' in ob.attrs and ob.attrs['extra'] == 'NotInDict']

#print(test_No_Dict("Merg la magazin kjaajhfhsdlfh maine."))

    
def take_all(text):
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = text)
    bsObj = bs(result, "lxml")
    n = int(max([ob.attrs['id'] for ob in bsObj.findAll("s")]))
    l = []
    print('n =', n)
    for i in range (1, n + 1):
        l.append([{'index_prop':ob.attrs['id'].split('.')[0], 'leg_head': ob.attrs['id'].split('.')[1] , \
               'head':ob.attrs['head'], 'lemma':ob.attrs['lemma'], 'deprel' : ob.attrs['deprel'], 'pos': ob.attrs['pos']} for ob \
              in bsObj.findAll("w", id = re.compile(str(i) + "\.\d+")) if 'deprel' in ob.attrs and \
                  'pos' in ob.attrs])
    return l

def connections(index_prop, legatura ,l):
    result = []
    for el in l:# el e o lista de dictionare
        for d in el:
            if int(d['head']) == legatura and int(d['index_prop']) == index_prop:
                result.append(d)
    return result

def all_connections(l, index_prop = 2):
    result = []
    for el in l:
        if int(el[0]['index_prop']) == index_prop:
     #       print 'Sunt aici' 
            for d in el:
                neighbors = connections(int(d['index_prop']), int(d['leg_head']), l)
      #          print 'neighbors =', neighbors
                if len(neighbors) > 0:
                    result.append({MyResult(d['index_prop'], d['leg_head'], d['head'], \
                                        d['pos'], d['lemma'], d['deprel']) : neighbors})
    return result
"""

#print connections(2, 1, l)

lr =  all_connections(l, 2)
for pair in lr: # pair e un dictionar format dintr-o 
    for key in pair:
        print key, pair[key]
"""
def parse_morphology(text):
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = text)
    bsObj = bs(result, "lxml")
    n = int(max([ob.attrs['id'] for ob in bsObj.findAll("s")]))
    l = []
    #print 'n =', n
    for i in range(1, n + 1):
        l.append([ ob.attrs['deprel'] for ob in bsObj.findAll("w", id = re.compile(str(i) + "\.\d+")) if \
                 'deprel' in ob.attrs and 'pos' in ob.attrs])
    return l

#print(parse_morphology("Fata merge des la mare."))


#get_description_Fdg_parser()
#print(test_Fdg_Parser('Inima bate incet').encode('ascii', 'ignore'))
#print(test_Fdg_Pos_Parser(test_Fdg_Parser('Inima bate incet')).encode('ascii', 'ignore'))
# l = take_all("Inima bate incet. Calul frumos merge repede.")
# for li in l:
#     try:
#         print(li)
#     except:
#         print("PASSS")
