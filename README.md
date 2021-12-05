# RosyChem Lab

This project was created in collaboration with RosyChem Lab, a research lab that uses Cyber Physical Systems (CPS) to automate chemical synthesis procedures. Our goal is to collect real-world CPU data from which we and others can develop Intrusion Detection Systems (IDS) to secure the CPS in smart laboratories and manufacturing floors. This repository includes the Robotic Arm Dataset (RAD) along with a non-intrusive tracing framework, RATracer. Additionally, we include scripts and results from preliminary analyses using command and power data.

This README file documents the directory structure of this project, documentation on the supervised experiment steps carried out to create RAD, the description of RAD and running the UR Robot Simulator. Further, it describes the steps required to set up, build and run the RATracer along with the steps on running the analysis scripts for command and power data.

## Resources

### Directory Structure

* [`analysis`](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis) contains the scripts, graphs and documentation for reproducing the analysis on command and power data. It also provides the scripts and documentation on performing the analysis to evaluate the performance of RATracer.

* [`dataset`](https://github.com/ubc-systopia/cps-security-code/tree/main/dataset) contains RAD that is stored in the form of .csv files where the supervised experiments are labeled as anamolous or benign and the rest are labeled as unknown procedures. It also contains the MongoDB instance for storing RAD.

* [`docs`](https://github.com/ubc-systopia/cps-security-code/tree/main/docs) contains additional docs that contains the description of the RAD along with the details of the supervised experiments and their steps. Further, they contain steps to install UR simulator and running it via Python script.

* [`tracer`](https://github.com/ubc-systopia/cps-security-code/tree/main/tracer) contains the  non-intrusive tracing framework, RATracer that uses the middlebox to collect the command and power trace data and send commands to the modules.

### Getting Started

##### Collecting Command Data
* [Building and Testing RATracer - Command](https://github.com/ubc-systopia/cps-security-code/blob/main/tracer/README.md)
* [Processing Tracing Files](https://github.com/ubc-systopia/cps-security-code/blob/main/tracer/data_processing/README.md)
* [Running Command Analysis](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis/Dataset_CommandAnalysis)

##### Collecting Power Monitoring Data
* [Building and Testing RATracer - Power Monitoring](https://github.com/ubc-systopia/cps-security-code/blob/main/tracer/RATracer_power_monitoring/README.md)
* [Running Power Analysis](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis/Dataset_PowerAnalysis)


### Robotic Arm Dataset (RAD)
* [Robotic Arm Dataset](https://github.com/ubc-systopia/cps-security-code/tree/main/dataset)
* [Features Description](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/RAD_Description.pdf)
* [Experiment Steps](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/Experiment_Steps.pdf)
* [Labeled Tracing Files Description](https://github.com/ubc-systopia/cps-security-code/blob/main/dataset/README.md)


### Additional Documents

* [Building and Running UR Robot Simulator](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/URsim_Setup.pdf)


# Contacts

#### Mailing List

#### People


#### Organization

University of British Columbia







