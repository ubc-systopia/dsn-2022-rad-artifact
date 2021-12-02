# Author : Amee Trivedi
# Objective: Compute the probability of a cmd sequence occuring

import pandas as pd
import os
import glob
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-I',
    '--idir',
    help='Provide path to the directory containing the .csv files. Default is the current directory.',
    type=str)
parser.add_argument(
    '-E',
    '--ifile_ext',
    default='.csv',
    help='Default file extension is ".csv". If the default extension is not used, provide an alternative.',
    type=str)
args = parser.parse_args()

file_index2 = ["20211018130924-1",  # 0
               "20211018132502-1",
               "20211018133320-1",
               "20211018135445-1",
               "20211018140458-1",
               "20211018141513-1",  # 5
               "20211019142004-1",
               "20211019142656-1",
               "20211019143332-1",
               "20211019144058-1",
               "20211019144749-1",  # 10
               "20211019145355-1",
               "20211012145802-1",
               "20211012150440-1",
               "20211012132024-1",
               "20211012143509-1",  # 15
               "20211013110848-1",  # A
               "20211013113911-1",  # A
               "20211015125921-1",
               "20211013115553-1",
               "20211015132125-1",  # 20
               "20211020125006-1",
               "20211020130134-1",  # A
               "20211022151947-1",
               "20211022152644-1"]  # 24

def compute_transition_prob():
    li = []
    li2 = []
    file_index1 = []
    t_regex = "Order1_MC_transition_"

    for item1 in file_index2:
        # first aggregate all the
        leave_out_sample = item1
        for item2 in file_index2:
            if item2 != leave_out_sample:
                df = pd.read_csv(args.idir + item2 + args.ifile_ext, index_col=False, header = 0)
                if (len(df.index) > 1):
                    print(item2)
                    print(list(df))
                    df = df[['Timestamp', 'Module', 'Method_Name', 'Arguments', 'Responses', 'Exceptions']]
                    # Add a row delimiter between individual experiment files
                    #new_row = {'Experiment': -1, 'Timestamp': -1, 'Module': -1, 'Method_Name': -1, 'Arguments': -1, 'Responses': -1, 'Exceptions': -1, 'Anomaly (Yes/No)': -1}
                    procedure_list = df['Method_Name'].to_list()
                    #print(procedure_list)
                    li.append(procedure_list)
                    file_index1.append(item2)

        # Compute the transition probability
        bigram_dict = {}
        for item in li:
            for i in range(0, len(item) - 1):
                value = item[i] + ":" + item[i + 1]
                if value in bigram_dict.keys():
                    bigram_dict[value] += 1
                else:
                    bigram_dict[value] = 1

        # Save the transition probability of the current training set using the name of the leave-one-out sample
        with open(args.idir + t_regex + item1 + ".csv", 'w') as f:
            for k, v in sorted(bigram_dict.items()):
                f.write('{}, {}, {} \n'.format(k.split(":")[0], k.split(":")[1], v))

        df_transition = pd.read_csv(args.idir + t_regex + item1 + ".csv", index_col=False, names = ["current_state", "next_state", "count"])

        # compute the probability of each transition
        df_transition['marginal'] = df_transition['count'].groupby(df_transition['current_state']).transform('sum')
        df_transition["probability"] = df_transition['count']/df_transition['marginal']
        print(df_transition)

        df_transition.to_csv(args.idir + t_regex + item1 + ".csv", index=False)
        print(args.idir + t_regex + item1 + ".csv")
        #break

    return(t_regex)

def clean_curr_state(row):
    return(row["current_state"].strip())

def clean_next_state(row):
    return(row["next_state"].strip())

def compute_perplexity_score(t_regex):
    perplexity = []
    file_name = []

    for item1 in file_index2:
        total_pp_value = 0
        current_prob = 0

        print(item1)
        # Get the transition matrix
        df_transition = pd.read_csv(args.idir + t_regex + item1 + ".csv", index_col=False)
        print(df_transition)

        df_transition["current_state_clean"] = df_transition.apply(clean_curr_state,axis=1)
        df_transition["next_state_clean"] = df_transition.apply(clean_next_state,axis=1)

        # Now read the command sequence (the leave one out sample)
        df_cmd = pd.read_csv(args.idir + item1 + args.ifile_ext, index_col=False, header=0)
        test_procedure_list = df_cmd['Method_Name'].to_list()

        # Now calculate the perplexity as log probability
        for i in range(0, len(test_procedure_list)-1):
            current_cmd = test_procedure_list[i]
            next_cmd = test_procedure_list[i+1]

            #print(current_cmd, next_cmd, len(next_cmd))
            subset = df_transition.loc[(df_transition['current_state_clean'] == current_cmd.strip()) &
                                                (df_transition['next_state_clean'] == next_cmd.strip())]
            #print(subset)
            #print(">>>>>>")
            #print(subset["probability"])
            transition_prob = subset.iloc[0]["probability"]
            #print(transition_prob, np.log2(transition_prob))
            total_pp_value += np.log2(transition_prob)
            #print(total_pp_value)

        print("-------")
        print(total_pp_value)

        perplexity_score = -1*total_pp_value/len(test_procedure_list)
        print(total_pp_value, perplexity_score)

        perplexity.append(perplexity_score)
        file_name.append(item1)
        #break

        for i in range(0, len(file_name)):
            print(file_name[i], perplexity[i])

    return(perplexity)

def main():
    ## Compute the transition probability matrix for each file using a leave-one-out method
    tfile_regex = compute_transition_prob()
    ## Compute the perplexity score of each command sequence using log base 2
    perplexity_score = compute_perplexity_score(tfile_regex)
    print(perplexity_score)

    #perplexity_score = [1.1115205294028037, 0.8989529841568795, 0.6760381720572242, 0.8270756881686195, 0.812460576004786, 0.61835329579532, 1.421211149856776, 0.8938517820962318, 0.6278822191705873, 0.8145995050445625, 0.6969933801768224, 0.6186205267537022, 1.0807032580673483, 1.6697602861505494, 1.182306691474293, 1.4423023938697614, 1.642970991660042, 1.6223093599628327, 1.3139557349365982, 1.4460432836466663, 1.4123127413488494, 1.4689743188405198, 1.677376594224576, 1.446511311099156, 1.26097023775061]
    e_pp = []
    for i in range(0, len(perplexity_score)):
        print(np.exp(perplexity_score[i]))
        e_pp.append(np.exp(perplexity_score[i]))

    # Scatter Plot of e_pp
    #Proc = [["Joystick"]*12, ["AS"]*5, ["AS_UR3"]*4, ["CSP"]*4]
    Proc = [["P4"] * 12, ["P1"] * 5, ["P2"] * 4, ["P3"] * 4]
    Proc_list = [item for sublist in Proc for item in sublist]
    anom_list = ["No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","Yes","Yes","Yes","No","No","No","No","No","No"]

    df= pd.DataFrame({"Value":e_pp, "ID": np.arange(0,25), "Procedure": Proc_list, "Anomaly":anom_list})
    sns.scatterplot(data=df, x="ID", y="Value", hue="Procedure", style="Anomaly")
    plt.xlabel("Procedure ID", fontsize=18)
    plt.ylabel("Perplexity Score", fontsize=18)
    plt.tight_layout()
    plt.savefig("./perplexity_score.pdf")
    # plt.show()

    #sns.scatterplot(data=df, x="ID", y="Value", hue="Procedure", style="Anomaly")
    sns.boxplot(x="Procedure", y="Value", hue="Anomaly", data=df)
    plt.xlabel("Procedure Type")
    plt.ylabel("Perplexity Score")
    plt.tight_layout()
    plt.savefig("./perplexity_score_boxplot.pdf")
    # plt.show()
    plt.clf()


    # sns.scatterplot(data=df, x="ID", y="Value", hue="Procedure", style="Anomaly")
    plt.figure(figsize=(3, 6))
    sns.boxplot(x="Procedure", y="Value", data=df)
    plt.xlabel("Procedure Type", fontsize=15)
    plt.ylabel("Perplexity Score", fontsize=15)
    plt.ylim(1,6)
    plt.tight_layout()
    plt.savefig("./perplexity_score_boxplot_nohue.pdf",  bbox_inches='tight', pad_inches=0.1)
    # plt.show()

if __name__ == "__main__":
    main()