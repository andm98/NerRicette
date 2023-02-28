from NerRicette.code.abstract_class.NutritionalDataset import NutritionalDataset
from NerRicette.code.Utils import Utils
from NerRicette.code.Nutritionals import Nutritionals
from NerRicette.code.Nutritionals import Nutritional
import urllib
import requests
import json
import spacy

class UsdaDataset(NutritionalDataset):
    def __init__(self, parser):
        self.utils = Utils()
        self.parser = parser
        self.api_key = 'pgCVzl1d9f0Fe6fpNcVAkWbk1z8A7sCSzrhyNFGe'
        self.url = 'https://api.nal.usda.gov/fdc/v1/foods/search/'
        self.nlp = spacy.load('en_core_web_sm')
    def getNutritional(self, str):
        print("get")

    def setNutritional(self, ing, sim_strategy, alt_strategy):
        ing_en = self.utils.translateIngredient(ing) 
        names_only = self.getFoodNameOnly(ing_en)
        api = self.url+'?api_key='+self.api_key+'&query='+self.getQuery(ing_en)
        req = requests.get(api)
        if(req.status_code is not 200):
            print("Superato il limite di chiamate dell'api USDA")
            return None
        foods = json.loads(req.text)["foods"]
        foods = list(filter(lambda food: sim_strategy.isPresent(names_only,  ("".join(food["description"].split(',')[:2]))) , foods))
        if(len(foods)==0):
            return None
        more_similar_food = None
        max_similarity = -1
        for food in foods:
            similarity = sim_strategy.compare(ing_en.getDescription(), "".join(food["description"].split(',')))
            if(similarity>max_similarity):
                max_similarity = similarity
                more_similar_food = food
            elif(similarity==max_similarity and alt_strategy is not None):
                sim_food = alt_strategy.compare(ing_en.getDescription(), "".join(food["description"].split(',')))
                sim_more = alt_strategy.compare(ing_en.getDescription(), "".join(more_similar_food["description"].split(',')))
                if(sim_food>sim_more):
                    max_similarity = similarity
                    more_similar_food = food 
        ing.nutr_text = more_similar_food["description"]
        nutrs = Nutritionals()
        for item in list(filter(lambda item: item["nutrientId"] in (self.getValNutsUSDA().keys()), more_similar_food["foodNutrients"])):
                nutr = Nutritional()
                nutr_gr = self.utils.convert_SI(ing_en.qty, ing_en.unit, 'g')
                if(nutr_gr is not None):
                    nutr.value = (nutr_gr*item["value"])/100
                    nutr.unit = item["unitName"]
                nutrs[self.getValNutUSDA(item["nutrientId"])]=nutr
        ing.nutr_vals = nutrs
   
    def getQuery(self, ingre):
        return urllib.parse.quote(ingre.text + " " + " ".join(ingre.state))+'&dataType=Survey%20%28FNDDS%29,Foundation,SR%20Legacy&pageSize=10&pageNumber=1'
    
     #metodi per la conversione dei valori nutrizionali da USDA

    def getValNutUSDA(self,id):
        nuts = self.getValNutsUSDA()
        if id in nuts:
            return nuts[id]
        return None

    def getValNutsUSDA(self):
        return {
            1003:"protein",
            1004:"total_lipid_fat",
            1005:"carbohydrate_by_difference",
            1008:"energy",
            1050:"carbohydrate_by_summation",
            1062:"energy",
            1063:"sugars",
            1079:"fiber_total_dietary",
            1093:"sodium_na",
            1257:"fatty_acids_total_trans",
            1258:"fatty_acids_total_saturated"
    }
    
    def getFoodNameOnly(self, ing):
        names_only = []
        words = ing.text.split()
        if len(words)==1:
            return ing.text
        for word in words:
            food_text = self.parser.parseWithoutNutr(word).ingredients[0].text
            if not self.utils.isBlank(food_text):
                names_only.append(food_text)
        if len(names_only)==1:
            return names_only[0]
        elif len(names_only)==0:
            return ing.text
        tokens = self.nlp(" ".join(names_only))
        names_only = []
        for token in tokens:
            if token.tag_ == 'NN':
                names_only.append(token.text)
        return " ".join(names_only) if len(names_only)>0 else ing.text