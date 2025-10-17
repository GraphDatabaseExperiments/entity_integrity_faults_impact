import mysql.connector
import run_experiments
import excel_writer
import prepare_experiment
import test_scenario_settings
import pandas as pd
import math
import time
import statistics
from datetime import datetime


if __name__ == "__main__":
    


    # Experiment setting

    scenario = 'duplication'

    scaling_factor = 1



    query_numbers = range(1,23)

    percentages_with_error = [0, 0.01, 0.1, 1, 10]  # enter amount of %, i.e. will be divided by 100 later, start with 0 to have time comparisson between query with PK and without



    #query_numbers = [1,8,11,19,20]

    #percentages_with_error = [0]



    amount_of_queries = 22


    runs = 100


    precission_accuracy = 4 # accuracy of recall and precision
    output_accuracy = 2 # accuracy for number of tuples in output
    time_accuracy = 2 # accuracy for execution time

    



    # multi table run

    tables = ["region", "nation", "customer", "orders", "supplier", "part", "partsupp", "lineitem"]
    key_attributes_list = [["r_regionkey"], ["n_nationkey"], ["c_custkey"], ["o_orderkey"], ["s_suppkey"], ["p_partkey"], ["ps_partkey", "ps_suppkey"], ["l_orderkey", "l_linenumber"]]
    parent_fk_attributes = [[[]], [["r_regionkey"]], [["n_nationkey"]], [["c_custkey"]], [["n_nationkey"]], [[]], [["p_partkey"], ["s_suppkey"]], [["o_orderkey"], ["ps_partkey", "ps_suppkey"]]]
    child_fk_attributes = [[[]], [["n_regionkey"]], [["c_nationkey"]], [["o_custkey"]], [["s_nationkey"]], [[]], [["ps_partkey"], ["ps_suppkey"]], [["l_orderkey"], ["l_partkey", "l_suppkey"]]]
    
    if scenario == 'deep_integrity':  # for deep integrity experiments only use tables customer, orders, supplier, part
        tables = tables[2:6]
        key_attributes_list = key_attributes_list[2:6]
        parent_fk_attributes = parent_fk_attributes[2:6]
        child_fk_attributes = child_fk_attributes[2:6]
       

    amount_of_tables = len(tables)

    




    # create connection to MySQL

    with open("mysql_auth.txt") as file:
        user = file.readline()
        password = file.readline()

    host = "localhost"
    if scaling_factor == 0.01:
        database = "tpc-h_small"
        folder_name = "small"
    if scaling_factor == 0.1:
       database = "tpc-h_medium"
       folder_name = "medium"
    if scaling_factor == 1:
       database = "tpc-h_large"
       folder_name = "large"


    my_db_conncetion = mysql.connector.connect(user = user, password = password, host = host, database = database)


    my_cursor = my_db_conncetion.cursor(buffered=True)


    # set buffer sizes, etc

    my_cursor.execute("SET GLOBAL innodb_buffer_pool_size = 34359738368") # 32GB
    my_cursor.execute("SET GLOBAL tmp_table_size = 2147483648") # 2GB
    my_cursor.execute("SET GLOBAL max_heap_table_size = 2147483648") # 2GB
    my_cursor.execute("SET GLOBAL join_buffer_size = 16777216") # 16MB



    # perform experiment each time with errors in a particular table

    for percentage_with_error in percentages_with_error:

        print()
        print(f"Chance to abort experiment at current percentage of error: {percentage_with_error}")
        print()
        for secs in range(10,0,-1):
            print(f"{secs} seconds to stop experiment")
            time.sleep(1)
        print()
        print("Experiment running")
        print()


        overview_table_accuracy = pd.DataFrame()
        overview_table_accuracy[0] = tables + ['', '# tuples in output (original): ', '# tuples in output (adjusted): ']

        overview_table_original_time = pd.DataFrame()
        overview_table_original_time[0] = tables

        overview_table_distorted_time = pd.DataFrame()
        overview_table_distorted_time[0] = tables



        symmetric_differences = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        intersections = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        originals = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        distortions = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        original_times = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        distorted_times = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        collected_accuracies = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]
        collected_precissions = [[[] for _ in range(amount_of_tables)] for _ in range(amount_of_queries)]


        # perform experiment multiple times for each table / query number combination
        for i in range(0, runs):

            for index, table in enumerate(tables):


                print()
                print(f"Current error: {percentage_with_error} percent")
                print(f"{runs-i} more experiment runs to go...")
                print(f"Current table: {table}")
                print(f"Started at {datetime.now().strftime("%H_%M_%S")}")
                print()

                parent_fks = parent_fk_attributes[index]
                child_fks = child_fk_attributes[index]
                key_attributes = key_attributes_list[index]


                # set up experiment setting
                if scenario == "duplication":
                    prepare_experiment.duplicate(my_db_conncetion, my_cursor, table, key_attributes, child_fks, parent_fks, percentage_with_error/100)
                elif scenario == "null":
                    prepare_experiment.introduce_nulls(my_db_conncetion, my_cursor, table, key_attributes, child_fks, parent_fks, percentage_with_error/100)
                elif scenario == "deep_integrity":
                    prepare_experiment.duplicate_deep_entity_integrity(my_db_conncetion, my_cursor, table, key_attributes, child_fks, parent_fks, percentage_with_error/100)



                for query_number in query_numbers:



                    if test_scenario_settings.is_affected(query_number, scaling_factor, table, percentage_with_error):

                          
                        # shows if experiment is still running
                        print()
                        print(f"Current error: {percentage_with_error} percent")
                        print(f"{runs-i} more experiment runs to go...")
                        print(f"Current table: {table}")
                        print(f"Current query: Query {query_number}")
                        print()


                        query, original_time, distorted_time, original_amount, distorted_amount, difference, intersection_amount = run_experiments.run(my_cursor, table, query_number, scaling_factor, scenario) # add connection as parameter for output testing


                        originals[query_number - 1][index].append(original_amount)
                        distortions[query_number - 1][index].append(distorted_amount)
                        symmetric_differences[query_number - 1][index].append(difference)
                        intersections[query_number - 1][index].append(intersection_amount)
                        original_times[query_number - 1][index].append(original_time)
                        distorted_times[query_number - 1][index].append(distorted_time)
                        if original_amount > 0:
                            collected_accuracies[query_number - 1][index].append(intersection_amount/original_amount)
                        else:
                            collected_accuracies[query_number - 1][index].append(0)
                        if distorted_amount > 0:
                            collected_precissions[query_number - 1][index].append(intersection_amount/distorted_amount)
                        else:
                            collected_precissions[query_number - 1][index].append(0)

                        
                        # add to all_results sheet
                        # first create all results sheet with corresponding header manually
                        #
                        if percentages_with_error != 0: # without error only used to measure running time
                            excel_writer.annotate_excel_file_results("results", "all_results.xlsx", scenario, scaling_factor, percentage_with_error, table, query_number, i+1, runs, original_time, distorted_time, original_amount, distorted_amount, intersection_amount)



                # drop duplicated and altered table(s) after all queries are run once
                
                copy_table_deletion = f"DROP TABLE IF EXISTS copy_{table};"
                my_cursor.execute(copy_table_deletion)
                if scenario == 'deep_integrity':
                    for child_table in prepare_experiment.get_child_tables(table):
                        copy_table_deletion = f"DROP TABLE IF EXISTS copy_{child_table};"
                        my_cursor.execute(copy_table_deletion)
                





        

        for query_number in query_numbers:

            average_query_original_output_amounts = []
            average_query_distorted_output_amounts = []
            average_accuracies = []
            average_precissions = []
            average_original_times = []
            average_distorted_times = []

            min_accuracies = []
            mean_accuracies = []
            median_accuracies = []
            max_accuracies = []
            accuracies_for_query = []

            min_precissions = []
            mean_precissions = []
            median_precissions = []
            max_precissions = []
            precissions_for_query = []



            for index, table in enumerate(tables):

                if test_scenario_settings.is_affected(query_number, scaling_factor, table, percentage_with_error):

                    # compute averages for current scenario across all runs
                    average_query_original_output_amount = round(sum(originals[query_number - 1][index])/len(originals[query_number - 1][index]), output_accuracy)
                    average_query_distorted_output_amount = round(sum(distortions[query_number - 1][index])/len(distortions[query_number - 1][index]), output_accuracy)

                    # compute recall (calculated from summed counts instead as average of recalls for each run)
                    if sum(originals[query_number - 1][index]) != 0:
                        average_accuracy = round(sum(intersections[query_number - 1][index]) / sum(originals[query_number - 1][index]), precission_accuracy)
                    else:
                        average_accuracy = "NaN"

                    #compute precission (in line with recall computation)
                    if sum(distortions[query_number - 1][index]) != 0:
                        average_precission = round(sum(intersections[query_number - 1][index]) / sum(distortions[query_number - 1][index]), precission_accuracy)
                    else:
                        average_precission = "NaN"


                    # for average time calculation take outliers out
                    if runs >= 4:
                        start = math.floor(runs/4)
                        end = math.ceil(runs*3/4)
                        original_times[query_number - 1][index] = sorted(original_times[query_number - 1][index])[start:end]
                        distorted_times[query_number - 1][index] = sorted(distorted_times[query_number - 1][index])[start:end]

                    average_original_time = round(sum(original_times[query_number - 1][index])/len(original_times[query_number - 1][index]), time_accuracy)
                    average_distorted_time = round(sum(distorted_times[query_number - 1][index])/len(distorted_times[query_number - 1][index]), time_accuracy)

                    
                    
                    # store averages over different table adjustments in lists

                    average_query_original_output_amounts.append(average_query_original_output_amount)
                    average_query_distorted_output_amounts.append(average_query_distorted_output_amount)
                    average_accuracies.append(average_accuracy)
                    average_precissions.append(average_precission)
                    average_original_times.append(average_original_time)
                    average_distorted_times.append(average_distorted_time)

                    
                    # store min, mean (not computed from summed counts), median and max values in lists

                    accuracies_for_query.append(collected_accuracies[query_number - 1][index])
                    min_accuracies.append(min(collected_accuracies[query_number - 1][index]))
                    mean_accuracies.append(statistics.mean(collected_accuracies[query_number - 1][index]))
                    median_accuracies.append(statistics.median(collected_accuracies[query_number - 1][index]))
                    max_accuracies.append(max(collected_accuracies[query_number - 1][index]))

                    precissions_for_query.append(collected_precissions[query_number - 1][index])
                    min_precissions.append(min(collected_precissions[query_number - 1][index]))
                    mean_precissions.append(statistics.mean(collected_precissions[query_number - 1][index]))
                    median_precissions.append(statistics.median(collected_precissions[query_number - 1][index]))
                    max_precissions.append(max(collected_precissions[query_number - 1][index]))


                else:
                    average_query_original_output_amounts.append("X")
                    average_query_distorted_output_amounts.append("X")
                    average_accuracies.append("X")
                    average_precissions.append("X")
                    average_original_times.append("X")
                    average_distorted_times.append("X")

                    accuracies_for_query.append(["X"])
                    min_accuracies.append("X")
                    mean_accuracies.append("X")
                    median_accuracies.append("X")
                    max_accuracies.append("X")

                    precissions_for_query.append(["X"])
                    min_precissions.append("X")
                    mean_precissions.append("X")
                    median_precissions.append("X")
                    max_precissions.append("X")

    

            # Collect amount of tuples in output of queries on original dataset and adjusted dataset across tables

            original_averages_without_x = [value for value in average_query_original_output_amounts if value != 'X']
            if len(original_averages_without_x) > 0:
                average_tuples_in_output_in_original = sum(original_averages_without_x)/ len(original_averages_without_x)
            else:
                average_tuples_in_output_in_original = 0

            distorted_averages_without_x = [value for value in average_query_distorted_output_amounts if value != 'X']
            if len(distorted_averages_without_x) > 0:
                average_tuples_in_output_in_distorted = sum(distorted_averages_without_x)/ len(distorted_averages_without_x)
            else:
                average_tuples_in_output_in_distorted = 0

            accuracies_stats = [min_accuracies, mean_accuracies, median_accuracies, max_accuracies]
            precissions_stats = [min_precissions, mean_precissions, median_precissions, max_precissions]


            # Write accuracy and execution time results to excel

            excel_writer.write_excel_file_query_results(scenario, f"{folder_name}/{scenario}/query_{query_number}", query_number, query, runs, scaling_factor, percentage_with_error, average_accuracies, accuracies_stats, accuracies_for_query, average_precissions, precissions_stats, precissions_for_query, average_query_original_output_amounts, average_query_distorted_output_amounts, average_original_times, average_distorted_times, tables)
            
            # Collect results for overview and dd empty line, average number of tuples in output on original and adjusted dataset to dataframe
            overview_table_accuracy[query_number] = average_accuracies + ['', average_tuples_in_output_in_original, average_tuples_in_output_in_distorted]
            overview_table_original_time[query_number] = average_original_times
            overview_table_distorted_time[query_number] = average_distorted_times




        # Write accuracy compiled results to excel

        excel_writer.write_overview_from_dataframe_accuracies(f"{folder_name}/{scenario}/accuracy", overview_table_accuracy, scaling_factor, percentage_with_error)

        # Write execution time compiled results to excel

        excel_writer.write_overview_from_dataframe_times(f"{folder_name}/{scenario}/time", overview_table_original_time, overview_table_distorted_time, scaling_factor, percentage_with_error)


    # closing db

    my_cursor.close()

    my_db_conncetion.close()




