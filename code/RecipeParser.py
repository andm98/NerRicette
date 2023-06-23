from transformers import pipeline
from NerRicette.code.Ingredient import Ingredient
from NerRicette.code.QtyConverter import QtyConverter
from NerRicette.code.Utils import Utils
from NerRicette.code.Recipe import Recipe
from NerRicette.code.UsdaDataset import UsdaDataset
from NerRicette.code.LemmaSimilarity import LemmaSimilarity
from NerRicette.code.EmbeddingSimilarity import EmbeddingSimilarity
from NerRicette.code.BioPortalTagger import BioPortalTagger 
from recipe_scrapers import scrape_me
from transformers import logging
from tqdm import tqdm

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
    ings = self.getIngsFromAnns(self.token_classifier(text.lower()))
    ricetta = Recipe()
    ricetta.ingredients = ings
    for ing in tqdm(ings):
      ing_en = self.utils.translateIngredient(ing)
      tag = self.semanticTagger.getSemanticTag(ing_en.text)
      ing_en.semantic_tags = tag
      ing.semantic_tags = tag
      ing.nutr_vals = self.nutr_dataset.getNutritional(ing_en, self.first_strg, self.alt_strg)
    return ricetta

  def parseFromUrl(self, url):
    ricetta = Recipe()
    ricettaScrape = scrape_me(url)
    #aggiungere controllo su stato della risposta
    if(ricettaScrape is not None):
      ricetta.title = ricettaScrape.title()
      ricetta.instructions = ricettaScrape.instructions_list()
      ingrs = []
      for ingScrape in tqdm(ricettaScrape.ingredients()):
        ings = self.getIngsFromAnns(self.token_classifier(ingScrape.lower()))
        for ing in ings:
          ing_en = self.utils.translateIngredient(ing)
          tag = self.semanticTagger.getSemanticTag(ing_en.text)
          ing_en.semantic_tags = tag
          ing.semantic_tags = tag
          ing.nutr_vals = self.nutr_dataset.getNutritional(ing_en, self.first_strg, self.alt_strg)
          ingrs.append(ing)
      ricetta.ingredients = ingrs
      return ricetta
     
  def parseWithoutNutr(self, text):    
    ings = self.getIngsFromAnns(self.token_classifier(text.lower()))
    for ing in ings:
      ing_en = self.utils.translateIngredient(ing)
      tag = self.semanticTagger.getSemanticTag(ing_en.text)
      ing.semantic_tags = tag
    ricetta = Recipe()
    ricetta.ingredients = ings
    return ricetta
  
  #annotations    
  def getIngsFromAnns(self, anns):
    ing = Ingredient()
    ings = []
    ings.append(ing)
    if anns is None:
        return ings
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
            print(ann['word'])
            ing.alt.append(ann['word'])
    return ings
