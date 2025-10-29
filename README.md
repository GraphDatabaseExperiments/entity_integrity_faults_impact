# How Much Entity Integrity Matters - A Methodology to Quantify the Impact of Entity Integrity Faults

Entity integrity plays a crucial role in ensuring data quality within a relational database. When violated, it leads to various faults that affect the accuracy and reliability of database queries. This repository provides scripts and artifacts from our experiments using a methodology for quantifying the impact of entity integrity faults on database query performance.

## Overview

This repository contains the following:

- results from applying our methodology framework to the TPC-H benchamrk
- files and instructions on how to replicate experiments

## Software Requirements:

The software used to perform the experiments carried out in our research are:

- Python 3.12.2

- MySQL 8.0.40


The TPC-H benchmark is provided on the official [TPC website](https://www.tpc.org/tpch/). 




## Methodology

In this work, we propose a comprehensive methodology for evaluating the impact of entity integrity faults in databases. It focuses on three causes of entity integrity faults: duplicate records, missing values in primary key attributes, and deep entity integrity violations where real-world entities are recorded multiple times with different identifiers. Different scaling factors of the datasets are chosen and different percentages of each of these violations are injected into the dataset to measure the impact of these dimensions. The methodology evaluates query accuracy using recall and precision metrics, comparing outputs from clean and faulty datasets. Additionally, it considers performance by measuring query execution time. Underneath we listed how these metrics are cacluated.

### Recall:

Recall measures the proportion of correct query answers preserved after introducing entity integrity faults. It compares the overlap between the clean and faulty dataset query results.

### Precision:

Precision evaluates how many of the new query answers from the dirty dataset are correct. It compares the overlap between the clean and dirty query results.

### Performance:

Performance is measured by query execution time, which evaluates how entity integrity faults affect the efficiency of database operations, especially in cases where primary keys are not enforced and a correpsonding index is not present in the database.


## Proof of Concept:

As proof of concept we applied our methodology to the TPC-H benchmark, a widely-used standard for evaluating the performance of relational database management systems. By running queries on datasets with different levels of entity integrity faults, we demonstrate the impact of these faults on analytical query workloads. We measure recall and precision of queries in addition to execution time.

Information on how to replicate the experiments can be found in the [instructions folder](/instructions).

The results of our experiments are located in this repository in the [results folder](/results)

