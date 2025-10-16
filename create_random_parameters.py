import random
from datetime import date, timedelta


def generate_query_parameters(query_num):

    types_size = ['STANDARD', 'SMALL', 'MEDIUM', 'LARGE', 'ECONOMY', 'PROMO']
    types_fabrication = ['ANODIZED', 'BURNISHED', 'PLATED', 'POLISHED', 'BRUSHED']
    types_metal = ['TIN', 'NICKEL', 'BRASS', 'STEEL', 'COPPER']
    container_sizes = ['SM', 'LG', 'MED', 'JUMBO', 'WARP']
    container_packaging = ['CASE', 'BOX', 'JAR', 'PKG', 'PACK', 'CAN', 'DRUM']
    regions = ['AFRICA', 'AMERICA', 'ASIA', 'EUROPE', 'MIDDLE EAST']
    segments = ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'MACHINERY', 'HOUSEHOLD']
    modes = ['REG AIR', 'AIR', 'RAIL', 'SHIP', 'TRUCK', 'MAIL', 'FOB']
    nations = ['ALGERIA',
        'ARGENTINA',
        'BRAZIL',
        'CANADA',
        'EGYPT',
        'ETHIOPIA',
        'FRANCE',
        'GERMANY',
        'INDIA',
        'INDONESIA',
        'IRAN',
        'IRAQ',
        'JAPAN',
        'JORDAN',
        'KENYA',
        'MOROCCO',
        'MOZAMBIQUE',
        'PERU',
        'CHINA'
        'ROMANIA',
        'SAUDI ARABIA',  
        'VIETNAM',
        'RUSSIA',
        'UNITED KINGDOM',
        'UNITED STATES']
    regions_by_nation = [
    'AFRICA',
    'AMERICA',
    'AMERICA',
    'AMERICA',
    'AFRICA',
    'AFRICA',
    'EUROPE',
    'EUROPE',
    'ASIA',
    'ASIA',
    'ASIA',
    'ASIA',
    'ASIA',
    'ASIA',
    'AFRICA',
    'AFRICA',
    'AFRICA',
    'AMERICA',
    'ASIA',
    'EUROPE',
    'ASIA',
    'ASIA',
    'EUROPE',
    'EUROPE',
    'AMERICA']
    colors = [
    'almond',
    'antique',
    'aquamarine',
    'azure',
    'beige',
    'bisque',
    'black',
    'blanched',
    'blue',
    'blush',
    'brown',
    'burlywood',
    'burnished',
    'chartreuse',
    'chiffon',
    'chocolate',
    'coral',
    'cornflower',
    'cornsilk',
    'cream',
    'cyan',
    'dark',
    'deep',
    'dim',
    'dodger',
    'drab',
    'firebrick',
    'floral',
    'forest',
    'frosted',
    'gainsboro',
    'ghost',
    'goldenrod',
    'green',
    'grey',
    'honeydew',
    'hot',
    'indian',
    'ivory',
    'khaki',
    'lace',
    'lavender',
    'lawn',
    'lemon',
    'light',
    'lime',
    'linen',
    'magenta',
    'maroon',
    'medium',
    'metallic',
    'midnight',
    'mint',
    'misty',
    'moccasin',
    'navajo',
    'navy',
    'olive',
    'orange',
    'orchid',
    'pale',
    'papaya',
    'peach',
    'peru',
    'pink',
    'plum',
    'powder',
    'puff',
    'purple',
    'red',
    'rose',
    'rosy',
    'royal',
    'saddle',
    'salmon',
    'sandy',
    'seashell',
    'sienna',
    'sky',
    'slate',
    'smoke',
    'snow',
    'spring',
    'steel',
    'tan',
    'thistle',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'white',
    'yellow']



    if query_num == 1: 
        return {'date_range': random.randint(60,120)}

    elif query_num == 2:
        type = types_metal[random.randint(0, len(types_metal) - 1)]
        region = regions[random.randint(0, len(regions) - 1)]
        size = random.randint(1,50)
        return {'type': f"'{type}'",'region': f"'{region}'", 'size': size}
    
    elif query_num == 3:
        segment = segments[random.randint(0,len(segments) - 1)]
        dt = f"date('1995-03-{random.randint(1,31)}')"
        return {'segment': f"'{segment}'", 'date': dt}

    elif query_num == 4:
        year = random.randint(1993,1997)
        month = random.randint(1,12)
        dt_start = f"date('{year}-{month}-01')"
        dt_end = f"date('{year + ((month + 3) // 13)}-{(month + 3) % 13 + ((month + 3) // 13)}-01')"
        return {'start_date': dt_start, 'end_date': dt_end}
    
    elif query_num == 5:
        region = regions[random.randint(0, len(regions) - 1)]
        year = random.randint(1993,1997)
        dt_start = f"date('{year}-01-01')"
        dt_end = f"date('{year + 1}-01-01')"
        return {'start_date': dt_start, 'end_date': dt_end, 'region': f"'{region}'"}
    
    elif query_num == 6:
        discount = (2 + random.randint(0,7))/100
        quantity = 24 + random.randint(0,1)
        year = random.randint(1993,1997)
        dt_start = f"date('{year}-01-01')"
        dt_end = f"date('{year + 1}-01-01')"
        return {'start_date': dt_start, 'end_date': dt_end, 'discount': discount, 'quantity': quantity}
    
    elif query_num == 7:
        nation_1_position = random.randint(0, len(nations) - 1)
        nation_2_position = (nation_1_position + random.randint(1, len(nations) - 1)) % len(nations)
        nation_1 = nations[nation_1_position]
        nation_2 = nations[nation_2_position]
        return {'nation1' : f"'{nation_1}'", 'nation2': f"'{nation_2}'"}

    elif query_num == 8:
        nation_region_position = random.randint(0,len(nations) - 1)
        nation = nations[nation_region_position]
        region = regions_by_nation[nation_region_position]
        type = types_size[random.randint(0, len(types_size) - 1)] + ' ' + types_fabrication[random.randint(0, len(types_fabrication) - 1)] + ' ' + types_metal[random.randint(0, len(types_metal) - 1)]
        return {'type': f"'{type}'",'region': f"'{region}'", 'nation': f"'{nation}'"}

    elif query_num == 9:
        color = colors[random.randint(0, len(colors) - 1)]
        return {'color': f"'{color}'"}

    elif query_num == 10:
        year = random.randint(1993,1994)
        month = random.randint(2,13)
        dt_start = f"date('{year + (month // 13)}-{(month % 13) + ((month // 13))}-01')"
        dt_end = f"date('{year + ((month + 3) // 13)}-{((month + 3) % 13) + (((month + 3) // 13))}-01')"
        return {'start_date': dt_start, 'end_date': dt_end}

    elif query_num == 11:
        nation = nations[random.randint(0, len(nations) - 1)]
        return {'nation' : f"'{nation}'"}

    elif query_num == 12:
        mode_1_position = random.randint(0,len(modes) - 1)
        mode_2_position = (mode_1_position + random.randint(1, len(modes) - 1)) % len(modes)
        mode_1 = modes[mode_1_position]
        mode_2 = modes[mode_2_position]
        year = random.randint(1993,1997)
        dt_start = f"date('{year}-01-01')"
        dt_end = f"date('{year + 1}-01-01')"
        return {'start_date': dt_start, 'end_date': dt_end, 'mode1': f"'{mode_1}'", 'mode2': f"'{mode_2}'"}

    elif query_num == 13:
        words_1 = ['special', 'pending', 'unusual', 'express']
        words_2 = ['packages', 'requests', 'accounts', 'deposits']
        word_1 = words_1[random.randint(0, len(words_1) - 1)]
        word_2 = words_2[random.randint(0, len(words_2) - 1)]
        return {'word1' : f"'{word_1}'", 'word2': f"'{word_2}'"}

    elif query_num == 14:
        year = random.randint(1993,1997)
        month = random.randint(1,12)
        dt_start = f"date('{year}-{month}-01')"
        dt_end = f"date('{year + ((month + 1) // 13)}-{(month + 1) % 13 + ((month + 1) // 13)}-01')"
        return {'start_date': dt_start, 'end_date': dt_end}

    elif query_num == 15:
        year = random.randint(1993,1997)
        if year < 1997:
            month = random.randint(1,12)
        else:
            month = random.randint(1,10)
        dt_start = f"date('{year}-{month}-01')"
        dt_end = f"date('{year + ((month + 3) // 13)}-{((month + 3) % 13) + (((month + 3) // 13))}-01')"
        return {'start_date': dt_start, 'end_date': dt_end}      

    elif query_num == 16:
        brand = "Brand#" + f"{random.randint(1,5)}" + f"{random.randint(1,5)}"
        type = types_size[random.randint(0, len(types_size) - 1)] + ' ' + types_fabrication[random.randint(0, len(types_fabrication) - 1)]
        sizes_string = str(random.sample(range(1,51), 8))[1:-1]
        return {'brand': f"'{brand}'", 'type': f"'{type}'", 'sizes': sizes_string}

    elif query_num == 17:
        brand = "Brand#" + f"{random.randint(1,5)}" + f"{random.randint(1,5)}"
        container = container_sizes[random.randint(0, len(container_sizes) - 1)] + ' ' + container_packaging[random.randint(0, len(container_packaging) - 1)]
        return {'brand': f"'{brand}'", 'container': f"'{container}'"}

    elif query_num == 18:
        return {'quantity': 275 + random.randint(0,3)} # value changed from original TPC-H specifications 312 - 315 as for smaller scaling factors empty output otherwise

    elif query_num == 19:
        brand_1 = "Brand#" + f"{random.randint(1,5)}" + f"{random.randint(1,5)}"
        brand_2 = "Brand#" + f"{random.randint(1,5)}" + f"{random.randint(1,5)}"
        brand_3 = "Brand#" + f"{random.randint(1,5)}" + f"{random.randint(1,5)}"
        quantity_1 = random.randint(1,10)
        quantity_2 = random.randint(10,20)
        quantity_3 = random.randint(20,30)
        return {'brand1': f"'{brand_1}'", 'brand2': f"'{brand_2}'", 'brand3': f"'{brand_3}'", 'quantity1': quantity_1, 'quantity2': quantity_2, 'quantity3': quantity_3}

    elif query_num == 20:
        color = colors[random.randint(0, len(colors) - 1)]
        nation = nations[random.randint(0, len(nations) - 1)]
        year = random.randint(1993,1997)
        dt_start = f"date('{year}-01-01')"
        dt_end = f"date('{year + 1}-01-01')"
        return {'color': f"'{color}'", 'nation' : f"'{nation}'", 'start_date': dt_start, 'end_date': dt_end}

    elif query_num == 21:
        nation = nations[random.randint(0, len(nations) - 1)]
        return {'nation' : f"'{nation}'"}
    
    elif query_num == 22:
        phone_country_code_string = str([f'{code}' for code in random.sample(range(10,35), 7)])[1:-1]
        return {'phone_string': phone_country_code_string}
    
    else: # can be removed after all other cases covered
        return {}




##### Delete below




# Auxiliary Functions

def next_random(seed):
    """Simulate TPC-H LCG random number generator."""
    # Use 31-bit linear congruential generator like TPC-H
    return (seed * 16807) % 2147483647

def random_number(min_val, max_val, seed):
    """Uniform random integer in [min_val, max_val]."""
    # Advance the seed (TPC-H uses deterministic seed)
    seed = next_random(seed)
    return min_val + (seed % (max_val - min_val + 1)), seed

def nurand(A, x, y, C, seed):
    """Non-uniform random number generator from TPC-H spec."""
    rand1, seed = random_number(0, A, seed)
    rand2, seed = random_number(x, y, seed)
    result = (((rand1 | rand2) + C) % (y - x + 1)) + x
    return result, seed

def random_date(start_year=1993, end_year=1997, seed=1):
    """Return a random date in the range [start_year-01-01, end_year-12-31]."""
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta_days = (end - start).days
    day_offset, seed = random_number(0, delta_days, seed)
    return start + timedelta(days=day_offset), seed


# TPC-H Parameter Ranges

# Constants from TPC-H specifications
DISCOUNT_RANGE = (2, 9)        # 0.02 - 0.09
QUANTITY_RANGE = (1, 50)       # 1 - 50
SHIPDATE_RANGE = (1993, 1997)  # For queries with date filters

# Example NURand constants from TPC-H (Section 4.2.2.13)
CUST_NURand_C = 65
ORD_NURand_C = 35
PART_NURand_C = 79

# -------------------------
# 3. Parameter Generation per Query
# -------------------------

def generate_query_parameters_alternative(query_num, stream=1, base_seed=1):
    """Generate TPC-H query parameters for a given query."""
    # Deterministic seed per query+stream
    seed = base_seed + query_num * 17 + stream * 23

    params = {}
    
    if query_num == 1:
        # Q1: no variable parameters (fixed query)
        params = {}
    
    elif query_num == 6:
        # Q6: Revenue Change Query
        shipdate, seed = random_date(*SHIPDATE_RANGE, seed)
        discount, seed = random_number(*DISCOUNT_RANGE, seed)
        quantity, seed = nurand(255, *QUANTITY_RANGE, PART_NURand_C, seed)

        params = {
            "shipdate": shipdate.strftime("%Y-%m-%d"),
            "discount": round(discount / 100.0, 2),
            "quantity": quantity
        }
    
    elif query_num in [3, 5, 7, 8, 10, 12, 18, 19]:
        # Example: Queries with random date + region/nation/part
        shipdate, seed = random_date(*SHIPDATE_RANGE, seed)
        params = {"shipdate": shipdate.strftime("%Y-%m-%d")}

    else:
        # Generic fallback: one numeric and one date param
        num, seed = random_number(1, 100, seed)
        d, seed = random_date(*SHIPDATE_RANGE, seed)
        params = {"num": num, "date": d.strftime("%Y-%m-%d")}

    return params
