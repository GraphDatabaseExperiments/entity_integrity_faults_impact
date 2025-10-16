# determine if scenario has affect on query to speed up experiments

def is_affected(query_number, scaling_factor, table, error) -> bool:
    
    is_affected = False

    if query_number == 1 or query_number == 6:
        if table == "lineitem":
            is_affected = True


    elif query_number == 2:
        if table == "region" or table == "nation":
            is_affected = True
        elif table ==  "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True
        elif table ==  "part":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True     
        elif table ==  "partsupp":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True


    elif query_number == 3 or query_number == 18:
        if table == "customer":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "lineitem":
            is_affected = True


    elif query_number == 4:
        if table == "orders":
            is_affected = True
        elif table == "lineitem":
            is_affected = True


    elif query_number == 5:
        if table == "region":
            is_affected = True
        elif table == "nation":
            is_affected = True
        elif table == "customer":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True              
        elif table == "lineitem":
            is_affected = True


    elif query_number == 6:
        if table == "lineitem":
            is_affected = True
        

    elif query_number == 7:
        if table == "nation":
            is_affected = True
        elif table == "customer":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True    
        elif table == "lineitem":
            is_affected = True


    elif query_number == 8:
        if table == "region":
            is_affected = True
        elif table == "nation":
            is_affected = True
        elif table == "customer":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True
        elif table ==  "part":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True   
        elif table == "lineitem":
            is_affected = True


    elif query_number == 9:
        if table == "nation":
            is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True
        elif table ==  "part":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True  
        elif table ==  "partsupp":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True
        elif table == "lineitem":
            is_affected = True


    elif query_number == 10:
        if table == "nation":
            is_affected = True
        elif table == "customer":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "lineitem":
            is_affected = True


    elif query_number == 11:
        if table == "nation":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True              
        elif table ==  "partsupp":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True


    elif query_number == 12:
        if table == "orders":
            is_affected = True
        elif table == "lineitem":
            is_affected = True


    elif query_number == 13:
        if table == "customer":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True
        elif table == "orders":
            is_affected = True


    elif query_number == 14 or query_number == 17 or query_number == 19:
        if table ==  "part":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True
        elif table == "lineitem":
            is_affected = True


    elif query_number == 15:
        if table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True            
        elif table == "lineitem":
            is_affected = True


    elif query_number == 16:
        if table ==  "part":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True  
        elif table ==  "partsupp":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True


    elif query_number == 20:
        if table == "nation":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True            
        elif table ==  "part":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True  
        elif table == "lineitem":
            is_affected = True


    elif query_number == 21:
        if table == "nation":
            is_affected = True
        elif table == "orders":
            is_affected = True
        elif table == "supplier":
            if error == 0:
                is_affected = True
            if scaling_factor == 0.01:
                if error >= 1:
                    is_affected = True
            elif scaling_factor == 0.1:
                if error > 0.01:
                    is_affected = True
            else:
                is_affected = True  
        elif table == "lineitem":
            is_affected = True


    elif query_number == 22:
        if table == "customer":
            if not (scaling_factor == 0.01 and 0 < error <= 0.01):
                is_affected = True
        elif table == "orders":
            is_affected = True

    return is_affected