import json
from deep_translator import GoogleTranslator
from NerRicette.code.datamodel.Ingredient import Ingredient


class QtyConverter:
    
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
    """
    def convert():
        for item in list(filter(lambda item: item["nutrientId"] in (self.getValNutsUSDA().keys()), more_similar_food["foodNutrients"])):
                nutr = Nutritional()
                nutr_gr = self.qty_converter.convert_SI(ing_en.qty, ing_en.unit, 'g')
                if(nutr_gr is not None):
                    nutr.value = (nutr_gr*item["value"])/100
                    nutr.unit = item["unitName"]
                nutrs[self.getValNutUSDA(item["nutrientId"])]=nutr
    """     