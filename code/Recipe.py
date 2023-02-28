from NerRicette.code.Ingredient import Ingredient
from NerRicette.code.Nutritionals import Nutritionals
from NerRicette.code.Nutritional import Nutritional
import json
class Recipe:
    def __init__(self):
        self.title = None
        self.ingredients = []
        self.instructions = []
    def __iter__(self):
        yield from {
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())
        # return json.dumps(dict(self), default=default, ensure_ascii=False)
    def __repr__(self):
        return self.__str__()
        
    def to_json(self):
        to_return = {"title": self.title, "ingredients": [], "instructions": self.instructions}
        ingrs = []
        for ingr in self.ingredients:
            ingrs.append(ingr.to_json())
        to_return["ingredients"] = ingrs
        return to_return

    def getNutritionalValue(self):
        nutritional = Nutritionals()
        total_for_nutr = None
        unit = None
        for key in nutritional.to_json().keys():
            for ingredient in self.ingredients:
                if ingredient.nutr_vals is not None and ingredient.nutr_vals[key] is not None and ingredient.nutr_vals[key].value is not None:
                    if total_for_nutr is not None:
                        total_for_nutr += ingredient.nutr_vals[key].value
                    else:
                        unit = ingredient.nutr_vals[key].unit
                        total_for_nutr = ingredient.nutr_vals[key].value
            nutritional[key]= Nutritional()
            nutritional[key].value = total_for_nutr
            nutritional[key].unit = unit
            total_for_nutr = None
            unit = None
        return nutritional
           

    