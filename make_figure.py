import numpy as numpy
import pandas as pd

# Use Agg instead of Xwindows or run ssh -X (comment out these lines)
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# Select session id for figure
name = open("data/id.txt")
session_id = name.readline()
name.close()

# Read delimited session string from file, convert to 2d array
f = open('data/session-'+session_id+'.txt', 'r')
data = f.read().split(",")
del data[-1]
data = [float(i) for i in data]
frames = [data[i*4:(i+1)*4] for i in range(len(data)//4)]

# Generate plot and save to /figures
df = pd.DataFrame(frames, columns=['c09-13', 'c09-14', 'c09-15', 'c09-16'])
plt.figure()
df.plot()
plt.savefig('figures/'+session_id+'.png')
