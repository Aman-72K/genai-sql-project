import sqlite3
import pandas as pd

# 1. Define the Data
products_data = {
    'product_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'product_name': ['Espresso', 'Latte', 'Cappuccino', 'Cold Brew', 'Matcha Latte', 
                    'Blueberry Muffin', 'Avocado Toast', 'Butter Croissant', 'Bagel', 'Breakfast Burrito'],
    'category': ['Beverage', 'Beverage', 'Beverage', 'Beverage', 'Beverage', 'Food', 'Food', 'Food', 'Food', 'Food'],
    'unit_price': [3.00, 4.75, 4.50, 5.50, 5.75, 3.75, 9.50, 4.25, 5.25, 8.50]
}

inventory_data = {
    'inventory_id': range(1, 11),
    'product_id': [101, 102, 106, 107, 108, 110, 104, 105, 109, 103],
    'stock_level': [50, 40, 12, 8, 15, 10, 25, 18, 20, 30],
    'reorder_point': [10, 15, 5, 4, 5, 3, 8, 5, 6, 10]
}

sales_data = {
    'transaction_id': [5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008, 5009, 5010, 5011, 5012],
    'product_id': [102, 107, 104, 106, 103, 101, 108, 102, 109, 110, 105, 101],
    'quantity': [1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 1, 2],
    'payment_method': ['Credit Card', 'Apple Pay', 'Credit Card', 'Cash', 'Credit Card', 'Cash', 
                       'Credit Card', 'Apple Pay', 'Credit Card', 'Cash', 'Credit Card', 'Credit Card']
}

# 2. Convert to DataFrames
df_products = pd.DataFrame(products_data)
df_inventory = pd.DataFrame(inventory_data)
df_sales = pd.DataFrame(sales_data)

# 3. Connect to SQLite and Load Data
conn = sqlite3.connect('cafe_business.db')

df_products.to_sql('coffee_products', conn, if_exists='replace', index=False)
df_inventory.to_sql('inventory_status', conn, if_exists='replace', index=False)
df_sales.to_sql('daily_sales', conn, if_exists='replace', index=False)

print("Database 'cafe_business.db' created successfully with 3 tables.")

# 4. Verification: Run a JOIN Query
query = """
SELECT 
    s.transaction_id, 
    p.product_name, 
    s.quantity, 
    (s.quantity * p.unit_price) AS total_revenue
FROM daily_sales s
JOIN coffee_products p ON s.product_id = p.product_id
LIMIT 5;
"""

print("\nSample Join Analysis (Sales + Products):")
print(pd.read_sql(query, conn))

conn.close()