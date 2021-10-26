# Usage: python perf_analysis.py --source "../csv/" --target "./perf_analysis_results/"
# Inputs: CSV files
# Outputs: For each CSV file, an output file 

import os
import pandas
import seaborn
import argparse

from datetime import datetime

from matplotlib import pyplot

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
    print("Plotting response times")

    dfs = []
    for source_file in source_files:
        print("Parsing", source_file)

        col_names=['id','ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec', 'arrival_time', 'departure_time']
        df = pandas.read_csv(args.source + source_file, index_col=False, header = 0, names=col_names)
        df.drop(labels=['ts', 'arguments', 'responses', 'exceptions'], axis='columns', inplace=True)
        df.drop(df[df.method != 'ARM'].index, axis='rows', inplace=True)
        
        df['resp_time_ms'] = df.apply(lambda row : compute_response_time(row['arrival_time'], row['departure_time']), axis='columns')
        df['exe_time_ms'] = df.apply(lambda row : row['exe_time_sec'] * 1000, axis='columns')

        df = pandas.DataFrame(df['resp_time_ms'])
        df['source'] = source_file

        dfs.append(df)
    
    cdf = pandas.concat(dfs)
    mdf = pandas.melt(cdf, id_vars=['source'])

    ax = seaborn.boxplot(x='source', y='value', hue='variable', data=mdf)
    ax.set_ylim((0, cdf['resp_time_ms'].max()))
    pyplot.xlabel("Scenario")
    pyplot.ylabel("Response Time (ms)")
    # pyplot.show()
    plotfile = args.target + "RESPONSE-TIMES.pdf"
    pyplot.savefig(plotfile)
    print("Saving results at", plotfile)
    pyplot.clf()

def plot_durations(source_files):
    print("Plotting absolute durations")

    for source_file in source_files:
        print("Parsing", source_file)

        col_names=['id','ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec', 'arrival_time', 'departure_time']
        df = pandas.read_csv(args.source + source_file, index_col=False, header = 0, names=col_names)
        df.drop(labels=['ts', 'module', 'method', 'arguments', 'responses', 'exceptions', 'exe_time_sec'], axis='columns', inplace=True)
        first_arrival_time = df.iloc[0]['arrival_time']
        df['relative_arrival_time'] = df.apply(lambda row : compute_response_time(first_arrival_time, row['arrival_time']), axis='columns')
        df['relative_departure_time'] = df.apply(lambda row : compute_response_time(first_arrival_time, row['departure_time']), axis='columns')
    
        # print()
        # print(df)

        for index, row in df.iterrows():
            x = [row['relative_arrival_time'], row['relative_departure_time']]
            y = [row['id'], row['id']]
            ax = seaborn.lineplot(x=x, y=y)
        
        pyplot.xlabel("Time (ms)")
        pyplot.ylabel("Request ID")
        # pyplot.show()
        plotfile = args.target + source_file.split(".csv")[0] + "-durations.pdf"
        pyplot.savefig(plotfile)
        print("Saving results at", plotfile)
        pyplot.clf()


if __name__ == "__main__":
    source_files = os.listdir(args.source)
    plot_resp_times(source_files)
    plot_durations(source_files)