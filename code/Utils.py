import json
from deep_translator import GoogleTranslator
from NerRicette.code.Ingredient import Ingredient


class Utils:
    def __init__(self):
        self.trans = GoogleTranslator(source='it', target='en')
       

    #metodi di conversione e normalizzazione delle unità di misura

    def normalizeUnit(self, unit):
        SI = {'g':'g', 'gr':'g', 'grammo': 'g', 'grammi': 'g', 'G': 'g', 
        'kg':'kg', 'kilo':'kg', 'chilo':'kg','chilogrammo':'kg', 'chili': 'kg', 'KG':'kg',
        'l':'l','litro':'l', 'litri':'l', 'L':'l',
        'ml':'ml','millilitro':'ml', 'ML':'ml'
        }
        if unit in SI:
            return SI[unit]
        return None

    def convert_SI(self, val, unit_in, unit_out):
        SI = {'mg':0.001,'cg':0.01, 'g':1.0, 'kg':1000, 'ml':0.001,'cl':0.01, 'l':1.0}
        if (unit_in not in SI or unit_out not in SI) or not val.isdigit():
            return None
        return float(val)*SI[unit_in]/SI[unit_out]

    #altri metodi di utilità

    def isBlank (self, myString):
        return not (myString and myString.strip()) 
    
    def getIngsFromAnns(self, anns):
        ing = Ingredient()
        ings = []
        ings.append(ing)
        if anns is None:
            return ings
        for ann in anns:
            if(ann['entity_group']=='ING'):
                if(not self.isBlank(ing.text)):
                    ing = Ingredient()
                    ings.append(ing)
                ing.text = ann['word']
            elif(ann['entity_group']=='QUANTITY'):
                if(not self.isBlank(ing.qty)):
                    ing = Ingredient()
                    ings.append(ing)
                ing.qty = ann['word']
            elif(ann['entity_group']=='UNIT'):
                norm_unit = self.normalizeUnit(ann['word'])
                ing.unit = norm_unit if norm_unit is not None else ann["word"]
            elif(ann['entity_group']=='STATE'):
                ing.state.append(ann['word'])
            elif(ann['entity_group']=='PART'):
                ing.part = ann['word']
            elif(ann['entity_group']=='ALT'):
                ing.alt.append(ann['word'])
        return ings

    def translateIngredient(self, ing):
        if ing is None:
            return None
        ing_en = Ingredient()
        ing_en.qty = ing.qty
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
        return ing_en

