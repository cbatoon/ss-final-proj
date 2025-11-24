# connector.py
import mysql.connector

# Connect to your MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",       
    database="ss_final"  
)

cursor = cnx.cursor()

def view_censored_customer_data(cols_query):
    """
    Returns a list of dictionaries with censored customer data.
    Sensitive data (SSN, Bank numbers, Names) is partially hidden.
    """
    selected_row = []

    for col in cols_query:
        if col == 'SSN':
            # Show only last 4 digits
            selected_row.append(f"CONCAT('***-**-', RIGHT({col}, 4)) AS {col}")
        elif col in ['balance', 'creditScore']:
            # Keep numeric data as-is
            selected_row.append(f"{col} AS {col}")
        elif col in ['bankNumR', 'bankNumA']:
            # Show last 4 digits of bank numbers
            selected_row.append(f"CONCAT('*****', RIGHT({col}, 4)) AS {col}")
        else:
            # Show first 2 letters of names/addresses
            selected_row.append(f"CONCAT(LEFT({col}, 2), '***') AS {col}")

    full_query = "SELECT " + ", ".join(selected_row) + " FROM Customers"
    cursor.execute(full_query)
    results = cursor.fetchall()

    # Convert tuples to dicts for JSON
    final_results = []
    for row in results:
        final_results.append({cols_query[i]: row[i] for i in range(len(cols_query))})

    return final_results
