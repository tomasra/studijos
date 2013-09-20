import numpy as np
import pandas as pd
import math as mt
import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            raw_data = line.split()
            entry = {}
            entry['hip'] = int(raw_data[0])
            entry['vmag'] = float(raw_data[1])
            entry['ra'] = float(raw_data[2])
            entry['de'] = float(raw_data[3])
            entry['plx'] = float(raw_data[4])
            entry['pmra'] = float(raw_data[5])
            entry['pmde'] = float(raw_data[6])
            entry['eplx'] = float(raw_data[7])
            if len(raw_data) == 9:
                entry['bv'] = float(raw_data[8])
            else:
                entry['bv'] = None
            data.append(entry)            
    return data
            
data = read_data('HIP_star.dat')

df = pd.DataFrame(data, columns=['bv'])
df.plot()
plt.show()