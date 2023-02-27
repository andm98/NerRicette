from transformers import AutoTokenizer, AutoModel
import json
from deep_translator import GoogleTranslator
import urllib
from RicetteNER.code.Ingredient import Ingredient
from RicetteNER.code.Nutritionals import Nutritionals
from RicetteNER.code.Nutritional import Nutritional
import numpy as np
import torch


class Utils:
    def __init__(self):
        PATH = './'
        self.trans = GoogleTranslator(source='it', target='en')
        self.model =  AutoModel.from_pretrained(PATH + "model/", output_hidden_states=True)
        self.tokenizer = AutoTokenizer.from_pretrained(PATH + "model/")

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

    #metodi per valutazione distanza sintattica e semantica

    def DistBatra(self, str1, str2):
        str1 = set(str1.split())
        str2 = set(str2.split())
        return float(len(str1 & str2)) / len(str1)

    def get_hidden_states(self, encoded, model, layers):
        with torch.no_grad():
            output = model(**encoded)
        # Get all hidden states
        states = output.hidden_states
        # Stack and sum all requested layers
        output = torch.stack([states[i] for i in layers]).mean(0).squeeze()
        # Only select the tokens that constitute the requested word
        word_tokens_output = output
        return word_tokens_output.sum(dim=0)
 
 
    def get_word_vector(self, sent, tokenizer, model, layers):
        encoded = tokenizer.encode_plus(sent, return_tensors="pt")
        with torch.no_grad():
            output = model(**encoded)
        return self.get_hidden_states(encoded, model, layers).numpy()
 
 
    def getWordEmb(self, sent, layers=None):
        # Use last four layers by default
        layers = [-4, -3, -2, -1] if layers is None else layers
        word_embedding = self.get_word_vector(sent, self.tokenizer, self.model, layers)
        return word_embedding 

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

    def getQueryUSDA(self, ingre):
        return urllib.parse.quote('+'+'('+ ingre.text + ')' + " " + " ".join(ingre.state))

    #altri metodi di utilità

    def isBlank (self, myString):
        return not (myString and myString.strip()) 
    
    def getIngsFromAnns(self, anns):
        ing = Ingredient()
        ings = []
        ings.append(ing)
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
   

