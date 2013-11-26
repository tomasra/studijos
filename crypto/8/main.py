#encoding:windows-1257
'''
Created on Oct 23, 2013

@author: tomas
'''

import re

abc = 'AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽ0123456789?!:;()<>.,*'
q1 = 'JJP?JŠ?8>'

def get_keys(c, q1, q2):
    diff = q2 - q1
    keys = []
    for k1 in range(0, len(abc)):
        for k2 in range(0, len(abc)):
            if ((k1 * (c - diff)) + k2) % len(abc) == c:
                keys.append([k1, k2])
    return keys
                
def dec_one(c, k1, k2):
    return (k1 * c + k2) % len(abc)
                
def dec_phrase(phrase, q1, q2):
    print 'pradzia'
    keys = get_keys(abc.index(phrase[0]), q1, q2)
    for k in keys:
        msg = ''
        for p in phrase:
            msg += abc[dec_one(abc.index(p), k[0], k[1])]
#         if (msg[3] == '*' and msg[6] == '*'):
        if (re.match('[^*]+[*][^*]{1,2}[*][^*]{1,2}', msg) != None):
            print msg
        
# print dec_one(abc.index('J'), 44, 30)
dec_phrase('GLGŪFŪGL', 31, 7)
dec_phrase('0JYUYŽUZ', 10, 40)
dec_phrase('Ų<;Ž1Ž14', 8, 5)
dec_phrase(')5:J5ŲJ)Š', 45, 51)
dec_phrase('M2G9GB9MM', 34, 26)
dec_phrase('IDDS;;S;', 4, 29)
dec_phrase('KĘ,Į,,Į,', 33, 25)
dec_phrase('<N;7<(7R<', 48, 41)
dec_phrase('>K>67>6E*', 49, 15)
dec_phrase('IKŽBIDBŽI', 28, 23)

    
# q2 = '8*ÅŖ:2K:8G'
# q3 = '133.Å²3.VP'
# q9 = 'U)29GB9MM'
# q10 = 'O55POFP<S'


