'''
Created on Oct 9, 2013

@author: tomas
'''

from scipy import stats
import math

seq1 = '10101101010110101100110100101001101100111110100111000001100100010100111010001101100110010011001001101001010110001000111100001010100101001110100110110001101010111100011010110001001011101011010000101001011100100010000111001010101100010110001011001101100110100001011001100101110101001010010100110110000011001001100010110011001010111101101010000011010001'
seq2 = '10000111000001100000110000101000110100101010000111000010100010110000011000101100000110001011000101100010010010001001000100001110001111000110100011110000101000100100100110010011000010100001010001001001001100011110010101001010100001110000111001000100001110000011000111100011010000011000010100011110001001000101100001110010001001001100010110010101001001'

def bit_count(seq):
    zeros, ones = 0, 0
    for s in seq:
        if s == '0':
            zeros += 1
        elif s == '1':
            ones += 1
    return [zeros, ones]

def bits_to_decimal(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | int(bit)
    return out

def simple_bit_test(seq):
    counts = bit_count(seq)
    return float((counts[0] - counts[1])**2) / float(len(seq))
    
def bit_pair_test(seq):
    n00, n01, n10, n11 = 0, 0, 0, 0
    for i in range(0, len(seq) - 1):
        pair = seq[i:i+2]
        if pair == '00':
            n00 += 1
        elif pair == '01':
            n01 += 1
        elif pair == '10':
            n10 += 1
        elif pair == '11':
            n11 += 1
    pair_square_sum = n00 **2 + n01 **2 + n10 **2 + n11 **2
    bit_square_sum = bit_count(seq)[0] **2 + bit_count(seq)[1] **2
    n = len(seq)
    return ((4.0 / (n - 1))) * float(pair_square_sum) - ((2.0 / n) * float(bit_square_sum)) + 1

def poker_test(seq, m):
    n = len(seq)
    if (m >= n):
        return None
    # zodziu skaicius
    k = n / m
    word_count = 2**m
    # zodis atvaizduojamas eilutes dalimi paversta i desimtaini skaiciu ir naudojamas kaip masyvo indeksas
    words = [0] * word_count
    for i in range(0, k):
        word = bits_to_decimal(seq[i*m:i*m + m])
        words[word] += 1
    
    # statistika
    t = (float(word_count) / float(k)) * float(sum([x**2 - k for x in words]))
    return t

def autocor_test(seq, d):
    n = len(seq)
    xor_sum = 0
    for i in range(0, n - d + 1):
        xor_sum += int(seq[i]) ^ int(seq[i + d - 1])
    return float(2 * xor_sum - n + d) / math.sqrt(n - d)

# def poker_test(seq):

# print(simple_bit_test(seq1))
# print(stats.chi2.cdf(simple_bit_test(seq1), 1))

print("Pavieniu bitu testas")
print(1 - stats.chi2.cdf(simple_bit_test(seq1), 1))
print(1 - stats.chi2.cdf(simple_bit_test(seq2), 1))

print("\nBitu poru testas")
print(1 - stats.chi2.cdf(bit_pair_test(seq1), 2))
print(1 - stats.chi2.cdf(bit_pair_test(seq2), 2))

print("\nPokerio testas")
m = 5
print(1 - stats.chi2.cdf(poker_test(seq1, m), 2**m - 1))
print(1 - stats.chi2.cdf(poker_test(seq2, m), 2**m - 1))

# print(autocor_test('1011101110', 3))
print("\nAutokoreliacijos testas")
d = 20
t1, t2 = autocor_test(seq1, d), autocor_test(seq2, d)
c1, c2 = stats.norm.cdf(t1), stats.norm.cdf(t2)
p1 = c1 if t1 < 0 else 1.0 - c1
p2 = c2 if t2 < 0 else 1.0 - c2

print(p1)
print(p2)

# (-4.965212315030781, -7.390083445627209)