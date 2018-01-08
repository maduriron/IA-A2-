import sys
import os

path = os.path.dirname(__file__)
sys.path.append(path)

from answerGenerator import *
from questionGerenator import *


def extractElements(input):
    for l in input:
        for element in l:
            yield element


def associate(questions, answers):
    if len(questions) != len(answers):
        raise Exception("Different numbers of questions and answers!")

    packed = []
    for element in extractElements(questions):
        packed.append(element)
    for element in extractElements(answers):
        packed.append(element)

    to_return = []
    for index in range(len(packed) / 2):
        to_return.append((packed[index], packed[index + len(packed) / 2]))

    return to_return


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
    answers = [generate_answer(input_1), generate_answer(input_2),
               generate_answer(input_3)]

    Q_A = associate(questions,answers)
    print Q_A
