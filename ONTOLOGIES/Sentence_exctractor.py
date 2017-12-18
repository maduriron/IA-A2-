# -*- coding: utf-8 -*-
# -*- coding: utf-16 -*-
from docx import Document
import codecs
import sys

try:
    f = codecs.open('sentences-' + sys.argv[1] + '.txt', 'w', 'utf-8')
    f.write(u'\ufeff')

    document = Document(sys.argv[1])

    for a in document.paragraphs:
        sentences = a.text\
            .replace('!', '.')\
            .replace('?', '.')\
            .replace("\n", ' ')\
            .replace("\t", ' ')\
            .replace('     ', ' ')\
            .replace('    ', ' ')\
            .replace('   ', ' ')\
            .replace('  ', ' ')\
            .split('.')
        if len(sentences) > 0:
            for s in sentences:
                s = s.strip()
                if len(s) > 0 and len(s) < 1000000:
                    s = s.replace(u'ţ', 't')\
                        .replace(u'Ț', 'T')\
                        .replace(u'ş', 's')\
                        .replace(u'Ș', 'S')\
                        .replace(u'î', 'i')\
                        .replace(u'Î', 'I')\
                        .replace(u'ă', 'a')\
                        .replace(u'Ă', 'A')\
                        .replace(u'â', 'a')\
                        .replace(u'Î', 'A')
                    f.write(s + "\n")
except:
    print("ERROR. NU ai introdus fisierul ca parametru")
