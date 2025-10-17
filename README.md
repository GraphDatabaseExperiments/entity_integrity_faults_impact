# How Much Entity Integrity Matters - A Methodology to Quantify the Impact of Entity Integrity Faults

Entity integrity plays a crucial role in ensuring data quality within a relational database. When violated, it leads to various faults that affect the accuracy and reliability of database queries. This repository provides scripts and artifacts from our experiments using a methodology for quantifying the impact of entity integrity faults on database query performance.

## Overview

This repository contains the following:

- results from applying our methodology framework to the TPC-H benchamrk
- files and instructions on how to replicate experiments

# Software Requirements:

The software used to perform the experiments carried out in our research are:

- Python 3.12.2

- MySQL 8.0.40


The TPC-H benchmark is provided on the official [TPC website](https://www.tpc.org/tpch/). 




## Methodology

In this work, we propose a comprehensive methodology for evaluating the impact of entity integrity faults in relational databases. Key components of the methodology include:

Data Quality Metrics:

Uniqueness: Ensures that each entity is represented by a unique identifier.

Completeness: Assesses whether data records are fully populated.

Impact on Query Metrics:

Precision: Measures how accurate the query results are when entity integrity faults are present.

Recall: Evaluates the completeness of the query results under such faults.

Performance: Quantifies how the faults affect the execution time and resource consumption of database queries.


## TPC-H Benchmark:

The methodology is applied to the TPC-H benchmark, a widely-used standard for evaluating the performance of database management systems. By running queries on datasets with different levels of entity integrity faults, we demonstrate the impact of these faults on real-world database tasks.

PROVIDE LINK TO TPC-H and / or UPLOAD SQL files (at least for small dataset)
