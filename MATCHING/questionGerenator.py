from suds.client import Client
import xml.etree.ElementTree as ET

d = {
    'c.c.l.': 'Unde',
    'c.c.m.': 'Cum',
    'c.c.c.': 'Din ce cauza',
    'c.c.s.': 'De ce',
    'c.c.t.': 'Cand',
    'c.d.': 'Ce',
    'c.i.': 'Cui'
}


def getWordType(word):
    if not any(c.isalpha() for c in word):
        return "None"
    client = Client('http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl')
    result = client.service.parseText(txt=word)
    root = ET.fromstring(result)
    POS = root.find('.//W')

    return POS.attrib['POS']


def separate(prop):
    return (prop[0], prop[1], prop[2])


def generate_questions(input):
    questions = []

    for prop in input:
        subject, predicate, object = separate(prop)
        question_pattern = "{} {} {}?"
        question = ""

        for t in object:
            if t[1] in d.keys():
                question = d[t[1]]
                break

            if t[1] == 'n.pred.':
                if getWordType(t[0]) == 'ADJECTIVE':
                    question = 'Cum'
                else:
                    question = 'Ce'
                break

        predicate = " ".join(p[0] for p in predicate)
        subject = " ".join(s[0] for s in subject)

        questions.append(question_pattern.format(question, predicate, subject))
    return questions


if __name__ == '__main__':
    input_1 = [([('calul', 'sbj.', '1.1'), ('frumos', 'a.adj.', '1.2')],
                [('merge', 'ROOT', '1.3')],
                [('la', 'prep.', '1.4'), ('mare', 'c.c.l.', '1.5')]),
               ([('mama', 'sbj.', '1.1'), ('mea', 'a.adj', '1.2')],
                [('a', '', '2.3'), ('facut', 'ROOT', '2.4'),
                 ('clatite', 'subst.', '2.5')],
                [('vinerea', 'c.c.t.', '2.6'), ('trecuta', 'a.adj.', '2.7')])
               ]
    input_2 = [([('baiatul', 'sbj.', '1.1')], [('este', 'ROOT', '1.2')],
                [('destept', 'n.pred.', '1.3')])]
    input_3 = [([('Sebastian', 'sbj.', '1.1')], [('devine', 'ROOT', '1.2')],
                [('aviator', 'n.pred.', '1.3')])]

    questions = [generate_questions(input_1), generate_questions(input_2),
                 generate_questions(input_3)]
    for q in questions:
        print q
