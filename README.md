# Arming IDS Researchers with a Robotic Arm Dataset (DSN 2022)

#### This is an ongoing project to design and develop intrusion detection systems (IDS) for the Hein Lab, a smart manufacturing research lab in the chemical sciences domain. 

### Overview
Designing effective IDS requires large datasets and high-quality, domain-specific benchmarks, which are difficult to obtain. To address this gap, we present the Robotic Arm Dataset (RAD), which we collected at the Hein Lab over a three-month period. We also present our non-intrusive tracing
framework RATracer, which can be retrofitted onto any existing Python-based automation pipeline, and two sets of preliminary
analyses based on the command and power data in RAD.

This repository includes the Robotic Arm Dataset (RAD) along with a non-intrusive tracing framework, RATracer (published with the python package index by the name of niraapad). Additionally, we include scripts and results from preliminary analyses using command and power data.

Details about RATracer and preliminary analyses can be found here: Research Paper Link 

This README file documents the directory structure of this project, documentation on the supervised experiment steps carried out to create RAD, the description of RAD and running the UR Robot Simulator. Further, it describes the steps required to set up, build and run the RATracer along with the steps on running the analysis scripts for command and power data.

## Resources

### Directory Structure

* [`analysis`](./analysis): The scripts, graphs and documentation for reproducing our analysis of command and power data. It also contains the scripts and documentation for evaluating the performance of RATracer.

* [`dataset`](./dataset/README.md): A collection of .csv files and a MongoDB instance. The MongoDB database contains all the original data; the .csv files are extractions from the database and contain labeled data for the supervised experiments as well as a collection of unknown procedures.

* [`docs`](./docs): Additional documents that contains the description of the dataset along with the details of the supervised experiments and their steps. Also documents the steps to install the UR simulator and run it from Python.

* [`tracer`](./tracer): The  non-intrusive tracing framework, RATracer, which uses a middlebox to collect command and power trace data before sending commands to the specific modules.

### Getting Started

##### Collecting Command Data
* [Building and Testing RATracer - Command](./tracer/RATracer_command/runtime_module)
* [Processing Tracing Files](./tracer/RATracer_command/data_processing_module/README.md)
* [Running Command Analysis](./analysis/Dataset_CommandAnalysis/README.md)

##### Collecting Power Monitoring Data
* [Building and Testing RATracer - Power Monitoring](./tracer/RATracer_power_monitoring/README.md)
* [Running Power Analysis](./analysis/Dataset_PowerAnalysis/README.md)


### Robotic Arm Dataset (RAD)
* [Robotic Arm Dataset](./dataset/README.md)
* [Features Description](./docs/RAD_Description.pdf)
* [Experiment Steps](./docs/Experiment_Steps.pdf)
* [Labeled Tracing Files Description](./dataset/README.md)


### Additional Documents

* [Building and Running UR Robot Simulator](./docs/UR_Sim_Setup.pdf)

## Contact

### People
Arpan Gujarati : arbanbg@gmail.com

Zainab Saeed Wattoo : zswattoo@gmail.com

### Organization
University of British Columbia
