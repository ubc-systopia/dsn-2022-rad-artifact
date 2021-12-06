import pandas as pd
import os
import glob
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold
import jenkspy

idir=<dataset file path>
ifile_ext=".csv"

file_index_anon = ["20211013110848-1",  # A
                    "20211013113911-1",  # A
                    "20211020130134-1"]  # A

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
    t_regex = "Order1_MC_5CV_transition_"

    # Make the k-folds
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    kf.get_n_splits(file_index2)
    print(kf)

    fold=0
    perplexity = []
    file_name = []

    for train_index, test_index in kf.split(file_index2):
        test = []
        train = []
        print("---------------------------------------------------------------------------------")
        fold += 1
        print(">>> Fold", fold)
        print("TRAIN:", train_index, "TEST:", test_index)

        for index in train_index:
            train.append(file_index2[index])

        for index in test_index:
            test.append(file_index2[index])

        for item2 in train:
            df = pd.read_csv(idir + item2 + ifile_ext, index_col=False, header = 0)
            if (len(df.index) > 1):
                print(item2)
                #print(list(df))
                df = df[['Timestamp', 'Module', 'Method_Name', 'Arguments', 'Responses', 'Exceptions']]
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
        with open(idir + t_regex + "fold" + str(fold) + ".csv", 'w') as f:
            for k, v in sorted(bigram_dict.items()):
                f.write('{}, {}, {} \n'.format(k.split(":")[0], k.split(":")[1], v))

        df_transition = pd.read_csv(idir + t_regex + "fold" + str(fold) + ".csv", index_col=False, names = ["current_state", "next_state", "count"])

        # compute the probability of each transition
        df_transition['marginal'] = df_transition['count'].groupby(df_transition['current_state']).transform('sum')
        df_transition["probability"] = df_transition['count']/df_transition['marginal']
        print(df_transition)

        df_transition.to_csv(idir + t_regex + "fold" + str(fold) + ".csv", index=False)
        print(idir + t_regex + "fold" + str(fold) + ".csv")
        #break

        # Now, compute the perplexity scores for the test dataset
        for item in test:
            total_pp_value = 0

            print(item)
            df_transition["current_state_clean"] = df_transition.apply(clean_curr_state, axis=1)
            df_transition["next_state_clean"] = df_transition.apply(clean_next_state, axis=1)

            # Now read the command sequence (the leave one out sample)
            df_cmd = pd.read_csv(idir + item + ifile_ext, index_col=False, header=0)
            test_procedure_list = df_cmd['Method_Name'].to_list()

            # Now calculate the perplexity as log probability
            for i in range(0, len(test_procedure_list) - 1):
                current_cmd = test_procedure_list[i]
                next_cmd = test_procedure_list[i + 1]

                # print(current_cmd, next_cmd, len(next_cmd))
                subset = df_transition.loc[(df_transition['current_state_clean'] == current_cmd.strip()) &
                                           (df_transition['next_state_clean'] == next_cmd.strip())]
                # print(subset)
                # print(">>>>>>")
                # print(subset["probability"])
                try:
                    transition_prob = subset.iloc[0]["probability"]
                except:
                    transition_prob = 0.0000001  # If the transition wasn't in the training set then assign it very very low probability not 0.

                # print(transition_prob, np.log2(transition_prob))
                total_pp_value += np.log2(transition_prob)
                # print(total_pp_value)

            print("-------")
            print(total_pp_value)

            perplexity_score = -1 * total_pp_value / len(test_procedure_list)
            print(total_pp_value, perplexity_score)

            perplexity.append(perplexity_score)
            file_name.append(item)
            # break

    for i in range(0, len(file_name)):
        print(file_name[i], perplexity[i])

    print(perplexity_score)

    return(file_name, perplexity)

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
        df_transition = pd.read_csv(idir + t_regex + item1 + ".csv", index_col=False)
        print(df_transition)

        df_transition["current_state_clean"] = df_transition.apply(clean_curr_state,axis=1)
        df_transition["next_state_clean"] = df_transition.apply(clean_next_state,axis=1)

        # Now read the command sequence (the leave one out sample)
        df_cmd = pd.read_csv(idir + item1 + ifile_ext, index_col=False, header=0)
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

def get_anon_GT(row):
    for item in file_index_anon:
        if item == row["File_Name"]:
            return("Anomalous")
    return("Non-Anomalous")

joystick_list = ["20211018130924-1",  # 0
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
               "20211019145355-1"]

as_list= ["20211012145802-1",
           "20211012150440-1",
           "20211012132024-1",
           "20211012143509-1",
           "20211013110848-1"]

as_ur3_list = ["20211013113911-1",  # A
               "20211015125921-1",
               "20211013115553-1",
               "20211015132125-1"]

csp_list = ["20211020125006-1",
           "20211020130134-1", # A
           "20211022151947-1",
           "20211022152644-1"]

def get_type(row):
    if row["File_Name"] in joystick_list:
        return("P4")
    elif row["File_Name"] in as_list:
        return("P1")
    elif row["File_Name"] in as_ur3_list:
        return("P2")
    else:
        return("P3")

def main():
    ## Compute the transition probability matrix for each file using a leave-one-out method
    fname, perplexity_score = compute_transition_prob()
    print(perplexity_score)

    #perplexity_score = [1.1115205294028037, 0.8989529841568795, 0.6760381720572242, 0.8270756881686195, 0.812460576004786, 0.61835329579532, 1.421211149856776, 0.8938517820962318, 0.6278822191705873, 0.8145995050445625, 0.6969933801768224, 0.6186205267537022, 1.0807032580673483, 1.6697602861505494, 1.182306691474293, 1.4423023938697614, 1.642970991660042, 1.6223093599628327, 1.3139557349365982, 1.4460432836466663, 1.4123127413488494, 1.4689743188405198, 1.677376594224576, 1.446511311099156, 1.26097023775061]
    e_pp = []
    for i in range(0, len(perplexity_score)):
        print(np.exp(perplexity_score[i]))
        e_pp.append(np.exp(perplexity_score[i]))

    # Now, arrange it as needed
    fname_new=[]
    e_pp_new = []
    for item in file_index2:
        index = fname.index(item)
        fname_new.append(fname[index])
        e_pp_new.append(e_pp[index])

    for i, j in zip(fname_new, e_pp_new):
        print(i,j)

    # Scatter Plot of e_pp
    #Proc = [["Joystick"]*12, ["AS"]*5, ["AS_UR3"]*4, ["CSP"]*4]
    #Proc = [["P4"] * 12, ["P1"] * 5, ["P2"] * 4, ["P3"] * 4]
    #Proc_list = [item for sublist in Proc for item in sublist]

    df= pd.DataFrame({"File_Name":fname_new, "Value":e_pp_new, "ID": np.arange(0,25)})
    df["GT_Anomaly"] = df.apply(get_anon_GT, axis=1)
    df["Procedure"] = df.apply(get_type, axis=1)

    sns.scatterplot(data=df, x="ID", y="Value", hue="Procedure", style="GT_Anomaly")
    plt.xlabel("Procedure ID", fontsize=18)
    plt.ylabel("Perplexity Score", fontsize=18)
    plt.tight_layout()
    plt.savefig("./perplexity_score_5FCV.pdf")
    plt.show()

    #sns.scatterplot(data=df, x="ID", y="Value", hue="Procedure", style="Anomaly")
    sns.boxplot(x="Procedure", y="Value", hue="GT_Anomaly", data=df)
    plt.xlabel("Procedure Type")
    plt.ylabel("Perplexity Score")
    plt.tight_layout()
    plt.savefig("./perplexity_score_boxplot_5FCV.pdf")
    plt.show()


    # sns.scatterplot(data=df, x="ID", y="Value", hue="Procedure", style="Anomaly")
    #plt.figure(figsize=(5, 2))
    sns.boxplot(x="Procedure", y="Value", data=df)
    plt.xlabel("Procedure Type", fontsize=15)
    plt.ylabel("Perplexity Score", fontsize=15)
    plt.ylim(0,6)
    plt.tight_layout()
    plt.savefig("./perplexity_score_boxplot_nohue_5FCV.pdf")
    plt.show()

    # Computing natural break
    df.sort_values(by='Value')

    df['quantile'] = pd.qcut(df['Value'], q=2, labels=['Non-Anomalous', 'Anomalous'])
    print(df)

    df['cut_bins'] = pd.cut(df['Value'],
                            bins=2,
                            labels=['Non-Anomalous', 'Anomalous'])

    breaks2 = jenkspy.jenks_breaks(df['Value'], nb_class=2)
    breaks3 = jenkspy.jenks_breaks(df['Value'], nb_class=3)
    print(breaks2)
    print(breaks3)

    df['cut_jenks2'] = pd.cut(df['Value'],
                             bins=breaks2,
                             labels=['Non-Anomalous', "Anomalous"],
                             include_lowest=True)

    df['cut_jenks3'] = pd.cut(df['Value'],
                             bins=breaks3,
                             labels=['Non-Anomalous', "Something", "Anomalous"],
                             include_lowest=True)

    print(df)

    # Precision, Recall, F1
    ground_truth_label = df["GT_Anomaly"].to_list()
    jenks2 = df["cut_jenks2"].to_list()

    correct = 0
    incorrect = 0
    false_positives = 0
    false_negatives = 0
    true_positives = 0
    true_negatives = 0

    for i in range(0, len(ground_truth_label)):
        if ground_truth_label[i] == jenks2[i]:
            correct += 1
            if ground_truth_label[i] == "Non-Anomalous":
                print("True Negatives", ground_truth_label[i], jenks2[i])
                true_negatives += 1
            else:
                print("True Positives", ground_truth_label[i], jenks2[i])
                true_positives += 1
        else:
            incorrect += 1
            if ground_truth_label[i] == "Non-Anomalous":
                print("False Positive", ground_truth_label[i], jenks2[i])
                false_positives += 1
            else:
                print("False Negative", ground_truth_label[i], jenks2[i])
                false_negatives += 1

    print(true_positives, false_negatives)
    print(false_positives, true_negatives)

    Precision = true_positives/(true_positives + false_positives)
    Recall = true_positives/(true_positives + false_negatives)  #Sensitivity
    true_negative_rate = true_negatives/(true_negatives + false_positives) #Specificity

    Accuracy = (true_positives + true_negatives)/(true_positives + true_negatives + false_positives + false_negatives)

    F1 = 2*(Precision*Recall)/(Precision + Recall)

    # Accuracy, Weighted Accuracy
    Weighted_Accuracy2 = (2*true_positives + true_negatives)/(2*true_positives + true_negatives + false_positives + false_negatives)
    Weighted_Accuracy25 = (2.5*true_positives + true_negatives)/(2.5*true_positives + true_negatives + false_positives + false_negatives)

    print("**********************************************\n")
    print("Precision :", Precision)
    print("Recall :", Recall)
    print("F1 :", F1)
    print("Accuracy :", Accuracy)
    print("Weighted Accuracy :", Weighted_Accuracy2, Weighted_Accuracy25)
    print("True Negative Rate :", true_negative_rate)
    print("**********************************************\n")

if __name__ == "__main__":
    main()


"""
3 0
9 13
**********************************************

Precision : 0.25
Recall : 1.0
F1 : 0.4
Accuracy : 0.64
Weighted Accuracy : 0.6785714285714286 0.6949152542372882
True Negative Rate : 0.5909090909090909
**********************************************
"""