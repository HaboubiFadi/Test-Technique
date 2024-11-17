
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
    empty_results=False # variable that return true if the the api call stop returning data.
    while empty_results ==False:
        headers['offset']=i # offset is the number of the record the api start injesting From . 
        try:
            response=requests.get(url,params=headers)    # using the requests library to use the Api endpoint.
            result=response.json() # Convert the incoming data into a json
            if not result['results']: # if the api return no data the loop end.
                empty_results=True
                pass
            else:
                all_results=all_results + list(result['results']) # Concat the new results with the rest of the data.
                i+=limit
        except Exception as e :
            print('Error Happened : ',e.args)
    #df_unique=pd.DataFrame(all_results).drop_duplicates() # Drop duplications from the dataset.
    #all_results_clean=df.to_dict(orient='records')
    
    
    
    session.bulk_insert_mappings(Entity, all_results) # Efficiently inserts multiple records in one go.
    session.commit() #  Persists changes to the database .    
