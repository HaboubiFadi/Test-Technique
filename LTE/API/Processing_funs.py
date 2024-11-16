"""
Purpose:
    * The purpose of these functions is to perform analytical computations on financial data stored in a PostgreSQL database. 
        They retrieve and process data to produce meaningful insights, such as profit calculations, 
        exceptional charges analysis, profitability analysis, expense categorization, and return on investment. 
        These insights are structured into pandas.DataFrame objects for further visualization or reporting.

These functions are central to enabling efficient and automated data analysis for business decision-making.

How They Work:

    * Each function executes a SQL query.
    * The results are fetched and converted into a Pandas DataFrame.
    * DataFrames are returned to app.py for rendering.
"""


import psycopg2
import pandas as pd




def Database_connection(db_config):
    try:
        conn = psycopg2.connect(**db_config) # Establishes a connection to PostgreSQL.

        cursor = conn.cursor()
        return cursor # Returns a cursor for executing queries.
    except Exception as e :
        print('Error Occured ',e)
        return None
    


'''
    Documentation : 
Calcule_Profit:
    * Calculates yearly profit by subtracting charges from products.
    * Groups by exercice_comptable (accounting year) for aggregation.

'''    

def Calcule_Profit(cursor):
    query=""" SELECT exercice_comptable,
    SUM(CASE WHEN produit_charge = 'PRODUITS' and montant_en_eur >= 0 THEN montant_en_eur ELSE 0 END) -
    SUM(CASE WHEN produit_charge = 'CHARGES' and montant_en_eur >= 0 THEN montant_en_eur ELSE 0 END) AS profit
        FROM 
    public.compte_resultat 
    GROUP BY 
    exercice_comptable
    ORDER BY 
    exercice_comptable;
"""
    cursor.execute(query)
    print("Selecting Profit (produit-charge) grouped by Year(exercice_comptable) from compte_resultat")
    profit_table = cursor.fetchall()
    profit_dataframe=pd.DataFrame(profit_table,columns=["Year","Profit"])
    return profit_dataframe


'''
    Documentation : 
Calculate_Exceptional_charges_Groupby_year:

    * Filters exceptional charges (type_de_resultat = 'EXCEPTIONNEL').
    * Aggregates charges by year.

'''




def Calculate_Exceptional_charges_Groupby_year(cursor):
    query=""" SELECT exercice_comptable,type_de_resultat,produit_charge,montant_en_eur from public.compte_resultat 

"""    
    cursor.execute(query)

    Exceptional_table = cursor.fetchall()
    df=pd.DataFrame(Exceptional_table,columns=["exercice_comptable","type_de_resultat","produit_charge","montant_en_eur"])
    exceptional_charges = (
    df[(df['type_de_resultat'] == 'EXCEPTIONNEL') & (df['produit_charge'] == 'CHARGES')]
    .groupby('exercice_comptable')['montant_en_eur']
    .sum()
    .reset_index(name='exceptional_charges')
)
    print(exceptional_charges)
    return exceptional_charges

'''
    Documentation : 
Calcul_profitability_analysis:

    * Computes profitability based on core Business products and costs (type_de_resultat = 'EXPLOITATION').

'''




def Calcul_profitability_analysis(cursor):
    query=""" SELECT exercice_comptable AS year,
    SUM(CASE WHEN produit_charge = 'PRODUITS' and montant_en_eur >= 0 THEN montant_en_eur ELSE 0 END) as Core_profit,
    SUM(CASE WHEN produit_charge = 'CHARGES' and montant_en_eur >= 0 THEN montant_en_eur ELSE 0 END) as Core_cost
        FROM 
    public.compte_resultat 
    where type_de_resultat ='EXPLOITATION'
    GROUP BY 
    exercice_comptable
    ORDER BY 
    exercice_comptable;
    """
    cursor.execute(query)

    profitability_table = cursor.fetchall()
    profitability_table_df=pd.DataFrame(profitability_table,columns=["year","Core_profit","Core_cost"])
    print(profitability_table_df)
    return profitability_table_df  





'''
    Documentation : 
Calcul_Expense_per_categorie:

    * Aggregates expenses (produit_charge = 'CHARGES') by category (poste) and year.

'''




def Calcul_Expense_per_categorie(cursor): # Categorie here mean the variable 'poste' in the Database
    query=""" SELECT 
    exercice_comptable As year, 
    poste AS category,
    Sum(montant_en_eur) As Expense_EUR
    FROM 
        public.compte_resultat  
    where produit_charge = 'CHARGES' 
    GROUP BY 
        poste ,
        exercice_comptable
    ORDER BY 
        exercice_comptable;
    """
    cursor.execute(query)

    Expense_table = cursor.fetchall()
    Expense_per_categorie_df=pd.DataFrame(Expense_table,columns=["Year","category","Expense_EUR"])
    print(Expense_per_categorie_df)
    return Expense_per_categorie_df  



'''
    Documentation : 
Return_on_investiment_per_year:

    * Calculates financial profits (type_de_resultat ='FINANCIER') grouped by year for investment analysis. (Profit outside the direct core business sales for example loans/credit)

'''

def Return_on_investiment_per_year(cursor):
    query="""select exercice_comptable As year, 
	   Sum(montant_en_eur) Profit_EUR
        from public.compte_resultat 
        where type_de_resultat ='FINANCIER' and produit_charge = 'PRODUITS'
        group by exercice_comptable
        order by exercice_comptable desc """    
    cursor.execute(query)

    ROI_table = cursor.fetchall()
    ROI_dataframe=pd.DataFrame(ROI_table,columns=["Year","Profit_EUR"])
    print(ROI_dataframe)
    return ROI_dataframe    

