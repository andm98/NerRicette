<style>
table {
  table-layout: fixed;
  word-wrap: break-word;
}
</style>
# NerRicette
![Bot](assets/imgs/bot_green.png?raw=true "Bot")
The repository contains NerRicette, a model for recognizing cooking-related tags and for estimating nutritional values.
A multilingual BERT model is used, trained in token classification with the following tags:
| Tag           | Descrizione                                              |
| ------------- | -------------------------------------------------------- |
| B-ING         | Ingredient name, including type ("farina 00",  "carne di manzo", "lievito di birra"), color ("riso bianco", "nero"),  taste ("gelato al cioccolato") and origin ( "pecorino romano").            |
| I-ING         | Term within a span of an ingredient.                     |
| B-QUANTITY    | Quantity.                                                |
| I-QUANTITY    | Term within a span of a quantity.                        |
| B-UNIT        | Unit of measure.                                         |
| I-UNIT        | Term within a span of a unit of measurement.             |
| B-STATE       | Ingredient processing ("tagliato", "cotto", "mescolato", "fritto"), purpose ("per decorazione"), freshness, temperature.         |
| I-STATE       | Term within a span of a state.                           |
| B-PART        | Part of the ingredient  ("succo", "buccia", "fegato", "filetto").                                                                |
| I-PART        | Term within a span of a part of the ingredient.          |
| B-ALT         |   Alternative to an ingredient. The alternative can 
include all the elements of this table or only some of them.               |
| I-ALT         | Term within a span of an alternative.                    |
| O             | Punctuation or terms not included in the above categories.                                                                        |

Nutritional values are estimated by searching for the closest ingredient among those available in the USDA datasets.
You can test the model at the following link:
[Test the model](https://colab.research.google.com/drive/1uDFF2jacVXE4TaxSXtPhCpB4YNwkganj#)

#### Reproducibility

1. Run the 'UnnotatedDataset' notebook for creating the unannotated recipe dataset
2. Annotate the data with the data\annotated\label_config.json configuration tags
3. Run the 'AnnotatedDataset' notebook for annotated dataset creation
4. Run the 'Training' notebook to train the model
You can use the dataset data\annotated\recipe_dataset.csv and perform step 4 directly.
#### Food Wordl
The model was used for developing a webapp, referred to as Food World (currently not online).
Food World is a platform for the semantic search of recipes, the estimation of nutritional values, and the creation of nutritional models.
Database design and individual tasks are described.
#### Dataset design
Food World is based on a database of recipes, with ingredients and nutritional values.
The insertion of a new recipe takes place automatically (with a possible final human control), through the following steps:
1. The recipe-scrapers library is used to get the title, ingredient list, and instructions.
2. The NER model extracts the ingredient, initial state, quantity, and unit of measurement.
3. The ingredient is searched in the database.
4. If the ingredient is available, it is added to the recipe.
5. If the ingredient is not available, semantic tags and nutritional information are assigned.
6. The ingredient is saved and added to the recipe.
7. The recipe is saved.
![Bot](assets/imgs/scheme.png?raw=true "Bot")
#### Semantic search
The recipes can be filtered for:
* Title.
* Ingredients and alternatives, available quantities, parts of the ingredient, initial state.
* Type of nutrition model (vegan, vegetarian).
* Nutritional values.
* Allergies.
#### Resources used
* recipe-scrapers [link](https://github.com/hhursev/recipe-scrapers)
* Hugginface [link](https://huggingface.co/)
* Modello Bert [link](https://huggingface.co/bert-base-multilingual-uncased)
* Spacy [link](https://spacy.io/)
* Doccano [link](https://github.com/doccano/doccano)
* USDA FoodData [link](https://fdc.nal.usda.gov/)
* GialloZafferano [link](https://www.giallozafferano.it/)
* Mysia.info [link](https://www.misya.info/)
