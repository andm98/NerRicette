import json
from NerRicette.code.Nutritional import Nutritional
class Nutritionals:
  def __init__(self):
    self.text = ""
    self.protein = None
    self.total_lipid_fat = None
    self.carbohydrate_by_difference = None
    self.energy = None
    self.carbohydrate_by_summation = None
    self.sugars = None
    self.fiber_total_dietary = None
    self.sodium_na = None
    self.fatty_acids_total_trans = None
    self.fatty_acids_total_saturated = None

  def __iter__(self):
    yield from {
          "text": self.text,
          "protein": self.protein,
          "total_lipid_fat": self.total_lipid_fat,
          "carbohydrate_by_difference":self.carbohydrate_by_difference,
          "energy":self.energy,
          "carbohydrate_by_summation":self.carbohydrate_by_summation,
          "sugars":self.sugars,
          "fiber_total_dietary": self.fiber_total_dietary,
          "sodium_na": self.sodium_na,
          "fatty_acids_total_trans": self.fatty_acids_total_trans,
          "fatty_acids_total_saturated": self.fatty_acids_total_saturated
    }.items()
  def __str__(self):
    return json.dumps(self.to_json())

  def __repr__(self):
    return self.__str__()

  def to_json(self):
    to_return = { 
          "text": self.text,
          "protein": 
            self.protein.to_json() if self.protein is not None else Nutritional().to_json()
          ,
          "total_lipid_fat": 
            self.total_lipid_fat.to_json() if self.total_lipid_fat is not None else Nutritional().to_json()
          ,
          "carbohydrate_by_difference":
            self.carbohydrate_by_difference.to_json() if self.carbohydrate_by_difference is not None else Nutritional().to_json()
          ,
          "energy":
            self.energy.to_json() if self.energy is not None else Nutritional().to_json()
          ,
          "carbohydrate_by_summation":
            self.carbohydrate_by_summation.to_json() if self.carbohydrate_by_summation is not None else Nutritional().to_json()
          ,
          "sugars":
            self.sugars.to_json() if self.sugars is not None else Nutritional().to_json()
          ,
          "fiber_total_dietary": 
            self.fiber_total_dietary.to_json() if self.fiber_total_dietary is not None else Nutritional().to_json()
          ,
          "sodium_na": 
            self.sodium_na.to_json() if self.sodium_na is not None else Nutritional().to_json()
          ,
          "fatty_acids_total_trans": 
            self.fatty_acids_total_trans.to_json() if self.fatty_acids_total_trans is not None else Nutritional().to_json()
          ,
          "fatty_acids_total_saturated": 
            self.fatty_acids_total_saturated.to_json() if self.fatty_acids_total_saturated is not None else Nutritional().to_json()
          }
    return to_return
        

  def __getitem__(self, key):
    return getattr(self, key)
  def __setitem__(self, key, value):
    setattr(self, key, value)


 
  
  

