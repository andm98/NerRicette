# NerRicette
![Imamgine 1](assets/imgs/robot.png?raw=true "Bot")
[a link](https://it.freepik.com/vettori-gratuito/illustrazione-del-concetto-di-android_19880016.htm#query=robot&position=6&from_view=author") Immagine di storyset

La repository contiene NerRicette un modello per il riconoscimento di tag relativi alla cucina e la stima dei valori nutrizionali di 
ricette.
Il riconoscimento avviene tramite un modello BERT multilinguaggio, addestrato nella fase di fine-tuning 
nell'assegnazione di uno dei seguenti tag ai token della frase in input:
| Tag           | Descrizione                                              |
| ------------- | -------------------------------------------------------- |
| B-ING         | Nome dell'ingrediente                                    |
| Content Cell  | Content Cell                                             |




Riproducibilità

1- Eseguire il notebook 'Creazione dataset'
2- Annotare i dati
3- Eseguire il notebook 'Creazione dataset' 
4- Eseguire il notebook 'Addestramento modello'

è possibile utilizzare i dati annotati in ... ed eseguire la fase 4


Risorse utilizzate:
-recipescraper
-hugginface e modello
-spacy





La cartella data contiene i dati annotati con il tool Doccano e i dati ottenuti con scraping dai siti Giallo Zafferano e Mysia.info.
La cartella colab contiene i notebook utilizzati per lo scraping e l'addestramento del modello.
è possibile testare il modello al seguente link: 
[a link]()

Il notebook permette di estrarre i tag da una lista di ingredienti o da un link di una ricetta e di stimare 
i valori nutrizionali.

La valutazione dei valori nutrizionali avviene tramite euristica dai dataset USDA.
[a link]()
