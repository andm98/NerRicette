# NerRicette
![Bot](assets/imgs/bot_green.png?raw=true "Bot")

La repository contiene NerRicette, un modello per il riconoscimento di tag relativi alla cucina e per la stima di valori nutrizionali.
Viene utilizzato un modello BERT multilinguaggio, addestrato nella classificazione dei token con i seguenti tag:
| Tag           | Descrizione                                              |
| ------------- | -------------------------------------------------------- |
| B-ING         | Nome dell'ingrediente                                    |
| I-ING         |                                                          |
| B-QUANTITY    | Quantità                                                 |
| I-QUANTITY    |                                                          |
| B-UNIT        | Unità di misura                                          |
| I-UNIT        |                                                          |
| B-STATE       | Lavorazione dell’ingrediente                             |
| I-STATE       |                                                          |
| B-PART        | Parte dell’ingrediente                                   |
| I-PART        |                                                          |
| B-EQUIPMENT   | Attrezzattura utilizzata nella ricetta                   |
| I-EQUIPMENT   |                                                          |
| B-ALT         | Alternativa di un ingrediente                            |
| I-ALT         |                                                          |
| O             | Altro                                                    |


La stima dei valori nutrizionali avviene tramite la ricerca dell'ingrediente più simile
tra quelli disponibili nei dataset USDA.


É possibile testare il modello al seguente link:
[Prova il modello](https://colab.research.google.com/drive/1uDFF2jacVXE4TaxSXtPhCpB4YNwkganj#)

#### Riprodubilità

1. Eseguire il notebook 'UnnotatedDataset' per la creazione del dataset di ricette non annotate
2. Annotare i dati con i tag della configurazione data\annotated\label_config.json
3. Eseguire il notebook 'AnnotatedDataset' per la creazione del dataset annotato
4. Eseguire il notebook 'Training' per addestrare il modello

É possibile utilizzare il dataset data\annotated\recipe_dataset.csv ed eseguire direttamente la fase 4.

#### Risorse utilizzate

* recipe-scrapers [link](https://github.com/hhursev/recipe-scrapers)
* Hugginface [link](https://huggingface.co/)
* Modello Bert [link](https://huggingface.co/bert-base-multilingual-uncased)
* Spacy [link](https://spacy.io/)
* Doccano [link](https://github.com/doccano/doccano)
* USDA FoodData[link](https://fdc.nal.usda.gov/)
* GialloZafferano [link](https://www.giallozafferano.it/)
* Mysia.info [link](https://www.misya.info/)