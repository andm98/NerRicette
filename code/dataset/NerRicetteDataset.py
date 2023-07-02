from NerRicette.code.abstract_class.NutritionalDataset import NutritionalDataset
from NerRicette.code.Utils import Utils
from NerRicette.code.datamodel.Ingredient import Ingredient
from NerRicette.code.datamodel.Nutritionals import Nutritionals
from NerRicette.code.datamodel.Nutritionals import Nutritional
from NerRicette.code.QtyConverter import QtyConverter
from NerRicette.code.abstract_class.SemanticTagger import SemanticTagger
from recipeapp.dao import IngredientDao
import urllib
import requests
import json
import spacy

class NerRicetteDataset(NutritionalDataset):
    def __init__(self):
        self.ingredient_dao = IngredientDao()
        self.utils = Utils()
        self.qtyConverter = QtyConverter()
        
    def setNutritional(self, ing, nutrs):
         ing.nutr_vals = nutrs
    
    def matchIngredient(self, ing, first_strategy=None, alt_strategy=None):
        foods = self.ingredient_dao.getByNameAndStateIn(ing.text, ing.state)
        if self.utils.isEmpty(foods):
            return None
        max_similarity = -1
        more_tags = None
        for food in foods:
            similarity = first_strategy.compare(ing.getDescriptionWithPart().split(), food.getDescriptionWithPart().split())
            if(similarity>max_similarity):
                max_similarity = similarity
                more_similar_food = food
                more_tags = None
            elif(similarity==max_similarity and alt_strategy is not None):
                sim_food = alt_strategy.compare(ing.getDescriptionWithPart().split(), food.getDescriptionWithPart().split())
                sim_more = alt_strategy.compare(ing.getDescriptionWithPart().split(), more_similar_food.getDescriptionWithPart().split())
                if(sim_food>sim_more):
                    max_similarity = similarity
                    more_similar_food = food 
        return more_similar_food

  
    def getNutritional(self, ing, first_strategy=None, alt_strategy=None):
        ing = self.matchIngredient(ing, first_strategy, alt_strategy)
        return ing.nutr_vals if ing else None
    
    def getQuery(self, ingre):
        return urllib.parse.quote(ingre.text)
