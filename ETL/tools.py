
"""
Purpose:
Handles the core ETL logic: Extracting and Loading data.

How It Works:
* Extracts data from the API in batches.
    * Uses offset and limit to fetch data in chunks.
    * looping continues until no records are returned (empty_results=True).
* Transforms the JSON data into a format suitable for insertion.
* Inserts the data into the database table mapped by Entity.
"""

import requests
import pandas as pd
def Extract_and_Store_Records(session,Entity,url,limit=100):
    i=0
    headers={}
    headers['limit']=limit # Number of records per API call .
    all_results=[]
    empty_results=False
    while empty_results ==False:
        headers['offset']=i
        try:
            response=requests.get(url,params=headers)    
            result=response.json()
            if not result['results']:
                empty_results=True
                pass
            else:
                all_results=all_results + list(result['results'])
                print('length:',len(all_results))
                i+=limit
        except Exception as e :
            print('Error Happened : ',e.args)
    
    all_results=pd.DataFrame(all_results).drop_duplicates() # Drop Duplication Row
    all_results=all_results.to_dict(orient='records')  # Convert Dataframe to dict .
    session.bulk_insert_mappings(Entity, all_results) # Efficiently inserts multiple records in one go.
    session.commit() #  Persists changes to the database .    