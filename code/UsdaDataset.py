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
        #self.api_key = 'DEMO_KEY'
        self.url = 'https://api.nal.usda.gov/fdc/v1/foods/search/'
        self.nlp = spacy.load('en_core_web_sm')
    def getNutritional(self, str):
        print("get")

    def score(self, ing):
        return ing['score']
    def setNutritional(self, ing, first_strategy, alt_strategy):
        ing_en = self.utils.translateIngredient(ing) 
        names_only = self.getFoodNameOnly(ing_en)
        api = self.url+'?api_key='+self.api_key+'&query='+self.getQuery(ing_en)
        req = requests.get(api)
        if(req.status_code != 200):
            print("Superato il limite di chiamate dell'api USDA")
            return None
        foods = json.loads(req.text)["foods"]
        print(ing_en.getDescription())
        for food in foods:
            print("".join(food["description"].split(', ')) + " first " + str(first_strategy.compare(ing_en.getDescription().split(), food["description"].split(', '))) + " alt " + str(alt_strategy.compare(ing_en.getDescription().split(), food["description"].split(', '))))
        foods = list(filter(lambda food: first_strategy.isPresent(names_only, food["description"].split(', ')[:2]) , foods))
        if(len(foods)==0):
            ing.nutr_vals = Nutritionals()
            return None
        foods.sort(reverse=True,key=self.score)
        more_similar_food = None
        max_similarity = -1
        for food in foods:
            similarity = first_strategy.compare(ing_en.getDescription().split(), food["description"].split(', '))
            if(similarity>max_similarity):
                max_similarity = similarity
                more_similar_food = food
            elif(similarity==max_similarity and alt_strategy is not None):
                sim_food = alt_strategy.compare(ing_en.getDescription().split(), food["description"].split(', '))
                sim_more = alt_strategy.compare(ing_en.getDescription().split(), more_similar_food["description"].split(', '))
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
        #dataType=Survey%20%28FNDDS%29
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
        if len(ing.text.split())==1:
            return [ing.text]
        tokens = self.nlp(ing.text)
        names_only = []
        for token in tokens:
            if token.tag_ == 'NN' or token.tag_ == 'NNS' or token.tag_ == 'NNP' or token.tag_ == 'NNPS':
                names_only.append(token.text)
        if(len(names_only)==1):
            return names_only
        for word in names_only:
            food_text = self.parser.parseWithoutNutr(word).ingredients[0].text
            if self.utils.isBlank(food_text):
                names_only.remove(word)
        return names_only if len(names_only)>0 else [ing.text]