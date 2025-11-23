from flask import Flask, render_template
import mysql.connector

#creates the connection to the mysql database

#must be a function that is initialized in EVERY page function, and not globally
#because if one function closes the global function, it is closed for ALL OTHER pages
def create_conn():
    conn = mysql.connector.connect(
        #CHANGE INFORMATION HERE FOR PRIVATE TESTING ON PERSONAL DATABASE
        host="localhost",
        port=8889,
        user="root",
        password="root",
        database='ss_final'
    )
    return conn


def create_app():
    #flask database information
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0HMhvC85qeiP9oDoovGDJbLwuAbGJYKA'
    # from .views import views
    # from .auth import auth
    return app

#creates appa
app = create_app()



@app.route('/')
#route for base page that shows the raw data from database
def base():

    #create the local connection
    conn = create_conn()

    #creates the interactant that allows for queries to be made to a certain database
    mycursor = conn.cursor(dictionary=True)

    #runs the query
    mycursor.execute("SELECT * FROM Customers")

    #stores the fetched results in a variable
    results = mycursor.fetchall()

    #closes the interactant variable and the connection
    mycursor.close()
    conn.close()

    #returns the results to the render template that renders the data on the specified webpage
    return render_template("base.html", results = results)

@app.route('/censored')
def cenx():

    #create the local connection
    conn = create_conn()

    #creates the interactant that allows for queries to be made to a certain database
    mycursor = conn.cursor(dictionary=True)

    #creates an array of a row of customer data that has been censored
    selected_row = []

    #a list of columns that have been selected for censorship AND printing
    cols_query = ['customerFirst', 'customerLast', 'address', 'balance', 'creditScore', 'bankNumR', 'bankNumA', 'SSN']

    #a function that censors as many columns in the cols_query and has specific handling for each type of data
    for col in cols_query:
        if col == 'SSN':
            selected_row.append(f"CONCAT('***-**-', RIGHT({col}, 4)) AS {col}")
        elif col == 'balance' or col == 'creditScore':
            selected_row.append(f"{col} AS {col}")
        elif col == 'bankNumR' or col == 'bankNumA':
            selected_row.append(f"CONCAT('*****', RIGHT({col}, 4)) AS {col}")
        else:
            selected_row.append(f"CONCAT(LEFT({col}, 2), '***') AS {col}")
    
    #gets the full query
    full_query = "SELECT " + ", ".join(selected_row) + " FROM ss_final.Customers"
    mycursor.execute(full_query)
    results = mycursor.fetchall()
    return render_template("cenx.html", results = results)

#Debugger
if __name__ == '__main__':
    app.run(debug=True)