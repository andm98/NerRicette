# NerRicette
![Bot](assets/imgs/robot.png?raw=true "Bot")

La repository contiene NerRicette, un modello per il riconoscimento di tag relativi alla cucina e la stima di valori nutrizionali.
Il riconoscimento avviene tramite un modello BERT multilinguaggio, addestrato nella fase di fine-tuning 
nella classificazione dei token in input con i seguenti tag:
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


La stima dei valori nutrizionali avviene tramite l'associazione degli ingredienti
riconosciuti con quelli presenti nei dataset USDA.

É possibile testare il modello al seguente link:
[Prova il modello](https://colab.research.google.com/drive/1uDFF2jacVXE4TaxSXtPhCpB4YNwkganj#)

1. Eseguire il notebook 'Creazione dataset'
2. Annotare i dati
3. Eseguire il notebook 'Creazione dataset annotato' 
4. Eseguire il notebook 'Addestramento modello'

É possibile utilizzare i dati annotati in ... ed eseguire direttamente la fase 4


Risorse utilizzate:
* recipescraper
* hugginface
* modello
* spacy
* usda
* doccano






La cartella data contiene i dati annotati con il tool Doccano e i dati ottenuti con scraping dai siti Giallo Zafferano e Mysia.info.
La cartella colab contiene i notebook utilizzati per lo scraping e l'addestramento del modello.
è possibile testare il modello al seguente link: 
[a link]()

Il notebook permette di estrarre i tag da una lista di ingredienti o da un link di una ricetta e di stimare 
i valori nutrizionali.

La valutazione dei valori nutrizionali avviene tramite euristica dai dataset USDA.
[a link]()
