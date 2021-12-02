# RosyChem Lab

This project was created in collaboration with RosyChem Lab, a research lab that uses Cyber Physical Systems (CPS) to automate chemical synthesis procedures, to bridge the gap of providing dataset for developing Intrusion Detection Systems (IDS) to secure the CPS in smart manufacturing. Towards this end, we provide the Robotic Arm Dataset (RAD) along with non-intrusive tracing framework, RATracer. Additionally, we also provide preliminary analyses on the command and power data in RAD. 

This README file provides the directory structure of this project, documentation on the supervised experiment steps carried out to create RAD, the description of RAD and running the UR Robot Simulator. Further, it describes the steps required to set up, build and run the RATracer along with the steps on running the analysis scripts for command and power data.

## Resources

### Directory Structure

* [`analysis`](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis) contains the scripts, graphs and documentation for reproducing the analysis on command and power data. It also provides the scripts and documentation on performing the analysis to evaluate the performance of RATracer.

* [`dataset`](https://github.com/ubc-systopia/cps-security-code/tree/main/dataset) contains RAD that is stored in the form of .csv files where the supervised experiments are labeled as anamolous or benign and the rest are labeled as unknown procedures. It also contains the MongoDB instance for storing RAD.

* [`docs`](https://github.com/ubc-systopia/cps-security-code/tree/main/docs) contains additional docs that contains the description of the RAD along with the details of the supervised experiments and their steps. Further, they contain steps to install UR simulator and running it via Python script.

* [`tracer`](https://github.com/ubc-systopia/cps-security-code/tree/main/tracer) contains the  non-intrusive tracing framework, RATracer that uses the middlebox to collect the trace data and send commands to the modules.

### Getting Started

##### Collecting Command\Response Data
* [Building and Testing RATracer - Command Data](https://github.com/ubc-systopia/cps-security-code/blob/main/tracer/README.md)
* [Processing Tracing Files](https://github.com/ubc-systopia/cps-security-code/blob/main/tracer/data_processing/README.md)
* [Running Command Analysis](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis/Dataset_CommandAnalysis)

##### Collecting Power Monitoring Data
* [Building and Testing RATracer - Power Monitoring Data (Add Readme file)]
* [Running Power Analysis](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis/Dataset_PowerAnalysis)


### Robotic Arm Dataset (RAD) and Description
* [Robotic Arm Dataset](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/RAD_Description.pdf)
* [RAD Description](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/RAD_Description.pdf)
* [Experiment Steps](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/Experiment_Steps.pdf)


### Additional Documents

* [Building and Running UR Robot Simulator](https://github.com/ubc-systopia/cps-security-code/blob/main/docs/URsim_Setup.pdf)


# Contacts

#### Mailing List

#### People


#### Organization

University of British Columbia







