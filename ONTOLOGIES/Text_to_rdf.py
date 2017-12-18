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
# print test_Fdg_Parser('George are acadele')


lista = []

def parseXMLOutput():

    """Aici se pune(momentan) textul pe care dorim sa il transformam in ontologie"""
    text_to_be_transformed = 'Neurochirurgia este o ramură a ştiinţelor medicale.'
    #Apelam functia de mai sus care ne parseaza texul si il tokenizeaza

    result = test_Fdg_Parser(text_to_be_transformed)
    root = ET.fromstring(result)
    #Formam apoi un tuplu care contine: subiectul, verbul si un alt tuplu care contine obiectele
    for phrase in root:
        grup = []
        objects_list = []
        for child in phrase:
            can_be_verb = 0
            can_be_subject = 0
            can_be_object = 0

            for key, value in child.attrib.items():
                if key == 'POS' and (value == 'NOUN' or value == 'PRONOUN'):
                    can_be_subject = 1
                if key == 'deprel' and value == 'sbj.' and can_be_subject == 1:
                    grup.append((child.attrib["LEMMA"],child.attrib["deprel"]))
                if key == 'POS' and value == 'VERB':
                    can_be_verb = 1
                if key == 'deprel' and value == 'ROOT' and can_be_verb == 1:
                    grup.append((child.attrib["LEMMA"],child.attrib["deprel"]))
                if key == 'POS' and (value == 'NOUN' or value == 'ADJECTIVE'):
                    can_be_object = 1
                if key == 'deprel' and (value == 'n.pred.' or value == 'c.d.' or value == 'a.adj.' or value == 'coord.'
                                        or value == 'a.subst.' or value == 'prep.') and can_be_object == 1:
                    objects_list.append((child.attrib["LEMMA"],child.attrib["deprel"]))
        if len(objects_list) != 0:
            grup.append(objects_list)
        lista.append(tuple(grup))
    return lista

#parseXMLOutput()

def to_rdf(list):
    #Functie care duce tuplul nostru creat mai sus intr-un format rdf corespunzator
    rdf = ET.Element('rdf:RDF')
    rdf.set("xmlns:rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdf.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    for value in list:
        for obj in value[2]:
            rdf_description = ET.SubElement(rdf, 'rdf:Description')
            rdf_subject = ET.SubElement(rdf_description, 'rdf:'+value[0][1])
            rdf_subject.text = value[0][0]
            rdf_predicate = ET.SubElement(rdf_description, 'rdf:'+value[1][1])
            rdf_predicate.text = value[1][0]
            rdf_object = ET.SubElement(rdf_description, 'rdf:'+obj[1])
            rdf_object.text = obj[0]

    return tostring(rdf)


# print(to_rdf(parseXMLOutput()))
fd = open("Generated_rdf.xml", "wb")
fd.write(b"<?xml version='1.0' encoding='utf-8'?>\n")
fd.write(to_rdf(parseXMLOutput()))