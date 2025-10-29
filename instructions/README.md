# Instructions

This file contains instructions on how to recreate the experiments conducted in our work.

## Execution

The main script to run our experiments is data_integrity_effects_sql.py

### Parameter Settings

On the top of the script are the parameters located that can be adjusted to run the experiments.

```

scenario = 'duplication'

scaling_factor = 1


query_numbers = range(1,23)

percentages_with_error = [0, 0.01, 0.1, 1, 10] 


runs = 100
```

For scenario the values 'duplication', 'null' and 'deep_integrity' can be chosen to inject the dataset with one of the three kinds of entity integrity violations. For scaling_factor a value has to be decided for which TPC-H has been generated. In our experiments we have chosen 0.01, 0.1 and 1. For more information on TPC-H we refer to the [dataset folder](/../dataset).
