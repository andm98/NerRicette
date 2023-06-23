import json
from deep_translator import GoogleTranslator
from NerRicette.code.Ingredient import Ingredient
import time

class Utils:
    def __init__(self):
        self.trans = GoogleTranslator(source='it', target='en')

    #altri metodi di utilità
    def isBlank (self, myString):
        return not (myString and myString.strip()) 
    def isEmpty(self, myArray):
        return myArray is None or len(myArray)==0
    def translateIngredient(self, ing):
        print("attendi traduzione...")
        time.sleep(5)
        if ing is None:
            return None
        ing_en = Ingredient()
        ing_en.qty = ing.qty
        ing_en.semantic_tags = ing.semantic_tags
        try:
            if not self.isBlank(ing.text):
                if not self.isBlank(ing.part):
                    ing_en.text = self.trans.translate(ing.part + ' di ' +ing.text)
                else:
                    ing_en.text = self.trans.translate(ing.text)
            if not self.isBlank(ing.unit):
                ing_en.unit = self.trans.translate(ing.unit)
            for state in ing.state:
                if not self.isBlank(ing.text):
                    ing_en.state.append(self.trans.translate(state))
        except:
            time.sleep(20)
        return ing_en
    


