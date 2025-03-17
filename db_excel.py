from openpyxl import Workbook

# Sample dictionary containing table details
tables_info = {
    "users": (
        "CREATE TABLE users (id INT, name VARCHAR(100), email VARCHAR(200));",
        ["id", "name", "email"]
    ),
    "orders": (
        "CREATE TABLE orders (order_id INT, user_id INT, amount DECIMAL(10,2));",
        ["order_id", "user_id", "amount"]
    ),
    "products": (
        "CREATE TABLE products (product_id INT, name VARCHAR(100), price DECIMAL(10,2));",
        ["product_id", "name", "price"]
    ),
}

# Create a new Excel workbook
wb = Workbook()
wb.remove(wb.active)  # Remove default sheet

# Iterate through tables and add them as separate sheets
for table_name, (sql_definition, columns) in tables_info.items():
    ws = wb.create_sheet(title=table_name)  # Create a sheet with the table name

    # Write SQL definition in the first row
    ws.append([sql_definition])

    # Write column names below
    for column in columns:
        ws.append([column])

# Save the Excel file
output_file = "database_structure.xlsx"
wb.save(output_file)

print(f"Excel file '{output_file}' created successfully.")
