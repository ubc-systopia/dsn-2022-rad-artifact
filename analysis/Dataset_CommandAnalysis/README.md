# Prepare the Dataset Folder for Command Analysis

## Step 1:
Download all csv datafiles from [RAD_Commands](../../dataset/RAD_Commands/csv.zip).

## Step 2:
Unzip the `csv.zip` folder. 

## Step 3:
From the `known_procedures` folder, copy all the csv files from the `anomaly` and `benign` folder in a separate folder that will have all the 25 files where this folder will be passed as `--idir` argument for most of the command analysis files. 


# Plotting Individual Experiments and Command Patterns

## Step 1:
The first script to run should be merge_all.py file using the following command:

 `python merge_all.py --idir <dataset folder> --ifile_ext <file extension (.csv)> --ofile <output concat file path>`
 
 ## Step 2:
To plot individual experiment timelines execute the script exp_timeline.py using the command:

`python exp_timeline.py --idir <dataset folder>`

## Step 3:
To plot command patterns within a module run the script cmd_analysis.py using the command:

`python cmd_analysis.py --ifile <concat file name>`

# N-Gram Analysis

# Step 1
To generate ngrams run the script ngram.py using the command:

`python ngram.py --idir <dataset folder> --ifile_ext <file extension (.csv)>`

It will store the ngrams in the csv file format in the dataset folder.

# Step 2
To plot the ngrams run the script ngram_analysis.py using the command:

`python ngram_analysis.py --idir <dataset folder containing the ngrams csv files>`

# TF-IDF

To perform TF-IDF analysis run the script ngram_tfidf.py uisng the command:

`python ngram_tfidf.py --idir <dataset folder> --ifile_ext <file extension (.csv)>`



## File Name Mapping to Procedure ID for TF-IDF
The selected 25 known procedural runs are mapped to the their respective procedure IDs that are used for TF-IDF.

| Procedure ID | File Name        |
|--------------|------------------|
| 0            | 20211018130924-1 |
| 1            | 20211018132502-1 |
| 2            | 20211018133320-1 |
| 3            | 20211018135445-1 |
| 4            | 20211018140458-1 |
| 5            | 20211018141513-1 |
| 6            | 20211019142004-1 |
| 7            | 20211019142656-1 |
| 8            | 20211019143332-1 |
| 9            | 20211019144058-1 |
| 10           | 20211019144749-1 |
| 11           | 20211019145355-1 |
| 12           | 20211012145802-1 |
| 13           | 20211012150440-1 |
| 14           | 20211012132024-1 |
| 15           | 20211012143509-1 |
| 16           | 20211013110848-1 |
| 17           | 20211013113911-1 |
| 18           | 20211015125921-1 |
| 19           | 20211013115553-1 |
| 20           | 20211015132125-1 |
| 21           | 20211020125006-1 |
| 22           | 20211020130134-1 |
| 23           | 20211022151947-1 |
| 24           | 20211022152644-1 |


# Perplexity Scores

* `python similarity_score.py --idir <dataset folder> --ifile_ext <file extension (.csv)>`
* `python order_1_MC_5_fold_CV.py --idir <dataset folder> --ifile_ext <file extension (.csv)>`
* `python order_2_MC_5_fold_CV.py --idir <dataset folder> --ifile_ext <file extension (.csv)>`
* `python order_3_MC_5_fold_CV.py --idir <dataset folder> --ifile_ext <file extension (.csv)>`

