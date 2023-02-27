from transformers import pipeline
from RicetteNER.code.Ingredient import Ingredient
from RicetteNER.code.Utils import Utils
from RicetteNER.code.Recipe import Recipe
from recipe_scrapers import scrape_me


class RecipeParser:
  PATH = './'
  def __init__(self):
    self.utils = Utils()
    self.token_classifier = pipeline(
      "token-classification", model=self.PATH + "model/", aggregation_strategy= "simple", ignore_labels = [])
  def parse(self, text):    
    ings = self.utils.getIngsFromAnns(self.token_classifier(text.lower()))
    ricetta = Recipe()
    ricetta.ingredients = ings
    for ing in ings:
      ing.setNutritions(self.utils, "USDA")
    print(ricetta)

  def parseFromUrl(self, url):
    ricetta = Recipe()
    ricettaScrape = scrape_me(url)
    #aggiungere controllo su stato della risposta
    if(ricettaScrape is not None):
      ricetta.title = ricettaScrape.title()
      ricetta.instructions = ricettaScrape.instructions_list()
      ingrs = []
      for ingScrape in ricettaScrape.ingredients():
        ings = self.utils.getIngsFromAnns(self.token_classifier(ingScrape.lower()))
        for ing in ings:
          ing.setNutritions(self.utils, "USDA")
          ingrs.append(ing)
      ricetta.ingredients = ingrs
      print(ricetta)
     