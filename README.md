# RosyChem Lab

This project contains the Robotic Arm Dataset (RAD) along with non-intrusive tracing framework, RATracer. Additionally, it also provides analyses on the command and power data 
in RAD. 

This README file provides the link to RAD and its description. Further, it describes the steps required to set up, build and run the RATracer along with 
the steps on running the analysis scripts for power and command data.

## Resources

### Directory Structure

* [`analysis`](https://github.com/ubc-systopia/cps-security-code/tree/main/analysis) contains the scripts and documentation for reproducing the analysis on command and power data. It also provides the scripts and documentation on performing the analysis to evaluate the performance of RATracer.

* [`dataset`](https://github.com/ubc-systopia/cps-security-code/tree/main/dataset) contains RAD that is stored in the form of .csv files where the supervised experiments are labeled as anamolous or benign and the rest are labeled as unknown procedure. RAD is also stored to a MongoDB instance.

* [`docs`](https://github.com/ubc-systopia/cps-security-code/tree/main/docs) contains additional docs that contain the description of the RAD along with the details of the supervised experiments and their steps. Further, they contain steps to install UR simulator and running it via Python script.

* [`tracer`](https://github.com/ubc-systopia/cps-security-code/tree/main/tracer) contains the  non-intrusive tracing framework, RATracer that uses the middlebox to collect the trace data and send commands to the modules.






