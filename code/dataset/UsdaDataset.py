from NerRicette.code.abstract_class.NutritionalDataset import NutritionalDataset
from NerRicette.code.Utils import Utils
from NerRicette.code.datamodel.Nutritionals import Nutritionals
from NerRicette.code.datamodel.Nutritionals import Nutritional
from NerRicette.code.QtyConverter import QtyConverter
from NerRicette.code.datamodel.Ingredient import Ingredient
from NerRicette.code.tagger.NerRicetteTagger import NerRicetteTagger
from NerRicette.code.abstract_class.SemanticTagger import SemanticTagger
import urllib
import requests
import json
import spacy
from django.conf import settings
from recipeapp.dao import NutritionalDao
class UsdaDataset(NutritionalDataset):
    def __init__(self, parser, tagger):
        self.nutritional_dao = NutritionalDao()
        self.utils = Utils()
        self.semanticTagger = tagger
        self.qtyConverter = QtyConverter()
        self.parser = parser
        self.api_key = settings.USDA
        self.url = 'https://api.nal.usda.gov/fdc/v1/foods/search/'
        self.nlp = spacy.load('en_core_web_sm')
        self.nerRicetteTagger = NerRicetteTagger()
    def setNutritional(self, ing, nutrs):
         ing.nutr_vals = nutrs
    
    def matchIngredient(self, ing, first_strategy, alt_strategy):
        names_only = self.getFoodNameOnly(ing)
        api = self.url+'?api_key='+self.api_key+'&query='+self.getQuery(ing)
        req = requests.get(api)
        if(req.status_code != 200):
            print("Superato il limite di chiamate dell'api USDA")
            return None
        foods = json.loads(req.text)["foods"]
        for food in foods:
            self.saveNutritional(self.getNutritionals(food))
        foods = list(filter(lambda food: first_strategy.isPresent(names_only, food["description"].split(', ')[:2]) , foods))
        if(len(foods)==0):
            return None 
        more_similar_food = None
        max_similarity = -1
        for food in foods:
            food["description"] = food["description"].replace(", raw", "")
            print("elemento più simile "+more_similar_food["description"] if more_similar_food is not None else "prima esecuzione") 
            print("elaborando "+food["description"])
            similarity = first_strategy.compare(ing.getDescription().split(), food["description"].split(', '))
            if(similarity>max_similarity):
                max_similarity = similarity
                more_similar_food = food
            elif(similarity==max_similarity and alt_strategy is not None):
                sim_food = alt_strategy.compare(ing.getDescription().split(), food["description"].split(', '))
                sim_more = alt_strategy.compare(ing.getDescription().split(), more_similar_food["description"].split(', '))
                print(sim_food)
                if(sim_food>sim_more):
                    max_similarity = similarity
                    more_similar_food = food 
        more_tags = self.semanticTagger.getSemanticTag(" ".join(more_similar_food["description"].split(', ')[:2]))
        ing_new = Ingredient()
        ing_new.text = more_similar_food["description"]
        ing_new.nutr_vals = self.getNutritionals(more_similar_food)
        if self.utils.isEmpty(ing.semantic_tags) or self.utils.isEmpty(more_tags) or ing.semantic_tags[0]["ancestor"]!=more_tags[0]["ancestor"]: #sostituire con controllo più dettagliato
            ing_new.nutr_vals.human_check = '1'
        return ing_new

    def score(self, ing):
        return ing['score']
    def getNutritional(self, ing, first_strategy, alt_strategy):
        ing = self.matchIngredient(ing, first_strategy, alt_strategy)
        return ing.nutr_vals if ing else None
    
    def getQuery(self, ingre):
        #dataType=Survey%20%28FNDDS%29
        return urllib.parse.quote(ingre.text + " " + " ".join(ingre.state))+'&dataType=Survey%20%28FNDDS%29,Foundation,SR%20Legacy&pageSize=10&pageNumber=1'
    
    def getNutritionals(self, usda_food):
        nutrs = Nutritionals()
        nutrs.text = usda_food["description"]
        for item in list(filter(lambda item: item["nutrientId"] in (self.getValNutsUSDA().keys()), usda_food["foodNutrients"])):
                nutr = Nutritional()
                nutr.value = item["value"]
                nutr.unit = item["unitName"]
                nutrs[self.getValNutUSDA(item["nutrientId"])]=nutr
        return nutrs
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
    
    def saveNutritional(self, nutritionals):
        self.nutritional_dao.save(nutritionals)   