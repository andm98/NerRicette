from NerRicette.code.abstract_class.NutritionalDataset import NutritionalDataset
from NerRicette.code.Utils import Utils
from NerRicette.code.Nutritionals import Nutritionals
from NerRicette.code.Nutritionals import Nutritional
from NerRicette.code.QtyConverter import QtyConverter
from NerRicette.code.abstract_class.SemanticTagger import SemanticTagger
import urllib
import requests
import json
import spacy

class UsdaDataset(NutritionalDataset):
    def __init__(self, parser, tagger):
        self.utils = Utils()
        self.semanticTagger = tagger
        self.qtyConverter = QtyConverter()
        self.parser = parser
        self.api_key = 'pgCVzl1d9f0Fe6fpNcVAkWbk1z8A7sCSzrhyNFGe'
        #self.api_key = 'DEMO_KEY'
        self.url = 'https://api.nal.usda.gov/fdc/v1/foods/search/'
        self.nlp = spacy.load('en_core_web_sm')
    def setNutritional(self, ing, nutrs):
         ing.nutr_vals = nutrs
    
    def matchIngredient(self, str):
        print("get")

    def score(self, ing):
        return ing['score']
    def getNutritional(self, ing_en, first_strategy, alt_strategy):
        names_only = self.getFoodNameOnly(ing_en)
        api = self.url+'?api_key='+self.api_key+'&query='+self.getQuery(ing_en)
        req = requests.get(api)
        if(req.status_code != 200):
            print("Superato il limite di chiamate dell'api USDA")
            return None
        foods = json.loads(req.text)["foods"]
        foods = list(filter(lambda food: first_strategy.isPresent(names_only, food["description"].split(', ')[:2]) , foods))
        if(len(foods)==0):
            return None #assegna quelli dell'ancestor
        foods.sort(reverse=True,key=self.score)
        more_similar_food = None
        max_similarity = -1
        more_tags = None
        sim_bool = False
        for food in foods:
            print("elaborando "+food["description"])
            similarity = first_strategy.compare(ing_en.getDescription().split(), food["description"].split(', '))
            if(similarity>max_similarity):
                max_similarity = similarity
                more_similar_food = food
                sim_bool = False
                more_tags = None
            elif(similarity==max_similarity and alt_strategy is not None):
                food_tags = self.semanticTagger.getSemanticTag(" ".join(food["description"].split(', ')[:2]))
                more_tags = self.semanticTagger.getSemanticTag(" ".join(more_similar_food["description"].split(', ')[:2])) if not sim_bool else more_tags
                sim_food = alt_strategy.compareWithTags(ing_en.getDescription().split(), food["description"].split(', '), ing_en.semantic_tags, food_tags)
                sim_more = alt_strategy.compareWithTags(ing_en.getDescription().split(), more_similar_food["description"].split(', '), ing_en.semantic_tags, more_tags)
                print(" ".join(food["description"].split(', ')[:2]))
                print(" ".join(more_similar_food["description"].split(', ')[:2]))
                print(sim_food)
                print(sim_more)
                if(sim_food>sim_more):
                    more_tags = food_tags
                    max_similarity = similarity
                    more_similar_food = food 
                sim_bool = True
                    
        print("WINNER")
        print(more_similar_food["description"])
        print("_____________________________")
        if self.utils.isEmpty(ing_en.semantic_tags) or self.utils.isEmpty(more_tags) or ing_en.semantic_tags[0]["ancestor"]!=more_tags[0]["ancestor"]: #sostituire con controllo più dettagliato
            print("CONTROLLO UOMO")
        nutrs = Nutritionals()
        nutrs.text = more_similar_food["description"]
        for item in list(filter(lambda item: item["nutrientId"] in (self.getValNutsUSDA().keys()), more_similar_food["foodNutrients"])):
                nutr = Nutritional()
                nutr.value = item["value"]
                nutr.unit = item["unitName"]
                nutrs[self.getValNutUSDA(item["nutrientId"])]=nutr
        return nutrs
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