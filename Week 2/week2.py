# TASK 1

def approval_message(order_value):
    if order_value > 100000:
        return("Needs Manager Approval")
    elif order_value > 50000:
            return("Needs Supervisor Approval")
    else:
            return("Auto-approved")

print(f'Test Order Value: 72500 - {approval_message(72500)}')

# TASK 2

order_values = [12000, 55000, 150000, 49999, 100001, 8000]

for values in order_values:
    message = approval_message(values)
    print(f'Approval message: {values} - {message}')


# TASK 3

def check_supplier_status(supplier_name, on_time_rate):
    if on_time_rate >= 0.90:
        status = 'Reliable'
    elif on_time_rate >= 0.80:
        status = 'Monitor'
    else:
        status = 'At Risk'
    return f'{supplier_name} : {status}'

print(check_supplier_status('Suppliera', 0.94))
print(check_supplier_status('SupplierB', 0.86))
print(check_supplier_status('SupplierE', 0.74))

# TASK 4

import csv

with open('supply_chain_dataset.csv', newline='') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print('Column names:', rows[0].keys())
print('Number of data rows:', len(rows))
print(rows[5])

#TASK 5

Number_of_rows = len(rows)
unique_suppliers = set()
highest_cost = 0.0
lowest_cost = float('inf')
delivered_count = 0


for row in rows:
    unique_suppliers.add(row['supplier_name'])

    cost = float(row['total_cost'])

    if cost > highest_cost:
        highest_cost = cost

    if cost < lowest_cost:
        lowest_cost = cost

    if row['delivery_status'] == 'Delivered':
        delivered_count += 1

print(f'''
1. Number of rows= {Number_of_rows}
2. Unique suppliers = {unique_suppliers}
3. Highest Total Cost = {highest_cost}
4. Lowest Total Cost = {lowest_cost}
5. Count of delivered = {delivered_count}''')

# Challenge 1

def advanced_approval(order_value, on_time_rate):
    if order_value > 100000 and on_time_rate < 0.80:
        return 'Rejected: High Value from High Risk Supplier'
    elif order_value > 100000:
        return 'Needs Manager Approval'
    else:
        return 'Auto-approved'

print(advanced_approval(120000, 0.75))
print(advanced_approval(45000, 0.95))

# Challenge 2 & 3

# USED AI pending correction class

def clean_supplier(name):
    ''' 'Supplier A', 'suppliera', 'SupplierA' -> 'SupplierA' '''
    compact = name.strip().lower().replace(' ', '')
    return 'Supplier' + compact[-1].upper()

def clean_category(category):
    """ ' Motors ' -> 'Motors' """
    return category.strip()

supplier_a_count = 0
supplier_a_total_cost = 0.0
gap_tracker = {}

for row in rows:
    raw_name = row['supplier_name']
    clean_name = clean_supplier(raw_name)

    raw_cat = row['product_category']
    clean_cat = clean_category(raw_cat)

if clean_name == 'SupplierA':
    supplier_a_count += 1
    supplier_a_total_cost += float(row['total_cost'])

for column, value in row.items():
    if value == '':
        if column not in gap_tracker:
            gap_tracker[column] = 0
        gap_tracker[column] += 1

print(f'Total Orders: {supplier_a_count}')
print(f'Total COst: ${supplier_a_total_cost:,.2f}\n')

for column. count in gap_tracker.items():
    print(f"Column '{column}' has {count} empty gap(s)")