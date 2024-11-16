"""
Purpose:
Maps the compte_resultat table to a Python class, enabling seamless ORM operations.

"""


from sqlalchemy import Column,Integer,String,FLOAT
import sys 

sys.path.append("../common") 
from common.base import Base




class compte_resultat(Base): # Represents the database table.
    __tablename__='compte_resultat'

    id=Column(Integer,primary_key=True) # Id is primary column that will be mapped dynamically 
    exercice_comptable=Column(Integer)
    type_de_resultat=Column(String)
    produit_charge=Column(String)
    poste=Column(String)
    detail_postes=Column(String)
    montant_en_eur=Column(FLOAT)
   
    
    def __init__(self,dic): # Automatically maps dictionary keys to object attributes.
        
            
        self.exercice_comptable=int(dic['exercice_comptable'])
        self.type_de_resultat=dic['type_de_resultat']
        self.produit_charge=dic['produit_charge']
        self.poste=dic['poste']
        self.detail_postes=dic['detail_postes']
        self.montant_en_eur=dic['montant_en_eur']



