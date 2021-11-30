#Imports
import pandas as pd
import os
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure


import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-I',
    '--idir',
    default='./ngrams',
    help='Input directory path which stores the csv files creating ngrams. Default is "./ngrams".',
    type=str)
args = parser.parse_args()

ifiles = ['bigram.csv','trigram.csv','fourgram.csv','fivegram.csv']

def change_width(ax, new_value):
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

def get_name(row):
    label = row[0]
    for i in range(1,len(row)-1):
        label = label + "_" + row[i]
    return(label)

def get_gram(row):
    if row.size == 4:
        return("Bigrams")
    elif row.size == 5:
        return("Trigrams")
    elif row.size == 6:
        return("Four-grams")
    elif row.size == 7:
        return("Five-grams")
    

df_new = pd.DataFrame()
for file in ifiles:

    df = pd.read_csv(args.idir + "\\" + file, header=None)
    df.sort_values(by=df.columns[len(df.columns)-1], ascending=False, inplace=True)
    df_top_10 = df.head(10)
    df_top_10[len(df_top_10.columns)]=df_top_10.apply(get_name,axis=1)
    df_top_10[len(df_top_10.columns)]=df_top_10.apply(get_gram,axis=1)
    df_seq_count = pd.DataFrame(list(zip(df_top_10[len(df_top_10.columns)-2], df_top_10[len(df_top_10.columns)-3], df_top_10[len(df_top_10.columns)-1])))
    df_new = pd.concat([df_new, df_seq_count])

fig, ax = plt.subplots(figsize=(12,6))
g=sns.barplot(data=df_new, x=df_new[0], y=df_new[1], hue=df_new[2], edgecolor='black', palette="Set3",  dodge=False)
plt.grid(True, which='major', linestyle='dashed', axis='y')
plt.margins(x=0)
g.set_xlabel(None)
plt.xticks(rotation=90, fontsize=13)
plt.yticks(fontsize=13)
plt.ylabel("Count", fontsize=15)
plt.legend(fontsize=13, loc='upper right', ncol=4)
g.legend_.set_title(None)
change_width(ax, 1)
plt.ylim(0,8000)
plt.tight_layout()
plt.savefig("./ngram.pdf")
# plt.show()
plt.clf()

