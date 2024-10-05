import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import signal

f = open("XB.ELYSE.02.BHV.2022-01-02HR04_evid0006.csv")
dataraw = f.readlines()
wsize = 30
data = []
xaxis = []
yaxis = []
yaxis_abs = []
yaxis_abs_wavg = []
xaxis_abs_wavg = []
yaxis_tempo = []
xaxis_tempo = []
avg_tempo = 0

for x in dataraw:
    data.append(x.split(','))
print(data[3])
for x in data[2:]:
    xaxis.append(float(x[1]))
    yaxis.append(float(x[2]))

sr = 20 # liczba sampli na sekundę
ts = max(xaxis)/sr #długość badania
t = np.arange(0,1,ts)
print(t)

for x in data[2:]:
    yaxis_abs.append(abs(float(x[2])))
    #print(x[1],x[2],end='')
    #print(float(x[1])/3600)
for i in range(0,math.ceil((len(xaxis)-wsize)/wsize)):
    #print(i,xaxis[i*wsize])
    yaxis_abs_wavg.append(sum((yaxis[i*wsize:(i+1)*wsize]))/wsize)
    xaxis_abs_wavg.append(i*wsize)

for i in range(0,len(yaxis)-2):
    yaxis_tempo.append(abs(yaxis[i+1] - yaxis[i]))
    xaxis_tempo.append(i)

avg_tempo = sum(yaxis_tempo)/len(yaxis_tempo)

print("avg tempo = ", avg_tempo)

fig, axs = plt.subplots(2,figsize=(19,5))
#plt.axhline(y = avg_tempo, color = 'r', linestyle = '-') 
axs[0].plot(xaxis, yaxis)
axs[0].set(xlabel='time (s)', ylabel='amplitude (eee?)',title='original_data')
axs[0].grid()

axs[1].plot(xaxis_tempo, yaxis_tempo)
axs[1].set(xlabel='ticks', ylabel='amplitude (eee?)',title='tempo')
axs[1].grid()

fig.savefig("test.png",dpi = 1200)
plt.show()