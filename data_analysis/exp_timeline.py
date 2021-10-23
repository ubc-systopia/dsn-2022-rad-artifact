# Author: Amee Trivedi
# Objective: To plot each individual experiment timeline

# Imports
import pandas as pd
import numpy as np
import os
import seaborn as sns
from matplotlib import pyplot as plt


idir="/Users/amee/Desktop/Research/CPS/dataset/experiments/datasets/"
ifile_ext=".csv"

def main():
    file_list = os.listdir(idir)
    print(file_list)

    # Experiment,Timestamp,Module,Method_Name,Arguments,Responses,Exceptions,Anomaly (Yes/No)

    li = []
    for item in file_list:
        if item.startswith("2021"):
            df = pd.read_csv(idir + item, index_col=False, header = 0)
            num_list = range(0, len(df.index))

            df["Timeline"] = num_list
            print(list(df))

            sns.stripplot(data=df, x="Timeline", y="Method_Name", jitter=False)
            plt.title("%s \n %s" % (item, df["Module"].unique()))
            plt.xlabel("Time", fontsize=15)
            plt.ylabel("Method Name", fontsize=15)
            plt.tight_layout()
            plt.savefig("./" + item.split(".csv")[0] + ".pdf")
            plt.clf()
            #plt.show()

if __name__ == "__main__":
    main()