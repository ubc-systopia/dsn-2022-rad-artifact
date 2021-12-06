#Imports
import pandas as pd
import os
import glob
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer


mport argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-I',
    '--idir',
    default='./ngrams',
    help='Input directory path which stores the csv files creating ngrams. Default is "./ngrams".',
    type=str)
args = parser.parse_args()


def main():
    file_list = os.listdir(args.idir)
    print(file_list)

    # Experiment,Timestamp,Module,Method_Name,Arguments,Responses,Exceptions,Anomaly (Yes/No)

    li = []
    file_index=[]
    for item in file_list:
        if item.startswith("2021"):
            df = pd.read_csv(args.idir + item, index_col=False, header = 0)
            if (len(df.index) > 1):
                print(item)
                print(list(df))
                df = df[['Timestamp', 'Module', 'Method_Name', 'Arguments', 'Responses', 'Exceptions']]
                # Add a row delimiter between individual experiment files
                #new_row = {'Experiment': -1, 'Timestamp': -1, 'Module': -1, 'Method_Name': -1, 'Arguments': -1, 'Responses': -1, 'Exceptions': -1, 'Anomaly (Yes/No)': -1}
                procedure_list = df['Method_Name'].to_list()
                print(procedure_list)
                li.append(procedure_list)
                file_index.append(item)

    ofile = args.idir + "procedure_list_all.csv"

    print("... %s" %ofile)
    if os.path.isfile(ofile):
        print('WARNING: This file already exists!')
        os.remove(ofile)

    with open(ofile, 'w') as f:
        for item in li:
            for val in item:
                f.write("%s\n" % val)
            f.write("-1 \n")


    bigram_dict={}
    trigram_dict={}
    fourgram_dict={}
    fivegram_dict={}

    lcss_score=[]

    # Bigrams
    for item in li:
        for i in range(0, len(item)-1):
            value=item[i]+"_"+item[i+1]
            if value in bigram_dict.keys():
                bigram_dict[value] +=1
            else:
                bigram_dict[value] = 1

    # Trigrams
    for item in li:
        for i in range(0, len(item)-2):
            value=item[i]+"_"+item[i+1] + "_" + item[i+2]
            if value in trigram_dict.keys():
                trigram_dict[value] +=1
            else:
                trigram_dict[value] = 1

    # 4grams
    for item in li:
        for i in range(0, len(item)-3):
            value=item[i]+"_"+item[i+1] + "_" + item[i+2] + "_" + item[i+3]
            if value in fourgram_dict.keys():
                fourgram_dict[value] +=1
            else:
                fourgram_dict[value] = 1

    # 5grams
    for item in li:
        for i in range(0, len(item) - 4):
            value = item[i] + "_" + item[i + 1] + "_" + item[i + 2] + "_" + item[i + 3] + "_" + item[i + 4]
            if value in fivegram_dict.keys():
                fivegram_dict[value] += 1
            else:
                fivegram_dict[value] = 1

    # Order the dictionaries
    bigram_dict_sorted = sorted(bigram_dict, key=bigram_dict.get, reverse=True)
    i=0
    bi_key_list=[]
    bi_val_list =[]
    for r in bigram_dict_sorted:
        print(r, bigram_dict[r])
        bi_key_list.append(r)
        bi_val_list.append(bigram_dict[r])
        i+=1
        if i >10:
            break

    trigram_dict_sorted = sorted(trigram_dict, key=trigram_dict.get, reverse=True)
    i = 0
    tri_key_list = []
    tri_val_list = []
    for r in trigram_dict_sorted:
        print(r, trigram_dict[r])
        tri_key_list.append(r)
        tri_val_list.append(trigram_dict[r])
        i += 1
        if i > 10:
            break

    fourgram_dict_sorted = sorted(fourgram_dict, key=fourgram_dict.get, reverse=True)
    i = 0
    four_key_list = []
    four_val_list = []
    for r in fourgram_dict_sorted:
        print(r, fourgram_dict[r])
        four_key_list.append(r)
        four_val_list.append(fourgram_dict[r])
        i += 1
        if i > 10:
            break

    fivegram_dict_sorted = sorted(fivegram_dict, key=fivegram_dict.get, reverse=True)
    i = 0
    five_key_list = []
    five_val_list = []
    for r in fivegram_dict_sorted:
        print(r, fivegram_dict[r])
        five_key_list.append(r)
        five_val_list.append(fivegram_dict[r])
        i += 1
        if i > 10:
            break

    #bigram_dict= sorted(bigram_dict.items(), key=lambda x: x[1], reverse=True)
    #trigram_dict= sorted(trigram_dict.items(), key=lambda x: x[1], reverse=True)
    #fourgram_dict= sorted(fourgram_dict.items(), key=lambda x: x[1], reverse=True)


    # Print the grams_dictionary
    #bigram_key_list = list(bigram_dict.keys())
    #bigram_val_list = list(bigram_dict.values())

    #trigram_key_list = list(trigram_dict.keys())
    #trigram_val_list = list(trigram_dict.values())

    #fourgram_key_list = list(fourgram_dict.keys())
    #fourgram_val_list = list(fourgram_dict.values())

    # Dataframe and plot
    bi_df = pd.DataFrame(
        {'keys': bi_key_list,
         'values': bi_val_list
         })

    tri_df = pd.DataFrame(
        {'keys': tri_key_list,
         'values': tri_val_list
         })

    four_df = pd.DataFrame(
        {'keys': four_key_list,
         'values': four_val_list
         })

    five_df = pd.DataFrame(
        {'keys': five_key_list,
         'values': five_val_list
         })

    bi_df['log_count'] = np.log(1 + bi_df['values'])
    print(bi_df['log_count'].tolist())

    tri_df['log_count'] = np.log(1 + tri_df['values'])
    print(tri_df['log_count'].tolist())

    four_df['log_count'] = np.log(1 + four_df['values'])
    print(four_df['log_count'].tolist())

    five_df['log_count'] = np.log(1 + five_df['values'])
    print(five_df['log_count'].tolist())

    print(bi_df['values'].tolist())
    print(tri_df['values'].tolist())
    print(four_df['values'].tolist())
    print(five_df['values'].tolist())

    # Plots
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="values", y="keys", data=bi_df)
    plt.xlabel("Frequency", fontsize=18)
    plt.ylabel("Bigrams", fontsize=18)
    plt.tight_layout()
    plt.savefig("./Bigram_barplot.pdf")
    plt.show()
    plt.clf()

    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="values", y="keys", data=tri_df)
    plt.xlabel("Frequency", fontsize=18)
    plt.ylabel("Trigrams", fontsize=18)
    plt.tight_layout()
    plt.savefig("./Trigram_barplot.pdf")
    plt.show()
    plt.clf()

    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="values", y="keys", data=four_df)
    plt.xlabel("Frequency", fontsize=18)
    plt.ylabel("Fourgrams", fontsize=18)
    plt.tight_layout()
    plt.savefig("./Fourgram_barplot.pdf")
    plt.show()
    plt.clf()

    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="values", y="keys", data=five_df)
    plt.xlabel("Frequency", fontsize=18)
    plt.ylabel("Fivegrams", fontsize=18)
    plt.tight_layout()
    plt.savefig("./Fivegram_barplot.pdf")
    plt.show()
    plt.clf()

    # Similarity
    corpus = []
    for index in [0,4,6,14,16,24,25,7,2,3,10,8, #Joystick
                  21,
                  20,17,18,19,
                  #23,15,12,11, # Crystal Solubility
                  11,15,12,23,  # Crystal Solubility
                  #22,
                  1,13,5,9]:
        str_val = " ".join(li[index])
        corpus.append(str_val)
        print(len(corpus),file_index[index])

    #for item in li:
    #    str_val = " ".join(item)
    #    corpus.append(str_val)

    """ Old text
    for index in [0,33,34,6,9,11,12,13,20,16,2,23,4,29,3,14,18,21,24,32,1,17,19,22,25,26,28,31,7,15,5,8,10,35,30,36,27]:
    str_val = " ".join(li[index])
    corpus.append(str_val)
    """

    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T

    print(pairwise_similarity)
    print(pairwise_similarity.toarray())
    print(len(li))
    plt.imshow(pairwise_similarity.toarray(), cmap='Spectral', interpolation='nearest')
    plt.colorbar()
    #plt.xticks(np.arange(1, 26, step=2))
    #plt.yticks(np.arange(1, 26, step=2))
    plt.xlabel("Procedure ID", fontsize=15)
    plt.ylabel("Procedure ID", fontsize=15)
    plt.savefig("./tfidf_colorbar_spectral.pdf")
    plt.tight_layout()
    plt.show()
    plt.clf()

    sns.heatmap(pairwise_similarity.toarray(), linewidth=0.5)
    plt.xlabel("Procedure ID", fontsize=15)
    plt.ylabel("Procedure ID", fontsize=15)
    plt.tight_layout()
    plt.savefig("./tfidf.pdf")
    #plt.show()
    plt.clf()

    #print(">>>>>")
    #print(corpus)
    #print(">>>>>>")
    #print(li)
    #print("Li printed")

    """
    lcss_str = []
    lcss_scores=[]

    for i in range(0,len(corpus)):
        row_scores = []
        row_string=[]
        for j in range(0, len(corpus)):
            #print(li[i], li[j])
            score = lcs(",".join(li[i]), ",".join(li[j]))
            print(score, i,j,len(li), len(score))
            print("****>>>>****")
            row_string.append(score)
            row_scores.append(len(score))
        lcss_str.append(row_string)
        lcss_scores.append(row_scores)

    #print(len(lcss_scores), len(lcss_scores[0]), len(lcss_scores[-1]),len(li))
    #print(lcss_str)
    print(lcss_scores)
    """

    #for i in lcss_scores:
    #    for j in i:
    #        print(j)
    #    print("\n")

    return 0

if __name__ == "__main__":
    main()
