# Usage: python perf_analysis.py --source "../csv/" --target "./perf_analysis_results/"
# Inputs: CSV files
# Outputs: For each CSV file, an output file 

import os
from numpy.lib.utils import source
import pandas
import seaborn
import argparse

from datetime import datetime

from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument(
    '-s',
    '--source',
    default='./',
    help='Directory path containing data files in .csv format.',
    type=str)
parser.add_argument(
    '-t',
    '--target',
    default='./',
    help='Directory path where the analysis resulys must be stored.',
    type=str)
args = parser.parse_args()

def compute_response_time(arrival_time_str, departure_time_str):
    datetime_format = '%Y:%m:%d:%H:%M:%S.%f'
    arrival_time = datetime.strptime(arrival_time_str, datetime_format)
    departure_time = datetime.strptime(departure_time_str, datetime_format)
    response_time = departure_time - arrival_time
    return response_time.total_seconds() * 1000

def plot_resp_times(source_files):
    commands = ['ARM', 'MVNG', 'ALL']
    for command in commands:
        print("Plotting response times for command", command)

        dfs = []
        for source_file in source_files:
            if 'SMALL' in source_file:
                continue
            print("Parsing", source_file)

            col_names=['id','ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec', 'arrival_time', 'departure_time']
            df = pandas.read_csv(args.source + source_file, index_col=False, header = 0, names=col_names)
            df.drop(labels=['ts', 'arguments', 'responses', 'exceptions'], axis='columns', inplace=True)
            if command != 'ALL':
                df.drop(df[df.method != command].index, axis='rows', inplace=True)
            
            df['resp_time_ms'] = df.apply(lambda row : compute_response_time(row['arrival_time'], row['departure_time']), axis='columns')
            df['exe_time_ms'] = df.apply(lambda row : row['exe_time_sec'] * 1000, axis='columns')

            df = pandas.DataFrame(df['resp_time_ms'])
            if 'LARGE' in source_file:
                df['source'] = 'MB-REMOTE-' + source_file.split('-')[0][-1]
            elif 'DIRECT' in source_file:
                df['source'] = 'DIRECT-' + source_file.split('-')[0][-1]
            else:
                df['source'] = 'MB-LOCAL-' + source_file.split('-')[0][-1]

            dfs.append(df)
        
        cdf = pandas.concat(dfs)
        mdf = pandas.melt(cdf, id_vars=['source'])
        mdf.sort_values('source', inplace=True)

        plt.figure(figsize=(6,3))
        ax = seaborn.boxplot(x='source', y='value', hue='variable', data=mdf)
        # ax.set_ylim((0, cdf['resp_time_ms'].max()))
        ax.set_ylim((0, 100))
        ax.get_legend().remove()
        ax.set(xlabel=None)
        plotfile = args.target + "RESPONSE-TIMES-FOR-" + command + ".pdf"
        # plt.xlabel("Scenarios (Focus: %s commands)" % command)
        plt.ylabel("Response Time (ms)")
        plt.xticks(rotation=90, fontsize=10)
        # plt.title(plotfile.split('/')[-1].split('.')[0])
        # plt.yscale('log')
        plt.grid(True, which='both')
        plt.tight_layout()
        # plt.show()
        plt.savefig(plotfile)
        print("Saving results at", plotfile)
        plt.clf()

def plot_durations(source_files):
    print("Plotting absolute durations")

    for exp_id in range(1, 7):
        print("Plotting for EXP%s" % exp_id)
        plt.figure(figsize=(6,3))
        labels = []
        for source_file in source_files:
            if exp_id != int(source_file.split('-')[0][-1]): continue
            if 'SMALL' in source_file: continue
            print("Parsing", source_file)

            col_names=['id','ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec', 'arrival_time', 'departure_time']
            df = pandas.read_csv(args.source + source_file, index_col=False, header = 0, names=col_names)
            # print(df)
            df.drop(labels=['ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec'], axis='columns', inplace=True)
            first_arrival_time = df.iloc[0]['arrival_time']
            df['relative_arrival_time'] = df.apply(lambda row : 0.001 * compute_response_time(first_arrival_time, row['arrival_time']), axis='columns')
            df['relative_departure_time'] = df.apply(lambda row : 0.001 * compute_response_time(first_arrival_time, row['departure_time']), axis='columns')
        
            # print()
            # print(df)

            # for index, row in df.iterrows():
            #     x = [row['relative_arrival_time'], row['relative_departure_time']]
            #     y = [row['id'], row['id']]
            #     ax = seaborn.lineplot(x=x, y=y)
            
            ax = seaborn.scatterplot(x='relative_arrival_time', y='id', data=df, linewidth=0)

            if 'LARGE' in source_file:
               labels.append('MB-REMOTE')
            elif 'DIRECT' in source_file:
               labels.append('DIRECT')
            else:
               labels.append('MB-LOCAL')

        plotfile = args.target + "EXP" + str(exp_id) + "-durations.pdf"
        plt.xlabel("Time (seconds)")
        plt.ylabel("Request ID")
        # plt.title("EXP" + str(exp_id))
        plt.legend(labels=labels)
        plt.tight_layout()
        plt.savefig(plotfile)
        print("Saving results at", plotfile)
        plt.clf()

def plot_arguments(source_files):
    print("Plotting arguments")
    argnames = ['acceleration', 'velocity', 'relative', 'x', 'y']

    dfs = {}
    for source_file in source_files:
        if 'LARGE' in source_file or 'SMALL' in source_file or 'DIRECT' in source_file: continue
        print("Parsing", source_file)

        exp_id = source_file.split('-')[0]

        col_names=['id','ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec', 'arrival_time', 'departure_time']
        df = pandas.read_csv(args.source + source_file, index_col=False, header = 0, names=col_names)
        df.drop(df[df.method != 'ARM'].index, axis='rows', inplace=True)
        df.drop(labels=['module', 'method', 'responses', 'exceptions', 'exe_time_sec', 'departure_time'], axis='columns', inplace=True)
        first_arrival_time = df.iloc[0]['arrival_time']
        df['relative_arrival_time'] = df.apply(lambda row : 0.001 * compute_response_time(first_arrival_time, row['arrival_time']), axis='columns')
        df[['velocity', 'acceleration', 'relative', 'x', 'y']] = df['arguments'].str.split(',', expand=True)
        
        for arg in argnames:
            df[['temp', arg]] = df[arg].str.split(':', expand=True)
            df.drop(labels=['temp'], axis='columns', inplace=True)
            df[arg] = df[arg].astype("float")
        
        dfs[exp_id] = df
    
        # print(df)

    for arg in argnames:
        plt.figure(figsize=(6,3))
        # print(df[arg].describe())
        plotfile = args.target + source_file.split(".csv")[0] + "-" + arg + ".pdf"
        for exp_id in dfs.keys():
            seaborn.scatterplot(x='relative_arrival_time', y=arg, data=dfs[exp_id], linewidth=0)
        # ax.set_ylim((0, df[arg].max()))
        plt.xlabel("Time (seconds)")
        plt.ylabel(arg.capitalize() + " (units)")
        plt.legend(labels=dfs.keys())
        # plt.title(plotfile)
        plt.tight_layout()
        # plt.show()
        plt.savefig(plotfile)
        print("Saving results at", plotfile)
        plt.clf()


if __name__ == "__main__":
    source_files = os.listdir(args.source)
    # plot_resp_times(source_files)
    plot_durations(source_files)
    # plot_arguments(source_files)