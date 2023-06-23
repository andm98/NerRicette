from transformers import pipeline
from NerRicette.code.datamodel.Ingredient import Ingredient
from NerRicette.code.QtyConverter import QtyConverter
from NerRicette.code.Utils import Utils
from NerRicette.code.datamodel.Recipe import Recipe
from NerRicette.code.dataset.UsdaDataset import UsdaDataset
from NerRicette.code.similarity.LemmaSimilarity import LemmaSimilarity
from NerRicette.code.similarity.EmbeddingSimilarity import EmbeddingSimilarity
from NerRicette.code.tagger.BioPortalTagger import BioPortalTagger 
from recipe_scrapers import scrape_me
from transformers import logging
from tqdm import tqdm
from pathlib import Path

class RecipeParser:
  logging.set_verbosity_error()
  PATH = './'
  def __init__(self):
    self.semanticTagger = BioPortalTagger()
    self.utils = Utils()
    self.qtyConverter = QtyConverter()
    self.token_classifier = pipeline(
      "token-classification", model=self.PATH + "model/", aggregation_strategy= "simple", ignore_labels = [])
    self.nutr_dataset = UsdaDataset(self, self.semanticTagger)
    self.first_strg = LemmaSimilarity()
    self.alt_strg = EmbeddingSimilarity()
    
  def parse(self, text):    
    ricetta = Recipe()
    ings = self.parseIngredients(text)
    ricetta.ingredients = ings
    return ricetta
  
  def parseIngredients(self, text):    
    ings = self.getIngsFromAnns(self.token_classifier(text.lower()))
    for ing in ings:
      ing_en = self.utils.translateIngredient(ing)
      tag = self.semanticTagger.getSemanticTag(ing_en.text)
      ing.semantic_tags = tag
      ing_en.semantic_tags = tag
      ing.nutr_vals = self.nutr_dataset.getNutritional(ing_en, self.first_strg, self.alt_strg)
      ing.human_check = ing.nutr_vals.human_check if ing.nutr_vals is not None else '0'
    return ings

  def parseFromUrl(self, url):
    ricetta = Recipe()
    ricettaScrape = scrape_me(url)
    ings = []
    if(ricettaScrape is not None):
      ricetta.title = ricettaScrape.title()
      ricetta.time = ricettaScrape.total_time()
      ricetta.portion =  ricettaScrape.yields()
      ricetta.instructions = ricettaScrape.instructions_list()
      for ingScrape in tqdm(ricettaScrape.ingredients()):
        ings+=self.parseIngredients(ingScrape)
      ricetta.ingredients = ings
      return ricetta
    
  def parseWithoutNutr(self, text):    
    ings = self.getIngsFromAnns(self.token_classifier(text.lower()))
    ricetta = Recipe()
    ricetta.ingredients = ings
    return ricetta
  
  #annotations    
  def getIngsFromAnns(self, anns):
    ing = Ingredient()
    ings = []
    if anns is None:
        return ings
    ings.append(ing)
    for ann in anns:
        if(ann['entity_group']=='ING'):
            if(not self.utils.isBlank(ing.text)):
                ing = Ingredient()
                ings.append(ing)
            ing.text = ann['word']
        elif(ann['entity_group']=='QUANTITY'):
            if(not self.utils.isBlank(ing.qty)):
                ing = Ingredient()
                ings.append(ing)
            ing.qty = ann['word']
        elif(ann['entity_group']=='UNIT'):
            norm_unit = self.qtyConverter.normalizeUnit(ann['word'])
            ing.unit = norm_unit if norm_unit is not None else ann["word"]
        elif(ann['entity_group']=='STATE'):
            ing.state.append(ann['word'])
        elif(ann['entity_group']=='PART'):
            ing.part = ann['word']
        elif(ann['entity_group']=='ALT'):
            ing.alt.append(ann['word'])
    return ings