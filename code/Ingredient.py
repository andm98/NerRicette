import json
from NerRicette.code.Nutritionals import Nutritionals
from NerRicette.code.Nutritional import Nutritional

class Ingredient:
  def __init__(self):
    self.text = ""
    self.qty = ""
    self.unit = ""
    self.state = []
    self.part = ""
    self.alt = []
    self.nutr_vals = None
    self.semantic_tags = None
    #self.nutr_vals_100g = None
  def __iter__(self):
    yield from {
          "text": self.text,
          "qty": self.qty,
          "unit":self.unit,
          "state":self.state,
          "part":self.part,
          "alt":self.alt,
          "nutr_vals": self.nutr_vals,
          "semantic_tags": self.semantic_tags
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
      "state":self.state, "part": self.part, 
      "alt": self.alt, "nutr_vals": nutr_val.to_json(),
      "semantic_tags": self.semantic_tags
    }
    return to_return
    
  def getDescription(self):
    return self.text + ' '+ " ".join(self.state)





       