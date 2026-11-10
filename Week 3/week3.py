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


# # Task 1

# # Create a list of every order's total_cost(as numbers).
# cost = []   # this creates an empty list

# # - Find the total spend and the average order value
# # first create an iteration to convert total_cost to float and then create a list
# for row in rows:
#     cost_val = float(row['total_cost']) # this changes total_cost to float and saves it in cost_val
#     cost.append(cost_val) # this populates the list (cost) created earlier with the float value of total_cost


# total_spend = sum(cost) # calculate total spend using inbuilt function
# average_order_value = total_spend / len(cost) # total spend is divided by the number of variables in cost (len(cost))

# print(f'Total Spend: {total_spend}')
# print(f'Average Order Value: {average_order_value}')

# # - Sort the lit and find the median
# sorted_cost = sorted(cost) # this sorts the cost list created earlier
# n = len(sorted_cost) # this counts the number of variables in cost

# print(sorted_cost[:5]) # prints 0,1,2,3,4 from the cost list
# print(n) # prints the total number of variables

# # Find the median

# mid = n // 2 # this calculates the position of the middle variable
# print(mid) 

# if n % 2 == 0: # checks if the total number of varibles in the list is even
#     median = (sorted_cost[mid - 1] + sorted_cost[mid]) / 2 # after confirming if list is even
#     # this calculates the median value (mid -1 + mid) divided by 2
# else:
#     median = sorted_cost[mid] # if n % 2 == 0 is odd, median is one variable and it returns
#     # the variable

# print(f'Median: {median}') # prints the median

# # Print the five smallest and largest orders

# # since the cost is sorted, it is now arranged from the smallest to the largest
# print(f'Five smallest orders: {sorted_cost[:5]}') # prints the first 5 indexes 0,1,2,3,4
# print(f'Five largest orders: {sorted_cost[-5:]}') # prints the last 5 indexes -1,-2,-3,-4,-5

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