#!/usr/bin/env python
# coding: utf-8

# For now, I am replacing generic labels such as W1, Itr2, and V1
# with hard-coded actual values, i.e., 20g, NABH4, and 100mm/s.
# This is only for the paper.
# In future, while we want more useful labels, these should be
# derived from the csv files itself
# (e.g., from the header row or from the file name)

import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('../CSV-Files/WEIGHTS-PLOT.csv')

w1 = data['W1_0'].tolist()
w2 = data['W2_0'].tolist()
w3 = data['W3_0'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, w1, label='20 g')
ax.plot(ts, w2, label='500 g', linestyle='dashed')
ax.plot(ts, w3, label='1000 g', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j0-weight.pdf")
plt.clf()

w1 = data['W1_1'].tolist()
w2 = data['W2_1'].tolist()
w3 = data['W3_1'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, w1, label='20 g')
ax.plot(ts, w2, label='500 g', linestyle='dashed')
ax.plot(ts, w3, label='1000 g', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j1-weight.pdf")
plt.clf()


w1 = data['W1_2'].tolist()
w2 = data['W2_2'].tolist()
w3 = data['W3_2'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, w1, label='20 g')
ax.plot(ts, w2, label='500 g', linestyle='dashed')
ax.plot(ts, w3, label='1000 g', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j2-weight.pdf")
plt.clf()


w1 = data['W1_3'].tolist()
w2 = data['W2_3'].tolist()
w3 = data['W3_3'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, w1, label='20 g')
ax.plot(ts, w2, label='500 g', linestyle='dashed')
ax.plot(ts, w3, label='1000 g', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j3-weight.pdf")
plt.clf()


w1 = data['W1_4'].tolist()
w2 = data['W2_4'].tolist()
w3 = data['W3_4'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, w1, label='20 g')
ax.plot(ts, w2, label='500 g', linestyle='dashed')
ax.plot(ts, w3, label='1000 g', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j4-weight.pdf")
plt.clf()


w1 = data['W1_5'].tolist()
w2 = data['W2_5'].tolist()
w3 = data['W3_5'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, w1, label='20 g')
ax.plot(ts, w2, label='500 g', linestyle='dashed')
ax.plot(ts, w3, label='1000 g', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j5-weight.pdf")
plt.clf()


data = pd.read_csv('../CSV-Files/VELOCITY-PLOT.csv')
data.head()

V1 = data['V100_0'].tolist()
V2 = data['V200_0'].tolist()
V3 = data['V250_0'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#ax.plot(ts, V1, label='100 mm/s')
ax.plot(ts, V1, label='100 mm/s', linestyle='solid')
ax.plot(ts, V2, label='200 mm/s', linestyle='dashed')
ax.plot(ts, V3, label='250 mm/s', linestyle='dotted')
#ax.plot(ts, V5, label='V5', linestyle='dashed')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j0-vel.pdf")
plt.clf()


V1 = data['V100_1'].tolist()
V2 = data['V200_1'].tolist()
V3 = data['V250_1'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#ax.plot(ts, V1, label='100 mm/s')
ax.plot(ts, V1, label='100 mm/s', linestyle='solid')
ax.plot(ts, V2, label='200 mm/s', linestyle='dashed')
ax.plot(ts, V3, label='250 mm/s', linestyle='dotted')
#ax.plot(ts, V5, label='V5', linestyle='dashed')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j1-vel.pdf")
plt.clf()


V1 = data['V100_2'].tolist()
V2 = data['V200_2'].tolist()
V3 = data['V250_2'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, V1, label='100 mm/s')
ax.plot(ts, V2, label='200 mm/s', linestyle='dashed')
ax.plot(ts, V3, label='250 mm/s', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j2-vel.pdf")
plt.clf()


V1 = data['V100_3'].tolist()
V2 = data['V200_3'].tolist()
V3 = data['V250_3'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, V1, label='100 mm/s')
ax.plot(ts, V2, label='200 mm/s', linestyle='dashed')
ax.plot(ts, V3, label='250 mm/s', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j3-vel.pdf")
plt.clf()

V1 = data['V100_4'].tolist()
V2 = data['V200_4'].tolist()
V3 = data['V250_4'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, V1, label='100 mm/s')
ax.plot(ts, V2, label='200 mm/s', linestyle='dashed')
ax.plot(ts, V3, label='250 mm/s', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j4-vel.pdf")
plt.clf()


V1 = data['V100_5'].tolist()
V2 = data['V200_5'].tolist()
V3 = data['V250_5'].tolist()
ts = data['TimeStamp'].tolist()

fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, V1, label='100 mm/s')
ax.plot(ts, V2, label='200 mm/s', linestyle='dashed')
ax.plot(ts, V3, label='250 mm/s', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j5-vel.pdf")
plt.clf()


data = pd.read_csv('../CSV-Files/ITERATION-PLOTS.csv')

I1 = data['itr1_0'].tolist()
I2 = data['itr2_0'].tolist()
I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()


fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI', linestyle='dashed')
ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j0-itr.pdf")
plt.clf()


I1 = data['itr1_1'].tolist()
I2 = data['itr2_1'].tolist()
I3 = data['itr3_1'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI', linestyle='dashed')
ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j1-itr.pdf")
plt.clf()


I1 = data['itr1_3'].tolist()
I2 = data['itr2_3'].tolist()
I3 = data['itr3_3'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI', linestyle='dashed')
ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j3-itr.pdf")
plt.clf()

I1 = data['itr1_4'].tolist()
I2 = data['itr2_4'].tolist()
I3 = data['itr3_4'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI')
ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j4-itr.pdf")
plt.clf()

I1 = data['itr1_5'].tolist()
I2 = data['itr2_5'].tolist()
I3 = data['itr3_5'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI', linestyle='dashed')
ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j5-itr.pdf")
plt.clf()


I1 = data['itr1_2'].tolist()
I2 = data['itr2_2'].tolist()
I3 = data['itr3_2'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI', linestyle='dashed')
ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j2-itr.pdf")
plt.clf()


I1 = data['itr1_0'].tolist()
#I2 = data['itr2_0'].tolist()
#I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts, I1, label='NABH4')
#ax.plot(ts, I2, label='CSTI', linestyle='dashed')
#ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)

I2 = data['itr2_0'].tolist()
#I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#ax.plot(ts, I1, label='NABH4')
ax.plot(ts, I2, label='CSTI', color='orange')
#ax.plot(ts, I3, label='GENTISTIC', linestyle='dotted')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)


I3 = data['itr3_0'].tolist()
ts = data['TimeStamp'].tolist()
fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#ax.plot(ts, I1, label='NABH4')
#ax.plot(ts, I2, label='CSTI', linestyle='dashed')
ax.plot(ts, I3, label='GENTISTIC', color='green')
ax.legend(fontsize=15)
ax.set_ylim((-1.5, 2.5))
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.clf()


##########


data0= pd.read_csv('../CSV-Files/l0l1.csv')
data1= pd.read_csv('../CSV-Files/l1l2.csv')
data2= pd.read_csv('../CSV-Files/l2l3.csv')
data3= pd.read_csv('../CSV-Files/l3l4.csv')
data4= pd.read_csv('../CSV-Files/l4l5.csv')

C0 = data0['actual_current_1'].tolist()
ts0 = data0['time'].tolist()
C1 = data1['actual_current_1'].tolist()
ts1 = data1['time'].tolist()
C2 = data2['actual_current_1'].tolist()
ts2 = data2['time'].tolist()
C3 = data3['actual_current_1'].tolist()
ts3 = data3['time'].tolist()
C4 = data4['actual_current_1'].tolist()
ts4 = data4['time'].tolist()

fig, ax= plt.subplots(figsize=(6, 5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax.plot(ts0, C0, label='L0-L1', linestyle='solid')
ax.plot(ts1, C1, label='L1-L2', linestyle='dashed')
ax.plot(ts2, C2, label='L2-L3', linestyle='dotted')
ax.plot(ts3, C3, label='L3-L4', linestyle='dashdot')
ax.plot(ts4, C4, label='L4-L5', linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.set_ylim((-1.5, 2.5))
ax.legend(fontsize=15, loc='upper left', ncol=3)
plt.xlabel('Ticks (1 tick = 40 ms)', fontsize=17)
plt.ylabel('Current (ma)', fontsize=17)
plt.tight_layout()
plt.savefig("j1-l1l2l3l4l5.pdf")
