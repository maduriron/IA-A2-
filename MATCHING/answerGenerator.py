def style(answer):
    return answer[0].upper() + answer[1:] + "."


def separate(prop):
    return (prop[0], prop[1], prop[2])


def generate_answer(input):
    answers = []

    for prop in input:
        _, _, object = separate(prop)
        answer = " ".join(element[0] for element in object)
        answers.append(style(answer))

    return answers


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

    answers = [generate_answer(input_1), generate_answer(input_2),
               generate_answer(input_3)]
    for a in answers:
        print a
