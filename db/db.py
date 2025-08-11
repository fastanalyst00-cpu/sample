import os
import pandas as pd
import sqlite3

# Ensure 'db' folder exists
os.makedirs('db', exist_ok=True)

# Load your existing data
excel_path = 'db/samplesssss.xlsx'
df = pd.read_excel(excel_path, dtype=str)  # Force everything as string, including PICK UP DATE

# Path to the database file inside 'db' folder
db_path = 'db/main.db'

# Connect to SQLite database
conn = sqlite3.connect(db_path)

# Write the DataFrame to a table named 'bookings_tbl'
try:
    df.to_sql('bookings_tbl', conn, if_exists='replace', index=False)
    print("✅ Database created and data inserted successfully.")
except Exception as e:
    print(f"❌ Error inserting data: {e}")
finally:
    conn.close()
