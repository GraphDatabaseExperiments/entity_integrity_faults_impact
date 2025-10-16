import mysql.connector
import time
import create_random_parameters
import random
import winsound # for trouble shooting

# can be deleted after output testing again
import pandas as pd
import os


#########################


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



# Execute experiments


def run(cursor, table_name, query_number, scaling_factor, scenario): # insert connection as parameter for output testing

    # create random parameters according to query number

    parameters = create_random_parameters.generate_query_parameters(query_number)


    # Benchmark queries

    query_1 = [[],[f"""select
              l_returnflag,
              l_linestatus,
              sum(l_quantity) as sum_qty,
              sum(l_extendedprice) as sum_base_price,
              sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
              sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
              avg(l_quantity) as avg_qty,
              avg(l_extendedprice) as avg_price,
              avg(l_discount) as avg_disc,
              count(*) as count_order
              from
              lineitem
              where
              l_shipdate <= DATE_ADD('1998-12-01', INTERVAL - {parameters.get('date_range', 0)} DAY)
              group by
              l_returnflag,
              l_linestatus
              order by
              l_returnflag,
              l_linestatus;"""]]


    query_2 = [[],
              [f"""select
              s_acctbal,
              s_name,
              n_name,
              p_partkey,
              p_mfgr,
              s_address,
              s_phone,
              s_comment
              from
              part,
              supplier,
              partsupp,
              nation,
              region
              where
              p_partkey = ps_partkey
              and s_suppkey = ps_suppkey
              and p_size = {parameters.get('size',0)}
              and p_type like CONCAT('%', {parameters.get('type','')})
              and s_nationkey = n_nationkey
              and n_regionkey = r_regionkey
              and r_name = {parameters.get('region','')}
              and ps_supplycost = (
              select
              min(ps_supplycost)
              from
              partsupp, supplier,
              nation, region
              where
              p_partkey = ps_partkey
              and s_suppkey = ps_suppkey
              and s_nationkey = n_nationkey
              and n_regionkey = r_regionkey
              and r_name = {parameters.get('region','')}
              )
              order by
              s_acctbal desc,
              n_name,
              s_name,
              p_partkey;"""]]


    query_3 = [[],
              [f"""select
              l_orderkey,
              sum(l_extendedprice*(1-l_discount)) as revenue,
              o_orderdate,
              o_shippriority
              from
              customer,
              orders,
              lineitem
              where
              c_mktsegment = {parameters.get('segment', '')}
              and c_custkey = o_custkey
              and l_orderkey = o_orderkey
              and o_orderdate < {parameters.get('date', '')}
              and l_shipdate > {parameters.get('date', '')}
              group by
              l_orderkey,
              o_orderdate,
              o_shippriority
              order by
              revenue desc,
              o_orderdate;"""]]


    query_4 = [[],
              [f"""select
              o_orderpriority,
              count(*) as order_count
              from
              orders
              where
              o_orderdate >= {parameters.get('start_date', '')}
              and o_orderdate < {parameters.get('end_date', '')}
              and exists (
              select
              *
              from
              lineitem
              where
              l_orderkey = o_orderkey
              and l_commitdate < l_receiptdate
              )
              group by
              o_orderpriority
              order by
              o_orderpriority;"""]]


    query_5 = [[],
              [f"""select
              n_name,
              sum(l_extendedprice * (1 - l_discount)) as revenue
              from
              customer,
              orders,
              lineitem,
              supplier,
              nation,
              region
              where
              c_custkey = o_custkey
              and l_orderkey = o_orderkey
              and l_suppkey = s_suppkey
              and c_nationkey = s_nationkey
              and s_nationkey = n_nationkey
              and n_regionkey = r_regionkey
              and r_name = {parameters.get('region', '')}
              and o_orderdate >= {parameters.get('start_date', '')}
              and o_orderdate < {parameters.get('end_date', '')}
              group by
              n_name
              order by
              revenue desc;"""]]


    query_6 = [[],
              [f"""select
              sum(l_extendedprice * l_discount) as revenue
              from
              lineitem
              where
              l_shipdate >= {parameters.get('start_date', '')}
              and l_shipdate < {parameters.get('end_date', '')}
              and l_discount between {parameters.get('discount', 0)} - 0.01 and {parameters.get('discount', 0)} + 0.01
              and l_quantity < {parameters.get('quantity', 0)};"""]]


    query_7 = [[],
          [f"""select
          supp_nt,
          cust_nt,
          l_year,
          sum(volume) as revenue
          from
          (
              select
              n1.n_name as supp_nt,
              n2.n_name as cust_nt,
              extract(year from l_shipdate) as l_year,
              l_extendedprice * (1 - l_discount) as volume
              from
              supplier,
              lineitem,
              orders,
              customer,
              nation n1,
              nation n2
              where
              s_suppkey = l_suppkey
              and o_orderkey = l_orderkey
              and c_custkey = o_custkey
              and s_nationkey = n1.n_nationkey
              and c_nationkey = n2.n_nationkey
              and (
                  (n1.n_name = {parameters.get('nation1','')} and n2.n_name = {parameters.get('nation2','')})
                  or (n1.n_name = {parameters.get('nation2','')} and n2.n_name = {parameters.get('nation1','')})
              )   
              and l_shipdate between date '1995-01-01' and date '1996-12-31'
          ) as shipping
          group by
          supp_nt,
          cust_nt,
          l_year
          order by
          supp_nt,
          cust_nt,
          l_year;"""]]


    query_8 = [[],
          [f"""select
          o_year,
          sum(case
              when nt = {parameters.get('nation','')} then volume
              else 0
          end) / sum(volume) as mkt_share
          from
          (
              select
              extract(year from o_orderdate) as o_year,
              l_extendedprice * (1 - l_discount) as volume,
              n2.n_name as nt
              from
              part,
              supplier,
              lineitem,
              orders,
              customer,
              nation n1,
              nation n2,
              region
              where
              p_partkey = l_partkey
              and s_suppkey = l_suppkey
              and l_orderkey = o_orderkey
              and o_custkey = c_custkey
              and c_nationkey = n1.n_nationkey
              and n1.n_regionkey = r_regionkey
              and r_name = {parameters.get('region','')}
              and s_nationkey = n2.n_nationkey
              and o_orderdate between date '1995-01-01' and date '1996-12-31'
              and p_type = {parameters.get('type','')}
          ) as all_nts
          group by
          o_year
          order by
          o_year;"""]]


    query_9 = [[],
              [f"""select
              nt,
              o_year,
              sum(amount) as sum_profit
              from
              (
                  select
                  n_name as nt,
                  extract(year from o_orderdate) as o_year,
                  l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
                  from
                  part,
                  supplier,
                  lineitem,
                  partsupp,
                  orders,
                  nation
                  where
                  s_suppkey = l_suppkey
                  and ps_suppkey = l_suppkey
                  and ps_partkey = l_partkey
                  and p_partkey = l_partkey
                  and o_orderkey = l_orderkey
                  and s_nationkey = n_nationkey
                  and p_name like CONCAT('%', {parameters.get('color','')}, '%')
              ) as profit
              group by
              nt,
              o_year
              order by
              nt,
              o_year desc;"""]]


    query_10 = [[],
              [f"""select
                  c_custkey,
                  c_name,
                  sum(l_extendedprice * (1 - l_discount)) as revenue,
                  c_acctbal,
                  n_name,
                  c_address,
                  c_phone,
                  c_comment
                  from
                  customer,
                  orders,
                  lineitem,
                  nation
                  where
                  c_custkey = o_custkey
                  and l_orderkey = o_orderkey
                  and o_orderdate >= {parameters.get('start_date', '')}
                  and o_orderdate < {parameters.get('end_date', '')}
                  and l_returnflag = 'R'
                  and c_nationkey = n_nationkey
                  group by
                  c_custkey,
                  c_name,
                  c_acctbal,
                  c_phone,
                  n_name,
                  c_address,
                  c_comment
                  order by
                  revenue desc;"""]]


    query_11 = [[],
          [f"""select
          ps_partkey,
          sum(ps_supplycost * ps_availqty) as value
          from
          partsupp,
          supplier,
          nation
          where
          ps_suppkey = s_suppkey
          and s_nationkey = n_nationkey
          and n_name = {parameters.get('nation','')}
          group by
          ps_partkey having
            sum(ps_supplycost * ps_availqty) > (
              select
                sum(ps_supplycost * ps_availqty) * {0.0001 / scaling_factor}
              from
                partsupp,
                supplier,
                nation
              where
                ps_suppkey = s_suppkey
                and s_nationkey = n_nationkey
                and n_name = {parameters.get('nation','')}
            )   
          order by
          value desc;"""]]


    query_12 = [[],
    [f"""select
    l_shipmode,
    sum(case
      when o_orderpriority = '1-URGENT'
        or o_orderpriority = '2-HIGH'
        then 1
      else 0
    end) as high_line_count,
    sum(case
      when o_orderpriority <> '1-URGENT'
        and o_orderpriority <> '2-HIGH'
        then 1
      else 0
    end) as low_line_count
    from
    orders,
    lineitem
    where
    o_orderkey = l_orderkey
    and l_shipmode in ({parameters.get('mode1','')}, {parameters.get('mode2','')})
    and l_commitdate < l_receiptdate
    and l_shipdate < l_commitdate
    and l_receiptdate >= {parameters.get('start_date', '')}
    and l_receiptdate < {parameters.get('end_date', '')}
    group by
    l_shipmode
    order by
    l_shipmode;"""]]


    query_13 = [[],
    [f"""select c_count, count(*) as custdist
    from (
      select
          c_custkey,
          count(o_orderkey) as c_count
      from
          customer left outer join orders on
              c_custkey = o_custkey
              and o_comment not like CONCAT('%', {parameters.get('word1','')}, '%', {parameters.get('word2','')}, 'requests', '%')
      group by  
          c_custkey
      ) as c_ords
    group by  
      c_count
    order by
      custdist desc,
      c_count desc;"""]]


    query_14 = [[],
    [f"""select
    100.00 * sum(case
      when p_type like 'PROMO%'
        then l_extendedprice * (1 - l_discount)
      else 0
    end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
    from
    lineitem,
    part
    where
    l_partkey = p_partkey
    and l_shipdate >= {parameters.get('start_date', '')}
    and l_shipdate < {parameters.get('end_date', '')};"""]]


    query_15 = [[],
    [f"""CREATE VIEW revenue0 (sup_no, total_revenue) as
    select
    l_suppkey,
    sum(l_extendedprice * (1 - l_discount))
    from
    lineitem
    where
    l_shipdate >= {parameters.get('start_date', '')}
    and l_shipdate < {parameters.get('end_date', '')} + interval '3' month
    group by
    l_suppkey;"""],
    ["""select
    s_suppkey,
    s_name,
    s_address,
    s_phone,
    total_revenue
    from
    supplier,
    revenue0
    where
    s_suppkey = sup_no
    and total_revenue = (
      select
        max(total_revenue)
      from
        revenue0
    )
    order by
    s_suppkey;"""],
    ["DROP VIEW revenue0;"]] # only view with stream ID 0 as no parallel execution of queries


    query_16 = [[],
    [f"""select
    p_brand,
    p_type,
    p_size,
    count(distinct ps_suppkey) as sup_cnt
    from
    partsupp,
    part
    where
    p_partkey = ps_partkey
    and p_brand <> {parameters.get('brand', '')}
    and p_type not like CONCAT({parameters.get('type', '')}, '%')
    and p_size in ({parameters.get('sizes', '')})
    and ps_suppkey not in (
      select
        s_suppkey
      from
        supplier
      where
        s_comment like '%Customer%Complaints%'
    )
    group by
    p_brand,
    p_type,
    p_size
    order by
    sup_cnt desc,
    p_brand,
    p_type,
    p_size;"""]]


    query_17 = [[],
    [f"""select
    sum(l_extendedprice) / 7.0 as avg_yearly
    from
    lineitem,
    part
    where
    p_partkey = l_partkey
    and p_brand = {parameters.get('brand', '')}
    and p_container = {parameters.get('container', '')}
    and l_quantity < (
      select
        0.2 *avg(l_quantity)
      from
        lineitem
      where
        l_partkey = p_partkey
    );"""]]


    query_18 = [[],
    [f"""select
    c_name,
    c_custkey,
    o_orderkey,
    o_orderdate,
    o_totalprice,
    sum(l_quantity)
    from
    customer,
    orders,
    lineitem
    where
    o_orderkey in (
      select
        l_orderkey
      from
        lineitem
      group by
        l_orderkey having
          sum(l_quantity) > {parameters.get('quantity', 0)}
    )
    and c_custkey = o_custkey
    and o_orderkey = l_orderkey
    group by
    c_name,
    c_custkey,
    o_orderkey,
    o_orderdate,
    o_totalprice
    order by
    o_totalprice desc,
    o_orderdate;"""]]

    query_19 = [[],
    [f"""select
    sum(l_extendedprice* (1 - l_discount)) as revenue
    from
    lineitem,
    part
    where
    (
      p_partkey = l_partkey
      and p_brand = {parameters.get('brand1', '')}
      and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
      and l_quantity >= {parameters.get('quantity1', 0)} and l_quantity <= {parameters.get('quantity1', 0)} + 10
      and p_size between 1 and 5
      and l_shipmode in ('AIR', 'AIR REG')
      and l_shipinstruct = 'DELIVER IN PERSON'
    )
    or  
    (
      p_partkey = l_partkey
      and p_brand = {parameters.get('brand2', '')}
      and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
      and l_quantity >= {parameters.get('quantity2', 0)} and l_quantity <= {parameters.get('quantity2', 0)} + 10
      and p_size between 1 and 10
      and l_shipmode in ('AIR', 'AIR REG')
      and l_shipinstruct = 'DELIVER IN PERSON'
    )
    or  
    (
      p_partkey = l_partkey
      and p_brand = {parameters.get('brand3', '')}
      and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
      and l_quantity >= {parameters.get('quantity3', 0)} and l_quantity <= {parameters.get('quantity3', 0)} + 10
      and p_size between 1 and 15
      and l_shipmode in ('AIR', 'AIR REG')
      and l_shipinstruct = 'DELIVER IN PERSON'
    );"""]]

    query_20 = [[],
    [f"""select
    s_name,
    s_address
    from
    supplier,
    nation
    where
    s_suppkey in (
      select
        ps_suppkey
      from
        partsupp
      where
        ps_partkey in (
          select
            p_partkey
          from
            part
          where
            p_name like CONCAT({parameters.get('color', '')}, '%')
        )   
        and ps_availqty > (
          select
            0.5 * sum(l_quantity)
          from
            lineitem
          where
            l_partkey = ps_partkey
            and l_suppkey = ps_suppkey
            and l_shipdate >= {parameters.get('start_date', '')}
            and l_shipdate < {parameters.get('end_date', '')}
        )   
    )
    and s_nationkey = n_nationkey
    and n_name = {parameters.get('nation', '')}
    order by
    s_name;"""]]


    query_21 = [[],
    [f"""select
          s_name,
          count(*) as numwait
    from
          supplier,
          lineitem l1,
          orders,
          nation
    where
          s_suppkey = l1.l_suppkey
          and o_orderkey = l1.l_orderkey
          and o_orderstatus = 'F'
          and l1.l_receiptdate > l1.l_commitdate
          and exists (
                  select *
                  from
                          lineitem l2
                  where
                          l2.l_orderkey = l1.l_orderkey
                          and l2.l_suppkey <> l1.l_suppkey
          )
          and not exists (
                  select
                          *
                  from
                          lineitem l3
                  where
                          l3.l_orderkey = l1.l_orderkey
                          and l3.l_suppkey <> l1.l_suppkey
                          and l3.l_receiptdate > l3.l_commitdate
          )
          and s_nationkey = n_nationkey
          and n_name = {parameters.get('nation', '')}
    group by
          s_name
    order by
          numwait desc,
          s_name;"""]]
    

    query_22 = [[],[f"""select
    cntrycode,
    count(*) as numcust,
    sum(c_acctbal) as totacctbal
    from
    (
      select
        substring(c_phone, 1, 2) as cntrycode,
        c_acctbal
      from
        customer
      where
        substring(c_phone, 1, 2) in ({parameters.get('phone_string', '')})
        and c_acctbal > (
          select
            avg(c_acctbal)
          from
            customer
          where
            c_acctbal > 0.00
            and substring(c_phone, 1, 2) in ({parameters.get('phone_string', '')})
        )   
        and not exists (
          select
            *
          from
            orders
          where
            o_custkey = c_custkey
        )   
    ) as custsale
    group by
    cntrycode
    order by
    cntrycode;"""]]






    # run benchmark query


    #queries = [query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10,
    #       query_11, query_12, query_13, query_14, query_15, query_16, query_17, query_18, query_19, query_20,
    #       query_21, query_22]
    
    #queries = [query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10,
    #    query_11, query_12, query_13, query_14, query_15, query_16, query_17, [[],["SELECT * FROM region;"]], query_19, query_20, query_21, query_22]
    
    queries = [query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10,
        query_11, query_12, query_13, query_14, query_15, query_16, query_17, query_18, query_19, query_20, query_21, query_22]


    query = queries[query_number - 1]



    # create query setting with random parameters staying the same for original table and table with duplicates


    # become redundant, parameters now created in Python and not in SQL
    """ 
    query_parameter_setting = query[0] 
    for subquery in query_parameter_setting:
        cursor.execute(subquery, multi=True)
    """


    if query_number == 15:
        
        # regular view creation
        query_view_creation = query[1][0]
        cursor.execute(query_view_creation, multi=True)

        # view creation with duplicates in lineitem
        query_view_creation_adjusted = query_view_creation.replace("revenue0", "copy_revenue0")
        if table_name == "lineitem":
          query_view_creation_adjusted = query_view_creation_adjusted.replace("lineitem", "copy_lineitem")
        cursor.execute(query_view_creation_adjusted, multi=True)



    # create adjusted query, i.e. query that selects from tables with entity integrity violations
    
    if query_number == 15:
        original_query = query[2][0][:-1]
        adjusted_query = original_query.replace("revenue0", "copy_revenue0")
    else:
        original_query = query[1][0][:-1]
        adjusted_query = original_query



    # avoid accidentally replacing regionkey with copy_regionkey, etc. and adjust table name
    
    adjusted_query = adjusted_query.replace(table_name + "key", table_name[:1] + "x" + table_name[1:] + "key")
    if query_number == 21 and table_name =="orders":
        adjusted_query = adjusted_query.replace("orderstatus", "ostatus")
    if table_name == "part":
        adjusted_query = adjusted_query.replace("partsupp", "psupp")




    # select scenario to either only change one table to copy_<table_name> (for entity integrity experiments) or make changes to multiple tables
    #
    # should ideally be recursive depending on how far pk attributes propagate along child table chain
    #  |
    #  v

    adjusted_query = adjusted_query.replace(table_name, "copy_" + table_name)

    if scenario == 'deep_integrity':

      tables_to_change = get_child_tables(table_name)

      for table_to_change in tables_to_change:
          adjusted_query = adjusted_query.replace(table_to_change, "copy_" + table_to_change)
          
          if table_to_change == 'partsupp': # this is hard-coded and shoudld ideally be done via recursion
              tables_of_child_to_change = get_child_tables(table_to_change)
              for table_of_child_to_change in tables_of_child_to_change:
                  adjusted_query = adjusted_query.replace(table_of_child_to_change, "copy_" + table_of_child_to_change)
              

    

    adjusted_query = adjusted_query.replace(table_name[:1] + "x" + table_name[1:] + "key", table_name + "key")
    if query_number == 21 and table_name =="orders":
        adjusted_query = adjusted_query.replace("ostatus", "orderstatus")
    if table_name == "part":
        adjusted_query = adjusted_query.replace("psupp", "partsupp")


    
    # run query on original tables and query on tables with duplicates

    cursor.execute("DROP TABLE IF EXISTS `result_1`")
    cursor.execute("DROP TABLE IF EXISTS `result_2`")

    cursor.execute("SET profiling = 1")

    
    query_result_table_creation = [f"CREATE TABLE result_1 AS ({original_query});",
                  f"CREATE TABLE result_2 AS ({adjusted_query});"]
    


    # execute original query and measure time
    cursor.execute(query_result_table_creation[0], multi=True)


    cursor.execute("SHOW PROFILES")
    profile = cursor.fetchall()
    original_query_time_in_ms = round(profile[-1][1]*1000,2)









    # execute (adjusted) query on tables with duplicates and measure time
    cursor.execute(query_result_table_creation[1], multi=True)

    cursor.execute("SHOW PROFILES")
    profile = cursor.fetchall()
    distorted_query_time_in_ms = round(profile[-1][1]*1000,2)

    cursor.execute("SET profiling = 0")







    #columns_for_query = [column[0] for column in cursor] # accesing tuple column without leading


    #join_condition = f" ON result_1.{columns_for_query[0]} = result_2.{columns_for_query[0]} " 
    #for column in columns_for_query[1:]:
    #    join_condition += f"AND result_1.{column} = result_2.{column} "

    #not_null_condition = f" WHERE (result_1.{columns_for_query[0]} IS NOT NULL OR result_2.{columns_for_query[0]} IS NOT NULL) " 
    #for column in columns_for_query[1:]:
    #    not_null_condition += f"OR (result_1.{columns_for_query[0]} IS NOT NULL OR result_2.{columns_for_query[0]} IS NOT NULL) "

    #query_second = [f"SELECT COUNT(*) FROM (SELECT * FROM result_1 LEFT JOIN result_2 {join_condition} {not_null_condition}) AS alias1 UNION (SELECT * FROM result_1 RIGHT JOIN result_2 {join_condition} {not_null_condition})"]
    #                "DROP VIEW result_1;",
    #                "DROP VIEW result_2;"]

    query_union = "SELECT COUNT(*) FROM (SELECT * FROM result_1 UNION SELECT * FROM result_2) AS union_count;"
    cursor.execute(query_union)

    for result in cursor:
        union_count = result[0]

  

    query_intersect = "SELECT COUNT(*) FROM (SELECT * FROM result_1 INTERSECT SELECT * FROM result_2) AS intersect_count;"
    cursor.execute(query_intersect)

    for result in cursor:
        intersect_count = result[0]


    

    query_original = "SELECT COUNT(*) FROM result_1;"
    cursor.execute(query_original)

    for result in cursor:
        amount_original = result[0]



    query_error = "SELECT COUNT(*) FROM result_2;"
    cursor.execute(query_error)

    for result in cursor:
        amount_distorted = result[0]


    ######################################
    #  for debugging purposes only
    """
    query_original = "SELECT * FROM result_1;"
    cursor.execute(query_original)

    print()
    for result in cursor:
        print(result)
    print()
    print()


    query_error = "SELECT * FROM result_2;"
    cursor.execute(query_error)

    for result in cursor:
        print(result)

    print()
    """


    ######################################

    
    """
    # for trouble shooting, can be removed again
    for secs in range(10,0,-1):
      print(f"{secs} seconds to view experiment experiment results")
      winsound.Beep(2500, 1000)
      time.sleep(1)
    """
    


    if query_number == 15:
      
      # drop regular view
      query_view_drop = query[3][0]
      cursor.execute(query_view_drop, multi=True)

      # drop adjusted view
      query_view_drop_adjusted = query_view_drop.replace("revenue0", "copy_revenue0")
      cursor.execute(query_view_drop_adjusted, multi=True)
    



    query_result_deletion = ["DROP TABLE result_1", "DROP TABLE result_2"]

    for subquery in query_result_deletion:
        cursor.execute(subquery, multi=True)

    #times = [round(time_of_run, precision) for time_of_run in sorted(times)[outliers:-outliers]]


    #average_time = round(sum(times)/(runs - 2*outliers), precision)



    query_string = "\n".join(["\n".join(subquery) for subquery in query])


    # now done in main python file
    """
    if scenario == 'deep_integrity':
      # adjust in case deletion of parents and / or parents of parents is required!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      # |
      # V

      child_tables_to_drop = get_child_tables(table_name)

      for child_to_drop in child_tables_to_drop:
          cursor.execute(f"DROP TABLE IF EXISTS copy_{child_to_drop};")
    """


    return query_string, original_query_time_in_ms, distorted_query_time_in_ms, amount_original, amount_distorted, union_count - intersect_count, intersect_count




