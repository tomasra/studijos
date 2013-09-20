#encoding:windows-1257
import re

# cipher = """
# IAIPL KPUIS IK��T EDIIS IILKS 
# M�KAE �USUT �A�SM UIAS� D�LOS 
# YSAPK AYA�� KIDAI SITNV AUAPI 
# LR� 
# """

cipher="""
ODMNG RPURO U�TRP K�IRA UOIVN 
TIAON R�IMR BKTNE ASNRK UJS�S 
SRUAS ASY�N �LA�U SYKAP KRPSV 
IOAAR I�VKS EAAKV SBKUR RAOEA 
LOKKL GISUR NAATO SROE� KKTUP 
IPTAU SAILM UTUUS ARNRI L��AP 
USRNU A�ENA ILLSJ GV�PR UIGGS 
MTRAO KPUKR JBOOG P�KSU NIDSK 
�IITT SPTAU OOEAL �GRSU IEUOA 
KKUSA AI�UN NOUOR �SIIK SL�OR 
IK�OM NN�A� �EPUY IDTIG UO�DN 
DAIAS A�
"""

cipher = re.sub('[\n ]', '', cipher)
# order = [3, 1, 5, 2, 0, 4]
order = [5, 0, 2, 1, 4, 3]
l = len(cipher) // len(order)    # eilutes ilgis

rez = ''
for i in range(0, l):
    for c in [cipher[i::l][j] for j in order]:
        rez += c
print(rez)
