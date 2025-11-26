# Instructions

This file contains instructions on how to recreate the experiments conducted in our work.

## Execution

The main script to run our experiments is data_integrity_effects_sql.py. To establish a connection with a MySQL database a file called mysql_auth.txt has be created with corresponding credentials.

### Parameter Settings

On the top of the script are the parameters located that can be adjusted to run the experiments.

```

scenario = 'duplication'

scaling_factor = 1


query_numbers = range(1,23)

percentages_with_error = [0, 0.01, 0.1, 1, 10] 


runs = 100
```

For the variable *scenario* the values 'duplication', 'null' and 'deep_integrity' can be chosen to inject the dataset with one of the three kinds of entity integrity violations.

For *scaling_factor* a value has to be decided for which TPC-H has been generated. In our experiments we have chosen 0.01, 0.1 and 1. For more information on TPC-H we refer to the [dataset folder](/./dataset).

For *query_numbers* the benchmark queries that are supposed to be executed can be set. For the full TPC-H workload this can remain as is.

The values in *percentages_with_error* determine which percentage of integrity violations should be injected. Each element in this list determines a percentage for which the amount of experiment runs specified by the variable *runs* is executed. The value 0 is included as this is used to determine the execution time on the original and dirty dataset. Here, the dirty dataset includes 0% entity integrity faults, i.e. is the original dataset, however, primary keys and associated indices have been removed.
