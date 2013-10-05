'''
Created on Oct 2, 2013

@author: tomas
'''

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

# desimtainis skaicius i 8 bitus
def decimal_to_bits(d):
    result = []
    bits = [int(x) for x in list('{0:0b}'.format(d))]
    for i in range(0, 8 - len(bits)):
        result.append(0)
    for b in bits:
        result.append(b)
    return result
        
def bits_to_decimal(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out
        
cipher = [201, 234, 59, 113, 243, 94, 4, 42, 41, 199, 240, 28, 78, 187, 54]
cipher_shortened = [234, 59, 113, 243, 94, 4, 42, 41, 199, 240, 28, 78, 187, 54]    # be pirmo simbolio

# sifras dvejetainiu formatu
cipher_bin = []
for c in cipher_shortened:
    for b in decimal_to_bits(c):
        cipher_bin.append(b)

registers = [1, 0, 0, 1, 0, 0, 1, 0]    # k9 - k2
coeficients = [1, 1, 0, 1, 0, 0, 0, 1]
message_bin = [] 
for c in cipher_bin:
    message_bin.append(c ^ registers[0])
    # nauja registro reiksme
    res = 0
    for i in range(0, 8):
        res += registers[i] * coeficients[i]
    res %= 2
    registers = [res] + registers[0:7]

message = ''
for m in chunks(message_bin, 8):
    message += chr(bits_to_decimal(m))

print(message)
# print(chunks(message, 8))
# print(bits_to_decimal(registers))
