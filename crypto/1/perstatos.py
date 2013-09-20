#encoding:windows-1257
import re

# cipher = """
# IAIPL KPUIS IKČĄT EDIIS IILKS 
# MČKAE ĖUSUT ŠAŪSM UIASČ DČLOS 
# YSAPK AYAĖŽ KIDAI SITNV AUAPI 
# LRĄ 
# """

cipher="""
ODMNG RPURO UĖTRP KŪIRA UOIVN 
TIAON RŽIMR BKTNE ASNRK UJSĖS 
SRUAS ASYĖN ŠLAĄU SYKAP KRPSV 
IOAAR IŽVKS EAAKV SBKUR RAOEA 
LOKKL GISUR NAATO SROEĄ KKTUP 
IPTAU SAILM UTUUS ARNRI LĖČAP 
USRNU AĖENA ILLSJ GVĄPR UIGGS 
MTRAO KPUKR JBOOG PĮKSU NIDSK 
ĘIITT SPTAU OOEAL ĖGRSU IEUOA 
KKUSA AIĖUN NOUOR ĘSIIK SLŪOR 
IKČOM NNĘAŲ ĖEPUY IDTIG UOŠDN 
DAIAS AĖ
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
