import csv
from datetime import datetime, date

with open("supply_chain_dataset.csv", newline="", encoding= "utf-8") as file:
    reader = csv.DictReader(file)
    columns = reader.fieldnames
    rows = list(reader)

def parse_date(text):
    if "/" in text:
        return datetime.strptime(text, "%m/%d/%Y").date()
    return date.fromisoformat(text)

# Task 1: Assess Data Quality
# 1. Missing values: Count the empty cells in each column.

missing_counts = {col: 0 for col in columns}
for row in rows:
    for col, val in row.items():
        if val is None or val.strip() == "":
            missing_counts[col] += 1

print("1. Missing values:", missing_counts)

# 2. Duplicates: Count rows that are exact copies of an earlier row.

seen_rows = set()
duplicate_count = 0
for row in rows:
    row_tuple = tuple(row.values())
    if row_tuple in seen_rows:
        duplicate_count += 1
    else:
        seen_rows.add(row_tuple)

print("2. Exact duplicate rows:", duplicate_count)

# 3. Text inconnsistencies: print the distinct values of supplier_name,
# warehouse_destination, delivery_status and product_category. Count the
# categories that have extra spaces.

text_cols = ["supplier_name", "warehouse_destination", "delivery_status", "product_category"]
distinct_vals = {col: set() for col in text_cols}
categories_with_spaces = set()

for row in rows:
    for col in text_cols:
        distinct_vals[col].add(row[col])

        cat = row["product_category"]
        if cat != cat.strip():
            categories_with_spaces.add(cat)

print("3. Distinct text values:")
for col, vals in distinct_vals.items():
    print(f" {col}: {sorted(vals)}")
print("  Categories with extra spaces:", len(categories_with_spaces), categories_with_spaces)

# 4. Date formats: count how many order_date and delivery_date values use each format.

date_formats = {
    "order_date": {"slash (MM/DD/YYYY)": 0, "iso (YYYY-MM-DD)": 0, "empty": 0},
    "delivery_date": {"slash (MM/DD/YYYY)": 0, "iso (YYYY-MM-DD)": 0, "empty": 0}
}

for row in rows:
    for col in ["order_date", "delivery_date"]:
        val = row[col].strip()
        if not val:
            date_formats[col]["empty"] += 1
        elif "/" in val:
            date_formats[col]["slash (MM/DD/YYYY)"] += 1
        else:
            date_formats[col]["iso (YYYY-MM-DD)"] += 1

print("4. Date formats:", date_formats)

# Task 2: Logical Checks

checks = {
    "zero_or_negative_cost": [],
    "cost_mismatch": [],
    "delivery_before_order": [],
    "delivery_days_mismatch": [],
    "on_time_disagreement": []
}

undelivered_statuses = {"cancelled", "In-Transit", "Pending", "Pendng"}
skipped_orders = 0

for row in rows:
    order_id = row["order_id"].strip()

    if row["total_cost"].strip() and row["quantity"].strip() and row["unit_price"].strip():
        total_cost = float(row["total_cost"])
        qty = float(row["quantity"])
        unit_price = float(row["unit_price"])

        if total_cost <= 0:
            checks["zero_or_negative_cost"].append(order_id)

        if abs(total_cost - (qty * unit_price)) > 1:
            checks["cost_mismatch"].append(order_id)

    status = row["delivery_status"].strip()
    if status in undelivered_statuses:
        skipped_orders += 1
        continue

    if row["order_date"].strip() and row["delivery_date"].strip():
        o_date = parse_date(row["order_date"])
        d_date = parse_date(row["delivery_date"])

        if d_date < o_date:
            checks["delivery_before_order"].append(order_id)

        if row["actual_delivery_days"].strip():
            actual_days = int(float(row["actual_delivery_days"]))
            expected_days = (d_date - o_date).days

            if actual_days != expected_days:
                checks["delivery_days_mismatch"].append(order_id)

            if row["lead_time_days"].strip() and row["on_time"].strip():
                lead_days = int(float(row["lead_time_days"]))
                on_time = row["on_time"].strip()

                if(on_time == "Yes" and actual_days > lead_days) or (on_time == "No" and actual_days <= lead_days):
                    checks["on_time_disagreement"].append(order_id)

print(f"Skipped undelivered orders: {skipped_orders}\n")
for check_name, failed_ids in checks.items():
    print(f"{check_name}: {len(failed_ids)} rows failed | Examples: {failed_ids[:5]}")


# Task 3: Standardise and Save
cleaned_rows = []
changes_per_col = {col: 0 for col in columns}

for row in rows:
    new_row = {}
    for col in columns:
        orig_val = row[col]
        val = orig_val.strip() if orig_val is not None else ""
        
        if val != "":
            # 1. Supplier names: SpplierA, ..., SupplierE
            if col == "supplier_name":
                clean_sup = val.replace("_", "").replace(" ", "").lower()
                if clean_sup.startswith("supplier") and len(clean_sup) == 9:
                    val = "Supplier" + clean_sup[-1].upper()
            
            # 2. Warehouses: Warehouse_1, ..., Warehouse_6
            elif col == "warehouse_destination":
                num = val.replace("Warehouse", "").replace("WH", "").replace("_", "").strip()
                if num.isdigit():
                    val = f"Warehouse_{num}"

            # 3. Fix status typos
            elif col == "delivery_status":
                typo_map = {
                    "Delievered": "Delivered",
                    "Pendng": "Pending"
                }
                val = typo_map.get(val, val)

            # 4. Standardise dates to YYYY-MM-DD
            elif col in ["order_date", "delivery_date"]:
                val = parse_date(val).isoformat()

        # Track if anything changed compared to the original cell
        if val != orig_val:
            changes_per_col[col] += 1

        new_row[col] = val
    cleaned_rows.append(new_row)

print("Values changed per column:", changes_per_col)

# Save to supply_chain_stabdardised.csv
with open("supply_chain_standardised.csv", "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=columns)
    writer.writeheader()
    writer.writerows(cleaned_rows)

# Reload and verify distinct values
with open("supply_chain_standardised.csv", newline ="", encoding= "utf-8") as verify_file:
    reloaded_rows = list(csv.DictReader(verify_file))

print("Verification after reload:")
for col in ["supplier_name", "warehouse_destination", "delivery_status", "product_category"]:
    unique_clean = sorted({r[col] for r in reloaded_rows})
    print(f"    {col}: {unique_clean}")


