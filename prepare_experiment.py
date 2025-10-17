import math



#################################################
#
# Helper Functions
#
#################################################


def get_parent_tables(table_name: str) -> list:
    if table_name == "region":
        parent_tables = []
    if table_name == "nation":
        parent_tables = ["region"]
    if table_name == "customer":
        parent_tables = ["nation"]
    if table_name == "orders":
        parent_tables = ["customer"]
    if table_name == "lineitem":
        parent_tables = ["orders", "partsupp"]
    if table_name == "part":
        parent_tables = []
    if table_name == "supplier":
        parent_tables = ["nation"]
    if table_name == "partsupp":
        parent_tables = ["part", "supplier"]
    return parent_tables



def get_child_tables(table_name: str) -> list:
    if table_name == "region":
        child_tables = ["nation"]
    if table_name == "nation":
        child_tables = ["supplier", "customer"]
    if table_name == "customer":
        child_tables = ["orders"]
    if table_name == "orders":
        child_tables = ["lineitem"]
    if table_name == "lineitem":
        child_tables = []
    if table_name == "part":
        child_tables = ["partsupp"]
    if table_name == "supplier":
        child_tables = ["partsupp"]
    if table_name == "partsupp":
        child_tables = ["lineitem"]
    return child_tables



def table_copying(cursor, table_name):

    table_copying = [f"DROP TABLE IF EXISTS copy_{table_name};",
    f"CREATE TABLE copy_{table_name} LIKE {table_name};",
    f"INSERT INTO copy_{table_name} SELECT * FROM {table_name};"]
    
    for subquery in table_copying:
        cursor.execute(subquery)


def table_preparation(cursor, table_name):

    table_duplication = [f"DROP TABLE IF EXISTS copy_{table_name};",
    f"CREATE TABLE copy_{table_name} LIKE {table_name};",
    f"ALTER TABLE copy_{table_name} DROP PRIMARY KEY;", # drop primary key for faster insertion of records
    f"INSERT INTO copy_{table_name} SELECT * FROM {table_name};"]
    
    for subquery in table_duplication:
        cursor.execute(subquery)



def determine_amount(cursor, table_name, percentage_with_error):
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    for result in cursor:
        amount = result[0]

    # only duplicate one tuple for region and nation as they have fixed amount of 5 and 25 tuples respectively for all scaling factors

    if table_name == 'region' or table_name == "nation":
        if percentage_with_error == 0:
            amount_to_duplicate = 0
        else:
            amount_to_duplicate = 1
    else:
        amount_to_duplicate = math.floor(percentage_with_error*amount)
    return amount_to_duplicate



def create_parent_table_fks(cursor, table_name, fk_attributes_child, fk_attributes_parent):
    
    parent_tables = get_parent_tables(table_name)

    fk_creation = []
    for index in range(len(parent_tables)):
        fk_creation.append(f"ALTER TABLE copy_{table_name} ADD CONSTRAINT copy_{table_name}_{parent_tables[index]}_fk FOREIGN KEY ({", ".join(fk_attributes_child[index])}) REFERENCES {parent_tables[index]} ({", ".join(fk_attributes_parent[index])});")


    for subquery in fk_creation:
        cursor.execute(subquery)







#################################################
#
# Duplication of random rows in table
#
#################################################

def duplicate(connection, cursor, table_name: str, key_attributes: list, fk_attributes_child: list, fk_attributes_parent: list, percentage_with_error: float):


    table_preparation(cursor, table_name)  

    amount_to_duplicate = determine_amount(cursor, table_name, percentage_with_error)


    # insert random duplicates into table at random (note that PK already dropped)

    duplication_query = f"""INSERT INTO copy_{table_name}
        SELECT *
        FROM {table_name}
        WHERE ({', '.join(key_attributes)}) IN (
            SELECT {', '.join(['k_attributes.' + k for k in key_attributes])}
            FROM (
                SELECT {', '.join(key_attributes)}
                FROM {table_name}
                ORDER BY RAND()
                LIMIT {amount_to_duplicate}
            ) AS k_attributes
        );
        """

    cursor.execute(duplication_query)


    create_parent_table_fks(cursor, table_name, fk_attributes_child, fk_attributes_parent)



    # add FK constraints from child table(s)
    #
    # also add FK constraints to child tables in null and deep integrity scenario, only speed up, accuracy won't change
    """
    # maybe not add fks to child table as index creation on key attributes on altered table necessary
    
    child_tables = get_child_tables(table_name)

    fk_creation = []
    if len(child_tables) > 0:
        pass #add to fk_creation index creation for key attribute in table_name / this will again speed up query execution even if fk not being used
    for index in range(len(child_tables)):
        fk_creation.append(f"ALTER TABLE {child_tables[index]} DROP CONSTRAINT {child_tables[index]}_{table_name}_fk")

    for subquery in fk_creation:
        cursor.execute(subquery)
    """
    connection.commit()







#################################################
#
# Setting random PK attributes to NULL
#
#################################################



def introduce_nulls(connection, cursor, table_name: str, key_attributes: list, fk_attributes_child: list, fk_attributes_parent: list, percentage_with_error: float):


    table_preparation(cursor, table_name)

    amount_to_set_to_null = determine_amount(cursor, table_name, percentage_with_error)



    # allow PK attributes to be NULL

    change_pk_domain = f"""ALTER TABLE copy_{table_name}
                        {', '.join([f"MODIFY {k} INT NULL" for k in key_attributes])};"""
    cursor.execute(change_pk_domain)



    # set PK attributes to NULL in table at random (note that PK already dropped)
    #
    # if only one key attribute set to NULL, if two attributes set either one or both to NULL at random

    if len(key_attributes) == 1: 
        null_query = ["SET SQL_SAFE_UPDATES = 0;", # turning off safe update mode should actually not be required as PK already dropped, but somehow now working without it
                    f"""UPDATE copy_{table_name} AS changing
                        JOIN (
                            SELECT {', '.join(key_attributes)}
                            FROM copy_{table_name}
                            ORDER BY RAND()
                            LIMIT {amount_to_set_to_null}
                        ) AS temp
                        ON
                        {' AND '.join([f"changing.{k} = temp.{k}" for k in key_attributes])}
                        SET{','.join([f" changing.{k} = NULL" for k in key_attributes])};
                        """,
                        "SET SQL_SAFE_UPDATES = 1;"] # turning safe update mode on again
    else:
        null_query = ["SET SQL_SAFE_UPDATES = 0;", # turning off safe update mode should actually not be required as PK already dropped, but somehow now working without it
            f"""UPDATE copy_{table_name} AS changing
                JOIN (
                    SELECT {', '.join(key_attributes)}, RAND() AS r1, RAND() AS r2
                    FROM copy_{table_name}
                    ORDER BY R1
                    LIMIT {amount_to_set_to_null}
                ) AS temp
                ON
                {' AND '.join([f"changing.{k} = temp.{k}" for k in key_attributes])}
                SET{','.join([f" changing.{k} = CASE WHEN temp.r2 BETWEEN {0.3333 * index} AND {0.3333 * (index+2)} THEN NULL ELSE changing.{k} END" for index, k in enumerate(key_attributes)])};
                """,
                "SET SQL_SAFE_UPDATES = 1;"] # turning safe update mode on again


    for subquery in null_query:
        cursor.execute(subquery)


    create_parent_table_fks(cursor, table_name, fk_attributes_child, fk_attributes_parent)

    connection.commit()






#################################################
#
# Establish Deep Integrity violation setting
#
#################################################


def duplicate_deep_entity_integrity(connection, cursor, table_name: str, key_attributes: list, fk_attributes_child: list, fk_attributes_parent: list, percentage_with_error):

    table_copying(cursor, table_name)

    amount_to_duplicate = determine_amount(cursor, table_name, percentage_with_error)

    
    # create temporary table with duplicated entities with different primary key

    temp_table_creation = [f"DROP TABLE IF EXISTS temp_{table_name};",
                           f"CREATE TABLE temp_{table_name} LIKE {table_name};",
                            f"""INSERT INTO temp_{table_name}
                            SELECT *
                            FROM {table_name}
                            WHERE ({', '.join(key_attributes)}) IN (
                                SELECT {', '.join(['k_attributes.' + k for k in key_attributes])}
                                FROM (
                                    SELECT {', '.join(key_attributes)}
                                    FROM {table_name}
                                    ORDER BY RAND()
                                    LIMIT {amount_to_duplicate}
                                ) AS k_attributes
                            );""",
                            f"UPDATE temp_{table_name} SET {', '.join([f"{k} = -{k}" for k in key_attributes])} WHERE {' AND '.join([f"{k} > 0" for k in key_attributes])};"] # > 0 condition is just because of safe update mode


    for subquery in temp_table_creation:
        cursor.execute(subquery)


    # insert new entities into table and add fk constraints to parent tables

    new_entity_query = f"""INSERT INTO copy_{table_name}
    SELECT * FROM temp_{table_name}"""
    cursor.execute(new_entity_query)


    create_parent_table_fks(cursor, table_name, fk_attributes_child, fk_attributes_parent)



    # create copy of referenced table(s) and change foreign keys in referenced table to randomly either reference original or duplicated (with new key) entity

    # might have to change to nested lists as nation has child tables customer and supplier and lineitem child of orders and partsupp
    #
    # issues for copying partsupp and introducing new records as new pk attributes on partsupp violate fks from partsupp to part and to supplier
    # same for copying lineitem with new pk values on l_ordkery violating fk from lineitem to orders
    #
    # also loop below would need changing to altering fks in multiple tables in case table_name is nation
    #  |
    #  v

    child_tables = get_child_tables(table_name)

    #child_fk_attributes = {'region' : ["n_regionkey"],'nation' :  ["c_nationkey"],'customer' :  ["o_custkey"],'orders' :  ["l_orderkey"],'supplier' :  ["ps_suppkey"],'part' :  ["ps_partkey"],'partsupp' :  ["l_partkey", "l_suppkey"],'lineitem' :  []}
    child_fk_attributes = {'region' : [{}],'nation' :  {'region' : ["n_regionkey"]},'customer' : {'nation' : ["c_nationkey"]},'orders' :  {'customer' : ["o_custkey"]},'supplier' : {'nation' : ["s_nationkey"]},'part' :  [{}],'partsupp' :  {'part' : ["ps_partkey"], 'supplier' : ["ps_suppkey"]},'lineitem' :  {'partsupp' : ["l_partkey", "l_suppkey"], 'orders' : ["l_orderkey"]}}

    # should ideally be recursive depending on how far pk attributes propagate along child table chain
    #  |
    #  v

    for new_table in child_tables:
        table_copying(cursor, new_table)

        if new_table == "partsupp":
            children_of_new_table = get_child_tables(new_table)
            for child_of_new_table in children_of_new_table:
                table_copying(cursor, child_of_new_table)


    for new_table in child_tables:
        fk_attributes = child_fk_attributes[new_table][table_name]
        for index, fk_attribute in enumerate(fk_attributes):
            fk_altering_query = ["SET SQL_SAFE_UPDATES = 0;", # turning off safe update mode to update fk attribute value
                                f"""UPDATE copy_{new_table}
                                    SET {fk_attribute} = CASE
                                        WHEN RAND() < 0.5 AND {fk_attribute} IN (SELECT -{key_attributes[index]} FROM temp_{table_name}) THEN -{fk_attribute}
                                        ELSE {fk_attribute}
                                    END
                                    WHERE {fk_attribute} > 0;""", # > 0 condition just because of safe mode
                                "SET SQL_SAFE_UPDATES = 1;"]

            for subquery in fk_altering_query:
                cursor.execute(subquery)

        # propagate changes in partsupp consistently up to lineitem
        #
        # ideally generalize part below
        #  |
        #  v

        if new_table == "partsupp":
            if table_name == "part":
                fk_propagation_query =["DROP TABLE IF EXISTS excluded;",
                                    """CREATE TABLE excluded AS
                                    (
                                        SELECT l_partkey, l_suppkey
                                        FROM copy_lineitem
                                        WHERE (l_partkey, l_suppkey) NOT IN
                                        (
                                            SELECT ps_partkey, ps_suppkey
                                            FROM copy_partsupp
                                        )
                                    );""",
                                    "SET SQL_SAFE_UPDATES = 0;",
                                    """UPDATE copy_lineitem
                                    SET l_partkey = CASE
                                        WHEN (l_partkey, l_suppkey) IN (SELECT * FROM excluded) THEN -l_partkey
                                        ELSE l_partkey
                                        END;""",
                                    "SET SQL_SAFE_UPDATES = 1;"]
            if table_name == "supplier":
                fk_propagation_query =["DROP TABLE IF EXISTS excluded;",
                                    """CREATE TABLE excluded AS
                                    (
                                        SELECT l_partkey, l_suppkey
                                        FROM copy_lineitem
                                        WHERE (l_partkey, l_suppkey) NOT IN
                                        (
                                            SELECT ps_partkey, ps_suppkey
                                            FROM copy_partsupp
                                        )
                                    );""",
                                    "SET SQL_SAFE_UPDATES = 0;",
                                    """UPDATE copy_lineitem
                                    SET l_suppkey = CASE
                                        WHEN (l_partkey, l_suppkey) IN (SELECT * FROM excluded) THEN -l_suppkey
                                        ELSE l_suppkey
                                    END;""",
                                    "SET SQL_SAFE_UPDATES = 1;"]

            for subquery in fk_propagation_query:
                cursor.execute(subquery)
            

        
                

    # delete temporary table again

    temp_table_creation = f"DROP TABLE IF EXISTS temp_{table_name};"
    cursor.execute(temp_table_creation)

    connection.commit()




