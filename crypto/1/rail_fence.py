#encoding:windows-1257
import re

# cipher="""
# PŪIVURSŠASĖČATSUĖJIIŪRA
# """

cipher="""
BČIAI IOPDU UŲNDE SIAAT ILNAS 
JŠRAI OSSAJ IVIŲR ATAAT UŠOEK 
MUOUI SLGRŠ KAČAK SASKŠ KRSLO 
KAŪNI K
"""

cipher = re.sub('[\n ]', '', cipher)

# eiluciu skaicius
key=4 

src_index = 0
message = [None] * len(cipher)

# eilute
for e in range(0, key):
    # j - pozicija kur keiciasi raidziu kryptis
    # i - pozicijos eiles numeris
    for i, j in enumerate(range(0, len(cipher), key - 1)):
        # p - simbolio vieta originaliame pranesime
        p = None
        # tvoreles virsus
        if (e == 0):
            if (i % 2 == 0):
                p = j
        # tvoreles apacia
        elif (e == (key - 1)):
            if (i % 2 == 1):
                p = j
        # tvoreles vidurys
        else:
            if (i % 2 == 0):
                p = j + e
            else:
                p = j + (key - e - 1)
        if (p != None and p < len(cipher)):
            # is eiles einantis sifro simbolis idedamas i reikiama pranesimo vieta
            message[p] = cipher[src_index]
            src_index += 1

print ''.join(message)