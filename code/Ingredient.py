import json
from RicetteNER.code.Nutritionals import Nutritionals
from RicetteNER.code.Nutritional import Nutritional
import requests
from scipy.spatial.distance import cosine

class Ingredient:
  def __init__(self):
    self.text = ""
    self.qty = ""
    self.unit = ""
    self.state = []
    self.part = ""
    self.alt = []
    self.nutr_vals = None
    #self.nutr_vals_100g = None
    self.usda_text = ""
  def __iter__(self):
    yield from {
          "text": self.text,
          "qty": self.qty,
          "unit":self.unit,
          "state":self.state,
          "part":self.part,
          "alt":self.alt,
          "nutr_vals": self.nutr_vals,
          "usda_text": self.usda_text
    }.items()
  def __str__(self):
    return json.dumps(self.to_json())

  def __repr__(self):
    return self.__str__()

  def to_json(self):
    nutr_val = Nutritionals() if self.nutr_vals is None else self.nutr_vals 
    #nutr_val_100g = Nutritionals() if self.nutr_vals_100g is None else self.nutr_vals_100g
    to_return = {
      "text": self.text, "qty": self.qty, "unit":self.unit,
      "state":self.state, "part": self.part, "usda_text": self.usda_text, 
      "alt": self.alt, "nutr_vals": nutr_val.to_json()
      #"nutr_vals_100g": nutr_val_100g.to_json()
    }
    return to_return
    
  def getDescription(self):
    return self.text + " ".join(self.state)

  def setNutritions(self, util, dataset):
    if(dataset=="USDA"):
      self.setNutritionsUSDA(util)

  def setNutritionsUSDA(self, util):
        ing_en = util.translateIngredient(self)
        print(ing_en.text)
        api_key = 'DEMO_KEY'
        THRESHOLD = 0.75
        food_descr = util.getWordEmb(ing_en.getDescription().lower())
        api = 'https://api.nal.usda.gov/fdc/v1/foods/search/?api_key=DEMO_KEY&query='+util.getQueryUSDA(ing_en)+'&dataType=Foundation,SR%20Legacy&pageSize=10&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc'
        req = requests.get(api)
        if(req.status_code is not 200):
            print("Ecceduto il numero di chiamate dell'api")
            return None
        foods = json.loads(req.text)["foods"]
        index = 0
        for food in foods:
            food_usda = ("".join(food["description"].split(',')[:2])).lower()
            if util.DistBatra(ing_en.text, food_usda)<THRESHOLD:
                foods.pop(index) 
            index+=1
        if(len(foods)==0):
            return None
        min_index = 0
        min_distance = 100
        index = 0
        for food in foods:
            print(food["description"])
            food_usda = util.getWordEmb(" ".join(food["description"].split(',')).lower())
            distance = cosine(food_descr, food_usda)
            print(distance)
            print("_____________________________________________________________________")
            if(distance<min_distance):
                min_distance = distance
                min_index = index
            index+=1
        resp =  foods[min_index]
        self.usda_text = resp["description"]
        nut_keys = util.getValNutsUSDA().keys()
        nutrs = Nutritionals()
        for item in list(filter(lambda item: item["nutrientId"] in (nut_keys), resp["foodNutrients"])):
                nutr = Nutritional()
                nutr_gr = util.convert_SI(ing_en.qty, ing_en.unit, 'g')
                if(nutr_gr is not None):
                    nutr.value = (nutr_gr*item["value"])/100
                    nutr.unit = item["unitName"]
                nutrs[util.getValNutUSDA(item["nutrientId"])]=nutr
        self.nutr_vals = nutrsù

        