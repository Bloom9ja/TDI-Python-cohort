import csv

with open ('supply_chain_dataset.csv', newline='') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

def clean_supplier(name):
    """ 'Supplier A', 'suppliera', 'SupplierA' -> 'SuplierA' """
    compact = name.strip().lower().replace(" ", "")
    return 'Supplier' + compact[-1].upper()

def clean_category(category):
    """ ' Motors ' -> 'Motors' """
    return category.strip()


# Task 1

# Create a list of every order's total_cost(as numbers).
cost = []   # this creates an empty list

# - Find the total spend and the average order value
# first create an iteration to convert total_cost to float and then create a list
for row in rows:
    cost_val = float(row['total_cost']) # this changes total_cost to float and saves it in cost_val
    cost.append(cost_val) # this populates the list (cost) created earlier with the float value of total_cost


total_spend = sum(cost) # calculate total spend using inbuilt function
average_order_value = total_spend / len(cost) # total spend is divided by the number of variables in cost (len(cost))

print(f'Total Spend: {total_spend}')
print(f'Average Order Value: {average_order_value}')

# - Sort the lit and find the median
sorted_cost = sorted(cost) # this sorts the cost list created earlier
n = len(sorted_cost) # this counts the number of variables in cost

print(sorted_cost[:5]) # prints 0,1,2,3,4 from the cost list
print(n) # prints the total number of variables

# Find the median

mid = n // 2 # this calculates the position of the middle variable
print(mid) 

if n % 2 == 0: # checks if the total number of varibles in the list is even
    median = (sorted_cost[mid - 1] + sorted_cost[mid]) / 2 # after confirming if list is even
    # this calculates the median value (mid -1 + mid) divided by 2
else:
    median = sorted_cost[mid] # if n % 2 == 0 is odd, median is one variable and it returns
    # the variable

print(f'Median: {median}') # prints the median

# Print the five smallest and largest orders

# since the cost is sorted, it is now arranged from the smallest to the largest
print(f'Five smallest orders: {sorted_cost[:5]}') # prints the first 5 indexes 0,1,2,3,4
print(f'Five largest orders: {sorted_cost[-5:]}') # prints the last 5 indexes -1,-2,-3,-4,-5

# Task 2

category_suppliers = {} # this creates an empty dictionary

for row in rows: # this goes through each row in the csv file one by one
    category = clean_category(row['product_category']) # this cleans the variables in the
    #column product_category using the function created above
    supplier = clean_supplier(row['supplier_name']) # this uses the function created above to
    # clean and unify the supplier names

    if category not in category_suppliers: # this verifies if a category already as a key
        #in the dictionary
        category_suppliers[category] = set() # creates a new set as category value for the key

    category_suppliers[category].add(supplier) # adde the supplier name to the category it belongs to

# Print each category with its suppliers
for cat, suppliers in category_suppliers.items(): # looks through the values in the dictionary
    print(f'{cat}: {suppliers}') # prints the category and the suppliers

# Look up who supplies "Pumps"
if 'Pumps' in category_suppliers: # Look for Pumps in the dictionary
    print(f'\nSuppliers for Pumps: {category_suppliers['Pumps']}') # prints the suppliers associated with Pumps

# Count how many unique suppliers there are
unique_suppliers = set() # creates an empty set
for suppliers in category_suppliers.values(): # looks through the values in the dictionary
    # and takes just the suppliers
    unique_suppliers.update(suppliers) # takes the values and brings them to a new set

print(f'Unique Suppliers: {len(unique_suppliers)}') # calculates the number of variables in
# unique suppliers and gives the answer

# Task 3

# Find Unique Values with Sets

raw_suppliers = set() #creates an empty set to store uncleaned supplier name
clean_suppliers = set() # creates an empty set to store cleaned supplier name

raw_categories = set() # creates an empty set to store uncleaned product categories
clean_categories = set() # creates an empty set to store cleaned product categories

delivery_statuses = set() # creates empty set to store unique delivery status

for row in rows:
    raw_suppliers.add(row['supplier_name']) # adds the uncleaned supplier names and add to a set
    raw_categories.add(row['product_category']) # adds the uncleaned product categories and add to a set

    clean_suppliers.add(clean_supplier(row['supplier_name'])) # adds the cleaned supplier names and add to a set
    clean_categories.add(clean_category(row['product_category'])) # adds the cleaned product categories and add to a set

    delivery_statuses.add(row['delivery_status']) # gets the delivery status from the row and adds it

print(f'Suppliers - Raw: {len(raw_suppliers)} | {len(clean_suppliers)}') # uses len to compare number of unique values before and after cleaning
print(f'Categories - Raw: {len(raw_categories)} | {len(clean_categories)}') # uses len to compare number of unique values before and after cleaning

print(delivery_statuses)

motors_suppliers = category_suppliers.get('Motors', set()) # retrieves the set of suppliers that provide motors
pumps_suppliers = category_suppliers.get('Pumps', set()) # safely retrieves the set of suppliers that provide pumps

# Both motors and pumps
both_motors_and_pumps = motors_suppliers & pumps_suppliers # uses set intersection operator to find suppliers that appear in both sets
print(f'Suppliers for  Both Motors and Pumps: {both_motors_and_pumps}') # prints the result of both

# Either Motors or Pumps
either_motors_or_pumps = motors_suppliers | pumps_suppliers 
print(f'Suppliers for Either Motors or Pumps: {either_motors_or_pumps}') # prints the result of the union of both sets

# Motors But Not Pumps
motors_not_pumps = motors_suppliers - pumps_suppliers
print(f'Suppliers for Motors But Not Pumps: {motors_not_pumps}') # prints the result of suppliers that provide motors but removes pumps

# Task 4

single_source_count = 0
total_categories = len(category_suppliers)

for category, suppliers in category_suppliers.items():
    if len(suppliers) == 1:
        supplier_name = list(suppliers)[0]
        print(f'RISK: "{category}" depends on only one supplier: {supplier_name}')
        single_source_count += 1

print(f'\n{single_source_count} of {total_categories} categories are single-source.')

# Task 5

network = {}

for row in rows:
    supplier = clean_supplier(row['supplier_name'])
    category = clean_category(row['product_category'])
    cost = float(row['total_cost'])

    if supplier not in network:
        network[supplier] = {
            'categories': set(),
            'order_count': 0,
            'total_spend': 0.0
        }

    network[supplier]['categories'].add(category)
    network[supplier]['order_count'] += 1
    network[supplier]['total_spend'] += cost

target_supplier = 'SupplierA'
if target_supplier in network:
    print(network[target_supplier])
else:
    print(f"Supplier '{target_supplier}' not founf in network.")

for supp, data in network.items():
    print(f'''Supplier: {supp} | Orders: {data['order_count']} 
          | Categories Supplied: {len(data['categories'])} 
          | Total Spend: ${data['total_spend']:,.2f}''')

# Challenge 1

high_value_orders = []

for row in rows:
    cost = float(row['total_cost'])
    if cost > 100000:
        high_value_orders.append(cost)

total_orders = len(rows)
count_high_value = len(high_value_orders)

if total_orders > 0:
    percentage = (count_high_value / total_orders) * 100
else:
    percentage = 0.0

print(f'Number of orders above 100,000: {count_high_value}')
print(f'Total number of orders: {total_orders}')
print(f'Percentage of high-value orders: {percentage:.2f}%')

# Challenge 2

max_categories_count = 0
top_supplier = None

for supplier, data in network.items():
    category_count = len(data['categories'])

    if category_count > max_categories_count:
        max_categories_count = category_count
        top_supplier = supplier

print(f'Supplier with the most categories: {top_supplier}')
print(f'Number of categories provided: {max_categories_count}')
print(f'Categories supplied: {network[top_supplier]['categories']}')

# Challenge 3

status_costs = {}

for row in rows:
    status = row['delivery_status'].strip()
    cost = float(row['total_cost'])

    if status not in status_costs:
        status_costs[status] = []

    status_costs[status].append(cost)

for status, costs in status_costs.items():
    print(f"""Status: '{status}' | Total Orders: {len(costs)} 
          | Total Value: ${sum(costs):,.2f}""")

    target_status = 'Delivered'

    if target_status in status_costs:
        delivered_costs = status_costs[target_status]
        avg_delivered_value = sum(delivered_costs) / len(delivered_costs)

        print(f"\nAverage value of a '{target_status}' order: ${avg_delivered_value:,.2f}")
    else:
        print(f"\nStatus '{target_status}' not found in dataset.")