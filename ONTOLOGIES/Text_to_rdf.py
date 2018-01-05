# -*- coding: utf-8 -*-
from suds.client import Client
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring


def get_description_Fdg_parser():
    """
    Functia asta afiseaza ce servicii web ofera Fdg Parser ul
    Va rog, ca dupa rulare sa va uitati la methods ca acolo apar
        functiile oferite de serv web, insotite de parametri
    """
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    print(client)
# get_description_Fdg_parser()

def test_Fdg_Parser(text):
    """
    Aici am apelat functia parseText, care are ca output un xml.
    """
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt=text)
    return result


def generateConnetionPath(phrase,wordid,list):
    x = wordid
    word_id = str(x).split('.')[1]
    for child in phrase:
        if word_id == child.attrib["head"]:
            list.append(child.attrib)
            generateConnetionPath(phrase, child.attrib["id"], list)

def connectionsBetweenWords(phrase,wordid):
    x = wordid
    prop_id = str(x).split('.')[0]
    word_id = str(x).split('.')[1]
    connected_words = []
    for child in phrase:
        if word_id == child.attrib["head"]:
            connected_words.append(child.attrib)
    return connected_words


def list_to_text(list):
    text = list[0]["LEMMA"]
    for i in range(1, len(list)):
        text += " "
        text += list[i]["LEMMA"]
    return text

def parseXMLOutput():
    return_list = []
    """Aici se pune(momentan) textul pe care dorim sa il transformam in ontologie"""
    text_to_be_transformed = """Fluxul sanguin cerebral este asigurat prin cele două artere carotide interne şi de cele două artere vertebrale care se unesc în trunchiul vertebrobazilar. Ramificaţiile intracraniene ale acestor artere sunt de tip terminal ceea ce conferă o gravitate crescută ocluziilor vasculare cerebrale."""
    #Apelam functia de mai sus care ne parseaza texul si il tokenizeaza

    callback_result_from_Parser = test_Fdg_Parser(text_to_be_transformed)
    root = ET.fromstring(callback_result_from_Parser)
    print(callback_result_from_Parser)
    #Formam apoi un tuplu care contine: subiectul, verbul si un alt tuplu care contine obiectele
    for phrase in root:
        current_list = []
        for child in phrase:
            if 'POS' in child.attrib and child.attrib['POS'] == 'VERB' or child.attrib["deprel"] == "ROOT":
                current_list.append([child.attrib])
                connected_words = connectionsBetweenWords(phrase, child.attrib["id"])
                for word in connected_words:
                    propozitie = []
                    propozitie.append(word)
                    generateConnetionPath(phrase,word["id"],propozitie)
                    current_list.append(propozitie)
        return_list.append(current_list)

    new_list = []
    for i in range(0, len(return_list)):
        prop =[]
        for j in range(0,len(return_list[i])):
            lista = []
            for x in range(0,len(return_list[i][j])):
                lista.append((return_list[i][j][x]["LEMMA"],return_list[i][j][x]["deprel"],return_list[i][j][x]["id"]))
            lista  = sorted(lista,key=lambda tup: tup[2])
            prop.append(lista)
        new_list.append(prop)
    ret = []
    for i in range(0, len(new_list)):
        subiect = [None]
        predicat = [None]
        obiect = [None]
        if(len(new_list[i])) > 0:
            predicat = new_list[i][0]
        else:
            continue
        for j in range(1,len(new_list[i])):
            for k in range(0,len(new_list[i][j])):
                if(new_list[i][j][k][1] == "sbj."):
                    subiect = new_list[i][j]
                    continue
                if new_list[i][j][k][1] == 'n.pred.' or new_list[i][j][k][1] == 'c.d.' or new_list[i][j][k][1] == 'a.adj.' or new_list[i][j][k][1] == 'coord.' or new_list[i][j][k][1] == 'a.subst.' or new_list[i][j][k][1] == 'prep.':
                    obiect = new_list[i][j]
        ret.append((subiect,predicat,obiect))
    return ret




def to_rdf(list):
    #Functie care duce tuplul nostru creat mai sus intr-un format rdf corespunzator
    rdf = ET.Element('rdf:RDF')
    rdf.set("xmlns:rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdf.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    for value in list:
        if(value[0][0] != None and value[1][0] != None and value[2][0] != None):
            subiect = ""
            for element_lista_subiect in value[0]:
                subiect += element_lista_subiect[0] + " "
            adjectiv = ""
            for element_lista_adjectiv in value[2]:
                adjectiv += element_lista_adjectiv[0] + " "

            rdf_description = ET.SubElement(rdf, 'rdf:Description')
            rdf_subject = ET.SubElement(rdf_description, 'rdf:' + value[0][0][1])
            rdf_subject.text = subiect.rstrip()
            rdf_predicate = ET.SubElement(rdf_description, 'rdf:' + value[1][0][1])
            rdf_predicate.text = value[1][0][0]
            rdf_object = ET.SubElement(rdf_description, 'rdf:' + value[2][0][1])
            rdf_object.text = adjectiv.rstrip()

    return tostring(rdf)


# print(to_rdf(parseXMLOutput()))


fd = open("Generated_rdf.xml", "wb")
fd.write(b"<?xml version='1.0' encoding='utf-8'?>\n")
fd.write(to_rdf(parseXMLOutput()))