#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('../CSV-Files/WEIGHTS-PLOT.csv')

w1 = data['W1_0'].tolist()
w2 = data['W2_0'].tolist()
w3 = data['W3_0'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots()
ax.plot(ts, w1, label='W1')
ax.plot(ts, w2, label='W2', linestyle='dashed')
ax.plot(ts, w3, label='W3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j0-weight.pdf")

w1 = data['W1_1'].tolist()
w2 = data['W2_1'].tolist()
w3 = data['W3_1'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots()
ax.plot(ts, w1, label='W1')
ax.plot(ts, w2, label='W2', linestyle='dashed')
ax.plot(ts, w3, label='W3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j1-weight.pdf")


w1 = data['W1_2'].tolist()
w2 = data['W2_2'].tolist()
w3 = data['W3_2'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, w1, label='W1')
ax.plot(ts, w2, label='W2', linestyle='dashed')
ax.plot(ts, w3, label='W3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j2-weight.pdf")


w1 = data['W1_3'].tolist()
w2 = data['W2_3'].tolist()
w3 = data['W3_3'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, w1, label='W1')
ax.plot(ts, w2, label='W2', linestyle='dashed')
ax.plot(ts, w3, label='W3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j3-weight.pdf")


w1 = data['W1_4'].tolist()
w2 = data['W2_4'].tolist()
w3 = data['W3_4'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, w1, label='W1')
ax.plot(ts, w2, label='W2', linestyle='dashed')
ax.plot(ts, w3, label='W3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j4-weight.pdf")


w1 = data['W1_5'].tolist()
w2 = data['W2_5'].tolist()
w3 = data['W3_5'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, w1, label='W1')
ax.plot(ts, w2, label='W2', linestyle='dashed')
ax.plot(ts, w3, label='W3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j5-weight.pdf")


data = pd.read_csv('../CSV-Files/VELOCITY-PLOT.csv')
data.head()

V1 = data['V100_0'].tolist()
V2 = data['V200_0'].tolist()
V3 = data['V250_0'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots()
#ax.plot(ts, V1, label='V1')
ax.plot(ts, V1, label='V1', linestyle='dashed')
ax.plot(ts, V2, label='V2', linestyle='dashed')
ax.plot(ts, V3, label='V3', linestyle='dashed')
#ax.plot(ts, V5, label='V5', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j0-vel.pdf")


V1 = data['V100_1'].tolist()
V2 = data['V200_1'].tolist()
V3 = data['V250_1'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
#ax.plot(ts, V1, label='V1')
ax.plot(ts, V1, label='V1', linestyle='dashed')
ax.plot(ts, V2, label='V2', linestyle='dashed')
ax.plot(ts, V3, label='V3', linestyle='dashed')
#ax.plot(ts, V5, label='V5', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j1-vel.pdf")


V1 = data['V100_2'].tolist()
V2 = data['V200_2'].tolist()
V3 = data['V250_2'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, V1, label='V1')
ax.plot(ts, V2, label='V2', linestyle='dashed')
ax.plot(ts, V3, label='V3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j2-vel.pdf")


V1 = data['V100_3'].tolist()
V2 = data['V200_3'].tolist()
V3 = data['V250_3'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, V1, label='V1')
ax.plot(ts, V2, label='V2', linestyle='dashed')
ax.plot(ts, V3, label='V3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j3-vel.pdf")

V1 = data['V100_4'].tolist()
V2 = data['V200_4'].tolist()
V3 = data['V250_4'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, V1, label='V1')
ax.plot(ts, V2, label='V2', linestyle='dashed')
ax.plot(ts, V3, label='V3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j4-vel.pdf")


V1 = data['V100_5'].tolist()
V2 = data['V200_5'].tolist()
V3 = data['V250_5'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots()
ax.plot(ts, V1, label='V1')
ax.plot(ts, V2, label='V2', linestyle='dashed')
ax.plot(ts, V3, label='V3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j5-vel.pdf")


data = pd.read_csv('../CSV-Files/ITERATION-PLOTS.csv')

I1 = data['itr1_0'].tolist()
I2 = data['itr2_0'].tolist()
I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2', linestyle='dashed')
ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j0-itr.pdf")


I1 = data['itr1_1'].tolist()
I2 = data['itr2_1'].tolist()
I3 = data['itr3_1'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2', linestyle='dashed')
ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j1-itr.pdf")


I1 = data['itr1_3'].tolist()
I2 = data['itr2_3'].tolist()
I3 = data['itr3_3'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2', linestyle='dashed')
ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j3-itr.pdf")

I1 = data['itr1_4'].tolist()
I2 = data['itr2_4'].tolist()
I3 = data['itr3_4'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2')
ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j4-itr.pdf")

I1 = data['itr1_5'].tolist()
I2 = data['itr2_5'].tolist()
I3 = data['itr3_5'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2', linestyle='dashed')
ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j5-itr.pdf")


I1 = data['itr1_2'].tolist()
I2 = data['itr2_2'].tolist()
I3 = data['itr3_2'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2', linestyle='dashed')
ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
plt.savefig("j2-itr.pdf")


I1 = data['itr1_0'].tolist()
#I2 = data['itr2_0'].tolist()
#I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
ax.plot(ts, I1, label='Itr1')
#ax.plot(ts, I2, label='Itr2', linestyle='dashed')
#ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')

I2 = data['itr2_0'].tolist()
#I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
#ax.plot(ts, I1, label='Itr1')
ax.plot(ts, I2, label='Itr2', color='orange')
#ax.plot(ts, I3, label='Itr3', linestyle='dashed')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')


I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots()
#ax.plot(ts, I1, label='Itr1')
#ax.plot(ts, I2, label='Itr2', linestyle='dashed')
ax.plot(ts, I3, label='Itr3', color='green')
ax.legend()
plt.xlabel('Time(ms)')
plt.ylabel('Current(ma)')
