"""
Purpose:
Acts as the orchestrator for the ETL process.

The script waits for the database to be ready (using Exceptions to deal with connection rejection ,and to synchronize with Docker startup ).
The session is passed to tools.Extract_and_Store_Records for data extraction and loading.
We created two indexes (idx_year,idx_produit_charge) to optimize our querys performance especially for Grouping and Aggregation



"""


from tools import Extract_and_Store_Records # import Function from tools.py where we keep our functions to maximize the level of readability
from common.base import session_factory
from sqlalchemy import Index

from Models.models import compte_resultat
import time
'''
# This code section begin with Start and end with END , is a way to verify database connection every 5 sec.
# and if it's still refuse to connect for 50s it exit the program.
'''

#Start
database_statue=False
i=0
while ( database_statue == False and i<10) :
    try:
        session,engine=session_factory(drop_tables=True)
        database_statue=True


    except Exception as e:
        print(e.args[0])
        print('Try...number=',i+1)
        time.sleep(5)
        i+=1
        continue
print('database_statue',database_statue)
if not database_statue:
    print('Exceeded Expected Time to Connect!!!! ')
    exit()
# END

url="https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/compte-de-resultat/records"

try:
    print(session)
    index_year = Index('idx_year', compte_resultat.exercice_comptable) # Create Index on 'exercice_comptable' .
    index_year.create(bind=engine) 

    idx_produit_charge = Index('idx_produit_charge', compte_resultat.produit_charge) # Create Index on 'produit_charge' .
    idx_produit_charge.create(bind=engine)
    Extract_and_Store_Records(session,compte_resultat,url)

    session.close()
except Exception as e  :
    print('Error',e)
    exit()