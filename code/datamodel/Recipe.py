from NerRicette.code.datamodel.Ingredient import Ingredient
from NerRicette.code.datamodel.Nutritionals import Nutritionals
from NerRicette.code.datamodel.Nutritional import Nutritional
import json
class Recipe:
    def __init__(self):
        self.id = None
        self.title = None
        self.time = None
        self.portion = None
        self.ingredients = []
        self.instructions = []
        self.nutritionals = None
    def __iter__(self):
        yield from {
            "id": self.id,
            "title": self.title,
            "time": self.time,
            "portion": self.portion,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "nutritionals": self.nutritionals
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())
    def __repr__(self):
        return self.__str__()
        
    def to_json(self):
        nutr_val = Nutritionals() if self.nutritionals is None else self.nutritionals 
        to_return = {"id":self.id, "title": self.title, "time": self.time,"portion": self.portion, "ingredients": [], "instructions": self.instructions, "nutritionals": nutr_val.to_json()}
        ingrs = []
        for ingr in self.ingredients:
            ingrs.append(ingr.to_json())
        to_return["ingredients"] = ingrs
        return to_return
    def setNutritionalValue(self):
        self.nutritionals = self.getNutritionalValue()
    def getNutritionalValue(self):
        nutritionals = Nutritionals()
        nutritionals.protein = Nutritional()
        nutritionals.protein.unit = 'unit'
        nutritionals.total_lipid_fat = Nutritional()
        nutritionals.total_lipid_fat.unit = 'unit'
        nutritionals.carbohydrate_by_difference = Nutritional()
        nutritionals.carbohydrate_by_difference.unit = 'unit'
        nutritionals.energy = Nutritional()
        nutritionals.energy.unit = 'unit'
        nutritionals.carbohydrate_by_summation = Nutritional()
        nutritionals.carbohydrate_by_summation.unit = 'unit'
        nutritionals.sugars = Nutritional()
        nutritionals.sugars.unit = 'unit'
        nutritionals.fiber_total_dietary = Nutritional()
        nutritionals.fiber_total_dietary.unit = 'unit'
        nutritionals.sodium_na = Nutritional()
        nutritionals.sodium_na.unit = 'unit'
        nutritionals.fatty_acids_total_trans = Nutritional()
        nutritionals.fatty_acids_total_trans.unit = 'unit'
        nutritionals.fatty_acids_total_saturated = Nutritional()
        nutritionals.fatty_acids_total_saturated.unit = 'unit'
        for ingredient in self.ingredients:
            if ingredient.qty is not None and ingredient.qty.isdigit():
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.protein is not None and ingredient.nutr_vals.protein.value is not None:
                    nutritionals.protein.value = nutritionals.protein.value + ingredient.nutr_vals.protein.value*int(ingredient.qty)/100 if nutritionals.protein.value is not None else ingredient.nutr_vals.protein.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.total_lipid_fat is not None and ingredient.nutr_vals.total_lipid_fat.value is not None:
                    nutritionals.total_lipid_fat.value = nutritionals.total_lipid_fat.value + ingredient.nutr_vals.total_lipid_fat.value*int(ingredient.qty)/100 if nutritionals.total_lipid_fat.value is not None else ingredient.nutr_vals.total_lipid_fat.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.carbohydrate_by_difference is not None and ingredient.nutr_vals.carbohydrate_by_difference.value is not None:
                    nutritionals.carbohydrate_by_difference.value = nutritionals.carbohydrate_by_difference.value + ingredient.nutr_vals.carbohydrate_by_difference.value*int(ingredient.qty)/100 if nutritionals.carbohydrate_by_difference.value is not None else ingredient.nutr_vals.carbohydrate_by_difference.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.energy is not None and ingredient.nutr_vals.energy.value is not None:
                    nutritionals.energy.value = nutritionals.energy.value + ingredient.nutr_vals.energy.value*int(ingredient.qty)/100 if nutritionals.energy.value is not None else ingredient.nutr_vals.energy.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.carbohydrate_by_summation is not None and ingredient.nutr_vals.carbohydrate_by_summation.value is not None:
                    nutritionals.carbohydrate_by_summation.value = nutritionals.carbohydrate_by_summation.value + ingredient.nutr_vals.carbohydrate_by_summation.value*int(ingredient.qty)/100 if nutritionals.carbohydrate_by_summation.value is not None else ingredient.nutr_vals.carbohydrate_by_summation.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.sugars is not None and ingredient.nutr_vals.sugars.value is not None:
                    nutritionals.sugars.value = nutritionals.sugars.value + ingredient.nutr_vals.sugars.value*int(ingredient.qty)/100 if nutritionals.sugars.value is not None else ingredient.nutr_vals.sugars.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.fiber_total_dietary is not None and ingredient.nutr_vals.fiber_total_dietary.value is not None:
                    nutritionals.fiber_total_dietary.value = nutritionals.fiber_total_dietary.value + ingredient.nutr_vals.fiber_total_dietary.value*int(ingredient.qty)/100 if nutritionals.fiber_total_dietary.value is not None else ingredient.nutr_vals.fiber_total_dietary.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.sodium_na is not None and ingredient.nutr_vals.sodium_na.value is not None:
                    nutritionals.sodium_na.value = nutritionals.sodium_na.value + ingredient.nutr_vals.sodium_na.value*int(ingredient.qty)/100 if nutritionals.sodium_na.value is not None else ingredient.nutr_vals.sodium_na.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.fatty_acids_total_trans is not None and ingredient.nutr_vals.fatty_acids_total_trans.value is not None:
                    nutritionals.fatty_acids_total_trans.value = nutritionals.fatty_acids_total_trans.value + ingredient.nutr_vals.fatty_acids_total_trans.value*int(ingredient.qty)/100 if nutritionals.fatty_acids_total_trans.value is not None else ingredient.nutr_vals.fatty_acids_total_trans.value*int(ingredient.qty)/100 
                
                if ingredient.nutr_vals is not None and ingredient.nutr_vals.fatty_acids_total_saturated is not None and ingredient.nutr_vals.fatty_acids_total_saturated.value is not None:
                    nutritionals.fatty_acids_total_saturated.value = nutritionals.fatty_acids_total_saturated.value + ingredient.nutr_vals.fatty_acids_total_saturated.value*int(ingredient.qty)/100 if nutritionals.fatty_acids_total_saturated.value is not None else ingredient.nutr_vals.fatty_acids_total_saturated.value*int(ingredient.qty)/100 
        if self.portion:
            nutritionals.protein.value = nutritionals.protein.value if nutritionals.protein.value is None else nutritionals.protein.value/self.portion
            nutritionals.total_lipid_fat.value = nutritionals.total_lipid_fat.value if nutritionals.total_lipid_fat.value is None else nutritionals.total_lipid_fat.value/self.portion
            nutritionals.carbohydrate_by_difference.value = nutritionals.carbohydrate_by_difference.value if nutritionals.carbohydrate_by_difference.value is None else nutritionals.carbohydrate_by_difference.value/self.portion
            nutritionals.energy.value = nutritionals.energy.value if nutritionals.energy.value is None else nutritionals.energy.value/self.portion  
            nutritionals.carbohydrate_by_summation.value = nutritionals.carbohydrate_by_summation.value if nutritionals.carbohydrate_by_summation.value is None else nutritionals.carbohydrate_by_summation.value/self.portion
            nutritionals.sugars.value = nutritionals.sugars.value if nutritionals.sugars.value is None else nutritionals.sugars.value/self.portion
            nutritionals.fiber_total_dietary.value = nutritionals.fiber_total_dietary.value if nutritionals.fiber_total_dietary.value is None else nutritionals.fiber_total_dietary.value/self.portion  
            nutritionals.sodium_na.value = nutritionals.sodium_na.value if nutritionals.sodium_na.value is None else nutritionals.sodium_na.value/self.portion
            nutritionals.fatty_acids_total_trans.value = nutritionals.fatty_acids_total_trans.value if nutritionals.fatty_acids_total_trans.value is None else nutritionals.fatty_acids_total_trans.value/self.portion
            nutritionals.fatty_acids_total_saturated.value = nutritionals.fatty_acids_total_saturated.value if nutritionals.fatty_acids_total_saturated.value is None else nutritionals.fatty_acids_total_saturated.value/self.portion
        return nutritionals
           

    