#Imports
import pandas as pd
import os
import glob

idir="<dataset_location_path_name>"
ifile_ext=".csv"

def main():
    file_list = os.listdir(idir)
    print(file_list)

    # Experiment,Timestamp,Module,Method_Name,Arguments,Responses,Exceptions,Anomaly (Yes/No)

    li = []
    for item in file_list:
        print(item)
        df = pd.read_csv(idir + item, index_col=False, header = 0)
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

    ofile = idir + "concat_all.csv"
    files_present = glob.glob(ofile)

    print("... %s" %ofile)
    if not files_present:
        frame.to_csv(ofile, index=False)
        print(ofile)
        print(list(frame))
    else:
        print('WARNING: This file already exists!')
        os.remove(ofile)
        print("New File saved: %s" %ofile)
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