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
    '--ifile',
    default='./concat_all.csv',
    help='Input file path where the merged data is currently stored. Default is "./concat_all.csv".',
    type=str)
args = parser.parse_args()

def change_width(ax, new_value):
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

def get_name(row):
    #N9, UR3e, IKA, Centrifuge, Tecan, and Quantos
    if row["Module"] == "ArduinoAugmentedQuantos":
        return("Quantos")
    elif row["Module"] == "Tecan Cavro":
        return("Tecan")
    elif row["Module"] == "Magnetic Stirrer":
        return("IKA")
    elif row["Module"] == "C9":
        return("C9")
    else:
        return("UR3Arm")


# Q1,2. Module and Method_Name frequency
def module_freq():
    df = pd.read_csv(args.ifile, index_col=False)
    print(list(df))
    print(len(df.index))
    df_new = df[df["Module"]!= '-1']
    print(len(df_new.index))
    # ['Timestamp', 'Module', 'Method_Name', 'Arguments', 'Responses', 'Exceptions']

    print("*************************************************************")
    print("Dataset Summary")
    print("*************************************************************")
    print(">>>> Total commands in the dataset: ", len(df_new.index))
    print(">>>> Total unique Modules in the dataset: ", df_new["Module"].nunique())
    print(">>>>      Modules names: ", df_new["Module"].unique())
    print(">>>> Total unique commands in the dataset: ", df_new["Method_Name"].nunique())
    print("*************************************************************")

    print(df.groupby(['Module']).size())
    print(df.describe())
    print(df_new.groupby(['Module']).size())
    g2 = df_new.groupby(['Module']).size().reset_index(name='count')
    g2["Percentage"] = (g2['count'] / g2['count'].sum()) * 100
    print(g2)

    fig, ax = plt.subplots()
    df_new["Abbr_Module"]=df_new.apply(get_name,axis=1)
    #plt.rcParams["figure.figsize"] = (10, 3)
    sns.histplot(data=df_new, ax=ax, x="Abbr_Module")
    change_width(ax, .35)
    plt.yscale("log")
    plt.xlabel("Module Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("./module_histogram.pdf")
    # # # # # plt.show()
    plt.clf()

    fig, ax = plt.subplots()
    df_new["Abbr_Module"]=df_new.apply(get_name,axis=1)
    #plt.rcParams["figure.figsize"] = (10, 3)
    sns.histplot(data=df_new, ax=ax, x="Abbr_Module")
    change_width(ax, .35)
    plt.yscale("log")
    plt.xlabel("Module Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("./module_histogram_log.pdf")
    # # # # plt.show()
    plt.clf()

    plt.rcParams["figure.figsize"] = (390, 120)
    sns.histplot(data=df_new, x="Method_Name", hue="Module", multiple="stack")
    plt.xticks(rotation=45)
    plt.xlabel("Method Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.tight_layout()
    plt.savefig("./method_name_histogram.pdf")
    # # # # plt.show()
    plt.clf()

    print(df_new.groupby(['Method_Name', 'Abbr_Module']).size())
    g1 = df_new.groupby(['Method_Name', 'Abbr_Module']).size().reset_index(name='count')
    g1["Percentage"] = (g1['count'] / g1['count'].sum()) * 100
    g1['log_count'] = np.log(1 + g1['count'])
    print(g1['log_count'].tolist())
    print(g1['count'].tolist())
    print(g1)

    # sns.barplot(x="Method_Name", y="count", data=g1, hue="Abbr_Module")
    # #plt.ylim(0, 100000)
    # plt.yscale("log")
    # plt.xlabel("Method Name", fontsize = 20)
    # plt.ylabel("Log Count", fontsize=20)
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.savefig("./method_name_reduced_loghistogram.pdf")
    # # # # # plt.show()
    # plt.clf()

    # g1_noinit=g1[g1["Method_Name"] != "_init_"]
    # sns.barplot(x="Method_Name", y="count", data=g1_noinit, hue="Abbr_Module")
    # #plt.ylim(0, 100000)
    # plt.yscale("log")
    # plt.xlabel("Method Name", fontsize = 20)
    # plt.ylabel("Count", fontsize=20)
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.savefig("./method_name_reduced_loghistogram_noinit.pdf")
    # # # # # plt.show()
    # plt.clf()

    df_new_noinit = df_new[df_new["Method_Name"] != "_init_"]
    df_new_noinit.sort_values("Module",inplace=True)
    plt.figure(figsize=(12,6))
    # sns.color_palette("deep")
    # sns.set_theme(style="darkgrid")
    g=sns.histplot(data=df_new_noinit, x="Method_Name", hue="Abbr_Module")
    g.set_ylim((0.1, 1000000))
    g.set_axisbelow(True)
    plt.grid(True, which='both', linestyle='dashed', axis='y')
    plt.margins(x=0)
    plt.xticks(rotation=90, fontsize=14)
    plt.yscale("log")
    # plt.xlabel("Command Type", fontsize = 15)
    g.set_xlabel(None)
    plt.ylabel("Count", fontsize=15)
    labels=[ \
        "UR3Arm (" + str(df_new.groupby(['Module']).size()[4]) + ")", \
        "Tecan (" + str(df_new.groupby(['Module']).size()[3]) + ")", \
        "IKA (" + str(df_new.groupby(['Module']).size()[1]) + ")", \
        "C9 (" + str(df_new.groupby(['Module']).size()[2]) + ")", \
        "Quantos (" + str(df_new.groupby(['Module']).size()[0]) + ")" ]
    plt.legend(fontsize=14, loc='upper right', ncol=3, labels=labels)
    g.legend_.set_title(None)
    plt.tight_layout()
    plt.savefig("./method_name_loghistogram_hue_noinit.pdf")
    # # # # plt.show()
    plt.clf()

    # sns.histplot(data=df_new, x="Method_Name", hue="Module")
    # g=sns.histplot(data=df_new_noinit, x="Method_Name", hue="Abbr_Module")
    # plt.xticks(rotation=90)
    # plt.yscale("log")
    # plt.xlabel("Method Name", fontsize = 20)
    # plt.ylabel("Count", fontsize=20)
    # g.legend_.set_title(None)
    # plt.tight_layout()
    # plt.savefig("./method_name_loghistogram_hue.pdf")
    # # # # # plt.show()
    # plt.clf()

    # g1_new = g1[g1["Percentage"] > 1]
    # sns.barplot(x="Method_Name", y="count", data=g1_new)
    # plt.xlabel("Method Name", fontsize = 20)
    # plt.ylabel("Count", fontsize=20)
    # plt.tight_layout()
    # plt.savefig("./method_name_reduced_histogram.pdf")
    # # # # # plt.show()
    # plt.clf()

    method_list = df_new["Method_Name"].unique()
    for method in method_list:
        df_method = df_new[df_new["Method_Name"] == method]
        print(df_method.head(10))
        print("-------")
        #sns.pairplot(df_method)
        # # # # plt.show()

    df_new['Group_row_id'] = df_new.groupby(['Module']).cumcount() + 1
    group_df = df_new.groupby(["Module"])
    for name, group in group_df:
        #print(group, group.size)

        sns.stripplot(data=group, x="Group_row_id", y="Method_Name", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestep (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Method Name", fontsize=15)
        plt.tight_layout()
        print(group["Module"].unique()[0])
        ofig = "./" + group["Module"].unique()[0] + "_method.pdf"
        print(ofig)
        plt.savefig(ofig)
        # # # # plt.show()
        plt.clf()

        sns.stripplot(data=group, x="Group_row_id", y="Responses", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestep (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Response", fontsize=15)
        plt.tight_layout()
        plt.savefig("./" + group["Module"].unique()[0] + "_response.pdf")
        # # # # plt.show()
        plt.clf()

        sns.stripplot(data=group, x="Group_row_id", y="Exceptions", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestamp (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Exceptions", fontsize=15)
        plt.tight_layout()
        plt.savefig("./" + group["Module"].unique()[0] + "_exception.pdf")
        # # # # plt.show()
        plt.clf()

        # sns.catplot(data=group, x="Arguments", y="Responses", col="Method_Name")
        # plt.tight_layout()
        # # # # # plt.show()

        # sns.catplot(data=group, x="Arguments", y="Exceptions", col="Method_Name")
        # plt.tight_layout()
        # # # # # plt.show()

        # sns.catplot(data=group, x="Group_row_id", y="Arguments", col="Method_Name", kind="strip")
        # plt.set_xticklabels(plt.get_xticks()[::100], rotation=45)
        # plt.xticks(np.arange(0,group.size,100), np.arange(0,group.size,100))
        # plt.tight_layout()
        # # # # # plt.show()

        # sns.catplot(data=group, x="Arguments", y="Responses", col="Method_Name", kind="strip")
        # plt.tight_layout()
        # # # # # plt.show()

        # sns.catplot(data=group, x="Arguments", y="Exceptions", col="Method_Name", kind="strip")
        # plt.tight_layout()
        # # # # # plt.show()

        print(">>> Next group <<<")

    """
        sns.catplot(data=group, x="Group_row_id", y="Method_Name", kind="strip")
        plt.tight_layout()
        # # # # plt.show()

        sns.catplot(data=group, x="Group_row_id", y="Responses", kind="strip")
        plt.tight_layout()
        # # # # plt.show()

        sns.catplot(data=group, x="Group_row_id", y="Exceptions", kind="strip")
        plt.tight_layout()
        # # # # plt.show()
    # Pairplot

    df_pair = df_new[['Method_Name', 'Arguments', 'Responses', 'Exceptions']]
    print(df_pair.head(10))
    sns.pairplot(df_pair, hue="Method_Name")
    # # # # plt.show()
    """

#def cmd_arg_plot():
#    # group by command and analyze the arguents


def main():
    # Q1,2. Module & Method_Name frequency
    module_freq() # APT: commented out coz analysis is done
    # Q5. Command arguments plots
    #cmd_arg_plot()

if __name__ == "__main__":
    main()