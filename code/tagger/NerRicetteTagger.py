from NerRicette.code.abstract_class.SemanticTagger import SemanticTagger
from NerRicette.code.Utils import Utils
from NerRicette.code.QtyConverter import QtyConverter
from recipeapp.dao import IngredientDao
import urllib
import requests
import json
import time

class NerRicetteTagger(SemanticTagger):
    def __init__(self):
        self.utils = Utils()
        self.ingredient_dao = IngredientDao()
    
    def matchIngredient(self, str):
        print("to do")
 
    
    def getSemanticTag(self, text):
        ings =  self.ingredient_dao.getByNameLike(text)
        if ings is not None and len(ings)>0:
            return ings[0].semantic_tags
        return None
    
    def setSemanticTag(self, ing, tags):
        print("to do")
    def getQuery(self,text):
        print("to do")
            