# RosyChem Lab

This project was created in collaboration with RosyChem Lab, a research lab that uses Cyber Physical Systems (CPS) to automate chemical synthesis procedures. Our goal is to collect real-world CPU data from which we and others can develop Intrusion Detection Systems (IDS) to secure the CPS in smart laboratories and manufacturing floors. This repository includes the Robotic Arm Dataset (RAD) along with a non-intrusive tracing framework, RATracer. Additionally, we include scripts and results from preliminary analyses using command and power data.

This README file documents the directory structure of this project, documentation on the supervised experiment steps carried out to create RAD, the description of RAD and running the UR Robot Simulator. Further, it describes the steps required to set up, build and run the RATracer along with the steps on running the analysis scripts for command and power data.

## Resources

### Directory Structure

* [`analysis`](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis): The scripts, graphs and documentation for reproducing our analysis of command and power data. It also contains the scripts and documentation for evaluating the performance of RATracer.

* [`dataset`](https://github.com/ubc-systopia/cps-security-code/tree/main/dataset): A collection of .csv files and a MongoDN instance. The MongoDB database contains all the original data; the .csv files are extractions from the database and contain labeled data for the supervised experiments as well as a collection of unknown procedures.

* [`docs`](https://github.com/ubc-systopia/cps-security-code/tree/main/docs): Additional documents that contains the description of the dataset along with the details of the supervised experiments and their steps. Also documents the steps to install the UR simulator and run it from Python.

* [`tracer`](https://github.com/ubc-systopia/cps-security-code/tree/main/tracer): The  non-intrusive tracing framework, RATracer, which uses a middlebox to collect command and power trace data before sending commands to the specific modules.

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







