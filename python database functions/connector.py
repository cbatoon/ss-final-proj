import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    port=8889,
    user="root",
    password="root"
    )

cursor = cnx.cursor()

def view_customer_data():
    cursor.execute("SELECT * FROM ss_final.Customers")
    results = cursor.fetchall()
    for row in results:
        print(row)

def view_censored_customer_names():
    cursor.execute("SELECT CONCAT(LEFT(customerFirst, 2), '***') AS customerFirst, CONCAT(LEFT(customerLast, 2), '****') AS customerLast FROM ss_final.Customers")
    results = cursor.fetchall()
    for row in results:
        print(row)

def view_censored_customer_data(cols_query):
    #Would probably have to make a loop that looks at the amount of columns in the query and then retrieves
    #the data from the database and compiles it into an actual row of data
    selected_row = []

    for col in cols_query:
        if col == 'SSN':
            selected_row.append(f"CONCAT('***-**-', RIGHT({col}, 4)) AS {col}")
        elif col == 'balance' or col == 'creditScore':
            selected_row.append(f"{col} AS {col}")
        elif col == 'bankNumR' or col == 'bankNumA':
            selected_row.append(f"CONCAT('*****', RIGHT({col}, 4)) AS {col}")
        else:
            selected_row.append(f"CONCAT(LEFT({col}, 2), '***') AS {col}")
        
    full_query = "SELECT " + ", ".join(selected_row) + " FROM ss_final.Customers"
    cursor.execute(full_query)
    results = cursor.fetchall()
    for row in results:
        print(row)

cols_query = ['customerFirst', 'customerLast', 'address', 'balance', 'creditScore', 'bankNumR', 'bankNumA', 'SSN']
#view_censored_customer_names()
view_censored_customer_data(cols_query)
