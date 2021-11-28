#Imports
import pandas as pd
import os
import glob
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
parser.add_argument(
    '-O',
    '--ofile',
    default='./concat_all.csv',
    help='Output file path where the merged data will be stored. Default is "./concat_all.csv".',
    type=str)
args = parser.parse_args()

def main():
    file_list = os.listdir(args.idir)
    print(file_list)

    # Experiment,Timestamp,Module,Method_Name,Arguments,Responses,Exceptions,Anomaly (Yes/No)

    li = []
    for item in file_list:
        print(item)
        df = pd.read_csv(args.idir +   item, index_col=False, header = 0)
        if (len(df.index) > 1):
            print(item)
            print(list(df))
            df = df[['Timestamp', 'Module', 'Method_Name', 'Arguments', 'Responses', 'Exceptions']]
            # Add a row delimiter between individual experiment files
            #new_row = {'Experiment': -1, 'Timestamp': -1, 'Module': -1, 'Method_Name': -1, 'Arguments': -1, 'Responses': -1, 'Exceptions': -1, 'Anomaly (Yes/No)': -1}
            new_row = {'Timestamp': -1, 'Module': -1, 'Method_Name': -1, 'Arguments': -1,'Responses': -1, 'Exceptions': -1}
            df = df.append(new_row, ignore_index=True)
            li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    # ofile = args.idir + "concat_all.csv"
    print("ofile =", args.ofile)
    files_present = glob.glob(args.ofile)

    print("... %s" %args.ofile)
    if not files_present:
        frame.to_csv(args.ofile, index=False)
        print(args.ofile)
        print(list(frame))
    else:
        print('WARNING: This file already exists!')
        os.remove(args.ofile)
        print("New File saved: %s" %args.ofile)
        print(list(frame))

    """
    li = []
    for filename in file_list:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    """
    return 0


if __name__ == "__main__":
    main()