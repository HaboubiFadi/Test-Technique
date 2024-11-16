"""
Purpose:
Acts as the orchestrator for the ETL process.

The script waits for the database to be ready (using time.sleep to synchronize with Docker startup).
The session is passed to tools.py for data extraction and loading.
"""


from tools import Extract_and_Store_Records # import Function from tools.py where we keep our functions to maximize the level of readability
from common.base import session_factory

from Models.models import compte_resultat
import time

# This code section begin with Start and end with END , is a way to verify database connection every 5 sec ,and if it's still refuse to connect for 50s it exit the program
#Start
database_statue=False
i=0
while ( database_statue == False and i<10) :
    try:
        session=session_factory(drop_tables=True)
        database_statue=True


    except Exception as e:
        print(e.args[0])
        print('Try...number=',i+1)
        time.sleep(5)
        i+=1
        continue
print('database_statue',database_statue)
if not database_statue:
    exit()
# END
url="https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/compte-de-resultat/records"
 
try:
    print(session)
    Extract_and_Store_Records(session,compte_resultat,url)
    session.close()
except Exception as e  :
    print('Error',e)
    exit()