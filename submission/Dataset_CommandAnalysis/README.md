# Steps to Run
Step 1:
Download all datafiles named: experiment_2021XXX.zip in a folder

Step 2:
Unzip all the experiment_2021XXX.zip files into a datasets folder

Step 3:
- Update idir path (line#9 in merge_all.py, line#12 exp_timeline.py and line #12 in cmd_analysis.py) with the path to "datasets" folder
i.e. update the below line in merge_all.py, exp_timeline.py, and cmd_analysis.py file.
idir="/Users/amee/Desktop/Research/CPS/dataset/experiments/datasets/" with the output of pwd command when in shell terminal of the above step 2.

Step 4:
The first script to run should be merge_all.py file using the following command
python merge_all.py

(My Python version is : Python 3.7.4, it should work on python2 or python3)

Step 5:
To plot individual experiment timelines execute the script exp_timeline.py using the command
python exp_timeline.py

Step 6:
To plot command patterns within a module run the script cmd_analysis.py using the command
python cmd_analysis.py


# File Name Mapping to Procedures
The selected 25 procedural runs are mapped to the their respective file name.
* 20211012132024-1 --> Automated Solubility
* 20211012143509-1 --> Automated Solubility
* 20211012145802-1 --> Automated Solubility
* 20211012150440-1 --> Automated Solubility
* 20211013110848-1 --> Automated Solubility
* 20211013113911-1 --> Automated Solubility with UR3e
* 20211013115553-1 --> Automated Solubility with UR3e
* 20211015125921-1 --> Automated Solubility with UR3e
* 20211015132125-1 --> Automated Solubility with UR3e
* 20211018130924-1 --> Joystick
* 20211018132502-1 --> Joystick
* 20211018133320-1 --> Joystick
* 20211018135445-1 --> Joystick
* 20211018140458-1 --> Joystick
* 20211018141513-1 --> Joystick
* 20211019142004-1 --> Joystick
* 20211019142656-1 --> Joystick
* 20211019143332-1 --> Joystick
* 20211019144058-1 --> Joystick
* 20211019144749-1 --> Joystick
* 20211019145355-1 --> Joystick
* 20211020125006-1 --> Crystal Solubility Profiling
* 20211020130134-1 --> Crystal Solubility Profiling
* 20211022151947-1 --> Crystal Solubility Profiling
* 20211022152644-1 --> Crystal Solubility Profiling


