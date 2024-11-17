
"""
Purpose:
* Core application file for running the Flask app.
* Manages routing, rendering templates, and handling data requests for visualization.

How it work :
* Sets up a Flask app.
* Connects to a PostgreSQL database using the Database_connection function from Processing_funs.py.
* Specifies PostgreSQL credentials (dbname, user, password, etc.).
* Connection is established via the Database_connection function.
* Renders index.html with a welcome message.
* then with each Button clicked you get the Table equivalent to the processing algorithm .
    * View_Profit, View_Exceptional_charges, View_profitability_analysis, etc.
    * Each route calculates specific metrics using functions from Processing_funs.py, 
        converts the result into an HTML table, and renders it using table.html.

        
"""








from flask import Flask, render_template
from waitress import serve 
import pandas as pd
from Processing_funs import *
import time

app = Flask(__name__)
db_config = {
    'dbname': 'postgres',
    'user': 'admin',
    'password': 'admin',
    'host': 'postgres',  
    'port': '5432'  
}


# This code section begin with Start and end with END , is a way to verify database connection every 5 sec ,and if it's still refuse to connect for 50s it exit the program
#Start
database_statue=False
i=0
while ( database_statue == False and i<10) :
    
    db_cursor=Database_connection(db_config)
    if  db_cursor !=None :   
        print('Database Connected!!!')
        database_statue=True
    else:
        print('Try...number=',i+1)
        time.sleep(5)
        i+=1
        continue
print('database_statue:',database_statue)

# END






@app.route('/')
def home():
    return render_template('index.html', message='Welcome to Flask!')
import os
"""
This route return  the dashboard.html template that itself show our dashboard.pdf inside of it .

"""

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

"""
This view return a sample of the data 50 exactly and it send them as tables in html form .

"""



@app.route("/Sample_data")
def View_Sample_data():

    df_sample_data=Fetech_sample(db_cursor)
    table_html=df_sample_data.to_html(classes="table table-striped", index=False)
    return render_template("table.html", title="Sample Data 50 Row", table=table_html) # Uses Pandas’ .to_html() method to generate table HTML.




"""
All the routes that start with 'View_' work similarly 
they call the specific analytical function then convert the table returned into table of html form 
and finally send that table into a table.html template .  

"""



@app.route("/View_Profit")
def View_Profit():

    df_profit=Calcule_Profit(db_cursor)
    table_html=df_profit.to_html(classes="table table-striped", index=False)
    return render_template("table.html", title="Profit GroupedBy each Year", table=table_html) # Uses Pandas’ .to_html() method to generate table HTML.



@app.route("/View_Exceptional_charges")
def View_Exceptional_charges_Groupby_year():

    df_profit=Calculate_Exceptional_charges_Groupby_year(db_cursor)
    table_html=df_profit.to_html(classes="table table-striped", index=False)
    return render_template("table.html", title="Profit GroupedBy each Year", table=table_html)


@app.route("/View_Calcul_profitability_analysis")
def View_profitability_analysis_Groupby_year():

    df_profit=Calcul_profitability_analysis(db_cursor)
    table_html=df_profit.to_html(classes="table table-striped", index=False)
    return render_template("table.html", title="Profit GroupedBy each Year", table=table_html)



@app.route("/View_Calcul_Expense_per_categorie")
def View_Calcul_Expense_per_categorie():

    df_profit=Calcul_Expense_per_categorie(db_cursor)
    table_html=df_profit.to_html(classes="table table-striped", index=False)
    return render_template("table.html", title="Cost/Expense per categorie groupedby Year", table=table_html)





@app.route("/View_Return_on_investiment_per_year")
def View_Return_on_investiment_per_year():

    df_profit=Return_on_investiment_per_year(db_cursor)
    table_html=df_profit.to_html(classes="table table-striped", index=False)
    return render_template("table.html", title="Return on investiment per year", table=table_html)








if __name__ == '__main__':

    serve(app, host="0.0.0.0", port=8080) # Production-Ready Server: Uses Waitress to deploy the app in a production-like environment.


