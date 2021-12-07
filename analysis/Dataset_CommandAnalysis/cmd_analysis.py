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

def get_command_label(row):
    if row["Method_Name"] == "Q":
        return("Q (get_status)")
    elif row["Method_Name"] == "P":
        return("P (set_distance)")
    elif row["Method_Name"] == "V":
        return("V (set_velocity)")
    elif row["Method_Name"] == "A":
        return("A (set_position)")
    elif row["Method_Name"] == "I":
        return("I (set_valve_position)")
    elif row["Method_Name"] == "G":
        return("G (stop_batch_command)")
    elif row["Method_Name"] == "g":
        return("g (start_batch_command)") 
    elif row["Method_Name"] == "k":
        return("k (set_dead_volume)")
    elif row["Method_Name"] == "L":
        return("L (set_slope_code)")
    elif row["Method_Name"] == "Z":
        return("Z (set_home_position)")

    elif row["Method_Name"] == "IN_SP_1":
        return("IN_SP_1 (read_rated_temperature)")
    elif row["Method_Name"] == "IN_SP_4":
        return("IN_SP_4 (read_rated_speed)")
    elif row["Method_Name"] == "IN_PV_4":
        return("IN_PV_4 (read_stirring_speed)")
    elif row["Method_Name"] == "IN_NAME":
        return("IN_NAME (read_device_name)")
    elif row["Method_Name"] == "IN_PV_1":
        return("IN_PV_1 (read_external_sensor)")
    elif row["Method_Name"] == "IN_PV_2":
        return("IN_PV_2 (read_hotplate_sensor)")
    elif row["Method_Name"] == "STOP_4":
        return("STOP_4 (stop_the_motor)")
    elif row["Method_Name"] == "STOP_1":
        return("STOP_1 (stop_the_heater)")
    elif row["Method_Name"] == "OUT_SP_4":
        return("OUT_SP_4 (set_speed)")
    elif row["Method_Name"] == "START_4":
        return("START_4 (start_the_motor)")
    elif row["Method_Name"] == "OUT_SP_1":
        return("OUT_SP_1 (set_temperature)")
    elif row["Method_Name"] == "START_1":
        return("START_1 (start_the_heater)")  

    elif row["Method_Name"] == "HOME":
        return("HOME (home_n9)")  
    elif row["Method_Name"] == "CURR":
        return("CURR (get_axis_current)")  
    elif row["Method_Name"] == "MVNG":
        return("MVNG (get_axes_moving_states)")  
    elif row["Method_Name"] == "SPED":
        return("SPED (get_speed)")  
    elif row["Method_Name"] == "ARM":
        return("ARM (move_arm)")  
    elif row["Method_Name"] == "BIAS":
        return("BIAS (set_elbow_bias)")  
    elif row["Method_Name"] == "OUTP":
        return("OUTP (toggle_centrifuge)")  
    elif row["Method_Name"] == "JLEN":
        return("JLEN (set_elbow_length)") 
    elif row["Method_Name"] == "PING":
        return("PING (ping)")  
    elif row["Method_Name"] == "POS":
        return("POS (get_position)")  
    elif row["Method_Name"] == "MOVE":
        return("MOVE (move_axis)")  

    elif row["Method_Name"] =="zero":
        return("zero (zero_balance_reading)") 
    elif row["Method_Name"] == "_init_":
        if row["Module"] == "Magnetic Stirrer":
            return("_init_ (IKA)")
        elif row["Module"] == "UR3Arm":
            return("_init_ (UR3Arm)")
        elif row["Module"] == "C9":
            return("_init_ (C9)")
        elif row["Module"] == "Tecan Cavro":
            return("_init_ (Tecan)")
        elif row["Module"] == "ArduinoAugmentedQuantos":
            return("_init_ (Quantos)")
    else:
        return(row["Method_Name"])
    



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
    plt.clf()

    fig, ax = plt.subplots()
    df_new["Abbr_Module"]=df_new.apply(get_name,axis=1)
    df_new["x_labels"]=df_new.apply(get_command_label,axis=1)
    #plt.rcParams["figure.figsize"] = (10, 3)
    sns.histplot(data=df_new, ax=ax, x="Abbr_Module")
    change_width(ax, .35)
    plt.yscale("log")
    plt.xlabel("Module Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("./module_histogram_log.pdf")
    plt.clf()

    #plt.rcParams["figure.figsize"] = (390, 120)
    sns.histplot(data=df_new, x="Method_Name", hue="Module", multiple="stack")
    plt.xticks(rotation=45)
    plt.xlabel("Method_Name", fontsize = 20)
    plt.ylabel("Count", fontsize=20)
    plt.tight_layout()
    plt.savefig("./method_name_histogram.pdf")
    plt.clf()

    print(df_new.groupby(['Method_Name', 'Abbr_Module']).size())
    g1 = df_new.groupby(['Method_Name', 'Abbr_Module']).size().reset_index(name='count')
    g1["Percentage"] = (g1['count'] / g1['count'].sum()) * 100
    g1['log_count'] = np.log(1 + g1['count'])
    print(g1['log_count'].tolist())
    print(g1['count'].tolist())
    print(g1)

    plt.rcParams["figure.figsize"] = (390, 150)
    df_new_noinit = df_new[df_new["Method_Name"] != "_init_"]
    
    df_new.sort_values("Module",ascending=False, inplace=True)
    plt.figure(figsize=(12,6))
    # sns.color_palette("deep")
    # sns.set_theme(style="darkgrid")
    print(df_new)
    g=sns.histplot(data=df_new, x="x_labels", hue="Abbr_Module")
    g.set_ylim((0.1, 1000000))
    g.set_axisbelow(True)
    plt.grid(True, which='major', linestyle='dashed', axis='y')
    plt.margins(x=0)
    plt.xticks(rotation=90, fontsize=13)
    plt.yscale("log")
    # plt.xlabel("Command Type", fontsize = 14)
    g.set_xlabel(None)
    plt.ylabel("Count", fontsize=15)
    plt.legend(fontsize=13, loc='upper left', ncol=3, labels=["Quantos (" + str(df_new.groupby(['Module']).size()[0]) + ")",  "C9 (" + str(df_new.groupby(['Module']).size()[1]) + ")", "IKA (" + str(df_new.groupby(['Module']).size()[2]) + ")", "Tecan (" + str(df_new.groupby(['Module']).size()[3]) + ")", "UR3Arm (" + str(df_new.groupby(['Module']).size()[4]) + ")"])
    g.legend_.set_title(None)
    plt.tight_layout()
    plt.savefig("./method_name_loghistogram_hue_noinit.pdf")
    plt.show()
    plt.clf()

    method_list = df_new["Method_Name"].unique()
    for method in method_list:
        df_method = df_new[df_new["Method_Name"] == method]
        print(df_method.head(10))
        print("-------")

    df_new['Group_row_id'] = df_new.groupby(['Module']).cumcount() + 1
    group_df = df_new.groupby(["Module"])
    for name, group in group_df:
        #print(group, group.size)

        sns.stripplot(data=group, x="Group_row_id", y="Method_Name", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestep (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Method_Name", fontsize=15)
        plt.tight_layout()
        print(group["Module"].unique()[0])
        ofig = "./" + group["Module"].unique()[0] + "_method.pdf"
        print(ofig)
        plt.savefig(ofig)
        plt.clf()

        sns.stripplot(data=group, x="Group_row_id", y="Responses", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestep (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Response", fontsize=15)
        plt.tight_layout()
        plt.savefig("./" + group["Module"].unique()[0] + "_response.pdf")
        plt.clf()

        sns.stripplot(data=group, x="Group_row_id", y="Exceptions", jitter=False)
        plt.title("%s Module Patterns" % group["Module"].unique())
        plt.xlabel("Timestamp (Intra-Module Command Timeline)", fontsize=15)
        plt.ylabel("Exceptions", fontsize=15)
        plt.tight_layout()
        plt.savefig("./" + group["Module"].unique()[0] + "_exception.pdf")
        plt.clf()


        print(">>> Next group <<<")


def main():
    # Q1,2. Module & Method_Name frequency
    module_freq() 
    # Q5. Command arguments plots
    #cmd_arg_plot()

if __name__ == "__main__":
    main()
