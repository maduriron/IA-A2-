from __future__ import print_function
# -*- coding: utf-8 -*-
import re
from suds.client import Client
from bs4 import BeautifulSoup as bs
from Ontology import test_No_Dict

def get_questions_Radu(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    l = re.findall('\d+\.\[(.+);\n+(.+)?\]', data)
    return l

def get_questions_Sam(filename):
    f = open(filename,'r', encoding="utf8")
    data = f.read()
    f.close()
    l = re.findall('(.+\.)\n(.+\?)\n+', data)
    return l

def parse_morphology(text):
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt = text)
    bsObj = bs(result, "lxml")
    n = int(max([ob.attrs['id'] for ob in bsObj.findAll("s")]))
    l = []
    for i in range(1, n + 1):
        l.append([ ob.attrs['deprel'] for ob in bsObj.findAll("w", id = re.compile(str(i) + "\.\d+")) if \
                 'deprel' in ob.attrs and 'pos' in ob.attrs])
    return l

#filenames = lista cu numele fisierelor din care se iau intrebarile
def make_input_format(l):
    """l va fi o lista in care un element reprezinta
    mai multe propozitii, care fac impreuna max 100 000 prop
    q - lista de intrebari pentru fiecare text in parte"""
    result = []
    for sentences in l:
        sentences = sentences.replace('.', '. ')
        #print ('sentences=', sentences)
        response = parse_morphology(sentences)
        l1 = len(response)
        
        #print ('response =', response)

        sentences = sentences.replace(',', ' ') 
        sentences = re.sub('\(', ' ', sentences)
        sentences = re.sub('\)', ' ', sentences)
        sentences = sentences.replace('!', ' ') 
        sentences = sentences.replace(':', ' ') 
        sentences = sentences.replace(';', ' ')
        list_sentences = sentences.split('.')[:-1]
        l2 = len(list_sentences)
        if l1 != l2:
            print ('_________')
            print ('response=', response)
            print('\n')
            print ('sentences=', sentences)
            print ('_________')
        for pos,sentence in enumerate(list_sentences):
            #word_list = sentence.split()
            '''first = ()
            for i in range(0, len(word_list)):
                first += (i, )
            '''
            second = list(response[pos] )#pentru ca response si list_sentences reprezinta aceeasi lista de prop
            #print(second)
            result.append(second)
    return result 

def make_text_list(filename, margin):
    """
    returneaza un tuplu cu 2 liste:[text] [intrebari]
    """
    l = get_questions_Sam(filename)
    counter = 0
    result_text = []
    result_quest = []
    sentence = ''
    saved = ''
    for el in l:
        result_quest.append(el[1])   
        if counter + len(el[0]) < margin:
            sentence += el[0]
            counter += len(el[0])
        else:
            result_text.append(sentence)
            sentence = el[0]
            counter = len(el[0])       
    result_text.append(sentence)    
    return result_text, result_quest

def make_target_seq(filename,maxim):
    l = get_questions_Sam(filename)
    result = []
    for el in l:
        tup = []
        #tup = () #pentru tuplu
        text = el[0]
        q = el[1]
        text = text.replace('.', ' ')
        text = text.replace('(', ' ')
        text = text.replace(')', ' ')
        text = text.replace(',', ' ')
        text = text.replace(':', ' ')
        text = text.replace(';', ' ')
        text = text.replace('-', ' ')
        q = q.replace('.', ' ')
        q = q.replace('(', ' ')
        q = q.replace(')', ' ')
        q = q.replace(',', ' ')
        q = q.replace(':', ' ')
        q = q.replace(';', ' ')
        q = q.replace('?', ' ')
        q = q.replace('-', ' ')
        words_text = [w.lower() for w in text.split()]
        words_q = [w.lower() for w in q.split()]
        #print (words_text)
        #print (words_q)
        for word in words_q:
            gasit = 0
            for pos, w in enumerate(words_text):
                if word == w:
                    tup += [pos]
                    gasit = 1
                    break
            if gasit == 0:
                tup += [-1]
        tup+=[-2]*(maxim-len(tup))
        #tup=tuple(tup) #decomentare pentru tuple
        result.append(tup)
    #result=tuple(result) #decomentare pentru tuplu
    return result

"""
l = make_text_list('set1.txt', 4900)
print(l)

"""
#g = open('rezultat.txt', 'w')

#target = make_target_seq('set1.txt')
#text, q = make_text_list('set1.txt', 1000)
'''
t = make_text_list('set1.txt', 300)
inp = make_input_format(t[0])
target = make_target_seq('set1.txt')
print (max([len(t[0]) for t in inp]))
print(inp[0][0])
print(inp[:2])
#print (target)
#print(len(inp))
'''
#print(parse_morphology('Imagistica actuală evidenţiază cu uşurinţă volumul ventricular şi al spaţiilor interne. În plus  hipodensitatea periventriculară este un indiciu de compresiune cerebrală. Fluxul lichidului poate fi vizualizat prin tehnici speciale de rezonanţă magnetică nucleară. Măsurarea presiunii intracraniene nu este un indiciu fidel în hidrocefalia adultului. Tratamentul conservator are posibilităţi limitate  unele diuretice  neurotrofice  cu efect îndoielnic. Aceste tehnici au transformat hidrocefalia într-o boală curabilă dacă intervenţia se practică la timp. Boala subdurală în cazurile în care este compresivă se tratează similar cu hematomul subdural cronic prin trepanaţie şi drenaj. Boala subdurală în cazurile în care este compresivă se tratează similar cu hematomul subdural cronic prin trepanaţie şi drenaj. Bubele mari se tratează atunci când sunt mici. Diagnosticul clinic se bazează pe asocierea sindromului neurologic focal cu sindromul infecţios şi sindromul de hipertensiune intracraniană. Ma duc la baie.'))
def remake_input(input,maxim):
    input=list(input) # comentare pentru tuplu
    for i in range(len(input)):
        #print(i)
        #print(input[i])
        for j in range(len(input[i])):
            #print(input[i][j])
            if input[i][j]=='ROOT':
                input[i][j]=0
            elif input[i][j]=='sbj.':
                input[i][j]=1
            elif input[i][j]=='a.adj.':
                input[i][j]=2
            elif input[i][j]=='a.vb.':
                input[i][j]=3
            elif input[i][j]=='c.d.':
                input[i][j]=4
            elif input[i][j]=='subord.':
                input[i][j]=5
            elif input[i][j]=='det.':
                input[i][j]=6
            elif input[i][j]=='a.subst.':
                input[i][j]=7
            elif input[i][j]=='aux.':
                input[i][j]=8
            elif input[i][j]=='prep.':
                input[i][j]=9
            elif input[i][j]=='c.i.':
                input[i][j]=10
            elif input[i][j]=='coord.':
                input[i][j]=11
            elif input[i][j]=='refl.':
                input[i][j]=12
            elif input[i][j]=='ap.':
                input[i][j]=13
            elif input[i][j]=='n.pred.':
                input[i][j]=14
            elif input[i][j]=='c.ag.':
                input[i][j]=15
            elif input[i][j]=='a.adv.':
                input[i][j]=16
            elif input[i][j]=='c.c.m.':
                input[i][j]=17
            elif input[i][j]=='c.c.l.':
                input[i][j]=18
            elif input[i][j]=='neg.':
                input[i][j]=19
            elif input[i][j]=='c.c.t.':
                input[i][j]=20
            elif input[i][j]=='c.c.cond.':
                input[i][j]=21
            elif input[i][j]=='comp.':
                input[i][j]=22
            elif input[i][j]=='part.':
                input[i][j]=23
            elif input[i][j]=='c.c.cz.':
                input[i][j]=24
            elif input[i][j]=='a.pron.':
                input[i][j]=25
            elif input[i][j]=='c.c.scop.':
                input[i][j]=26
            elif input[i][j]=='c.c.instr.':
                input[i][j]=27
        input[i]+=[-2]*(maxim-len(input[i]))
        #print(len(input[i]))
        #input[i]=tuple(input[i]) decomentare pentru tuplu
        #print(input[i])

def return_data(file,size):
    list=make_text_list(file,size)
    #print(list[0])
    input=make_input_format(list[0])
    #print(input)
    #maxim = max([len(t) for t in input])
    maxim = 52
    target=make_target_seq(file,maxim)
    #print(max([len(t[0]) for t in input]))
    remake_input(input,maxim)
    #input=tuple(input) # decomentare pentru tuplu
    # print(input)
    # print(target)
    return input,target
#return_data('proba.txt',300)
