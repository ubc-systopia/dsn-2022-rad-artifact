# Author: Amee Trivedi
# Objective: Command and Module usage Analysis script

#Imports
import pandas as pd
import os
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


idir = "/Users/amee/Desktop/Research/CPS/dataset/experiments/datasets/"
ifile = "concat_all.csv"


# Q1,2. Module and Method_Name frequency
def module_freq():
    df = pd.read_csv(idir + ifile, index_col=False)
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


    sns.histplot(data=df_new, x="Module")
    plt.xlabel("Module Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.tight_layout()
    plt.savefig("./module_histogram.pdf")
    plt.show()
    plt.clf()

    sns.histplot(data=df_new, x="Method_Name", hue="Module", multiple="stack")
    plt.xticks(rotation=45)
    plt.xlabel("Method Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.tight_layout()
    plt.savefig("./method_name_histogram.pdf")
    plt.show()
    plt.clf()


    method_list = df_new["Method_Name"].unique()
    for method in method_list:
        df_method = df_new[df_new["Method_Name"] == method]
        print(df_method.head(10))
        print("-------")
        #sns.pairplot(df_method)
        #plt.show()

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
        plt.show()

        sns.stripplot(data=group, x="Group_row_id", y="Responses", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestep (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Response", fontsize=15)
        plt.tight_layout()
        plt.savefig("./" + group["Module"].unique()[0] + "_response.pdf")
        plt.show()

        sns.stripplot(data=group, x="Group_row_id", y="Exceptions", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestamp (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Exceptions", fontsize=15)
        plt.tight_layout()
        plt.savefig("./" + group["Module"].unique()[0] + "_exception.pdf")
        plt.show()

        #sns.catplot(data=group, x="Arguments", y="Responses", col="Method_Name")
        #plt.tight_layout()
        #plt.show()

        #sns.catplot(data=group, x="Arguments", y="Exceptions", col="Method_Name")
        #plt.tight_layout()
        #plt.show()

        #sns.catplot(data=group, x="Group_row_id", y="Arguments", col="Method_Name", kind="strip")
        #plt.set_xticklabels(plt.get_xticks()[::100], rotation=45)
        #plt.xticks(np.arange(0,group.size,100), np.arange(0,group.size,100))
        #plt.tight_layout()
        #plt.show()

        #sns.catplot(data=group, x="Arguments", y="Responses", col="Method_Name", kind="strip")
        #plt.tight_layout()
        #plt.show()

        #sns.catplot(data=group, x="Arguments", y="Exceptions", col="Method_Name", kind="strip")
        #plt.tight_layout()
        #plt.show()

        print(">>> Next group <<<")

    """
        sns.catplot(data=group, x="Group_row_id", y="Method_Name", kind="strip")
        plt.tight_layout()
        plt.show()

        sns.catplot(data=group, x="Group_row_id", y="Responses", kind="strip")
        plt.tight_layout()
        plt.show()

        sns.catplot(data=group, x="Group_row_id", y="Exceptions", kind="strip")
        plt.tight_layout()
        plt.show()
    # Pairplot

    df_pair = df_new[['Method_Name', 'Arguments', 'Responses', 'Exceptions']]
    print(df_pair.head(10))
    sns.pairplot(df_pair, hue="Method_Name")
    plt.show()
    """

def main():
    # Q1,2. Module & Method_Name frequency
    module_freq()

if __name__ == "__main__":
    main()