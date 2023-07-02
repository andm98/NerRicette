from NerRicette.code.abstract_class.SemanticTagger import SemanticTagger
from NerRicette.code.Utils import Utils
from NerRicette.code.QtyConverter import QtyConverter
import urllib
import requests
import json
import time

class BioPortalTagger(SemanticTagger):
    def __init__(self):
        self.utils = Utils()
        self.api_key = "c74be9f9-108a-4eed-bee3-19feedd5ccec"
        self.url = 'https://data.bioontology.org/annotator'
        
    
    
    def matchIngredient(self, str):
        print("to do")
 
    
    def getSemanticTag(self, ing, n_attempt=1):
        tags = None
        time.sleep(2)
        try:
            req = requests.get(self.getQuery(ing))
            if(req.status_code != 200):
                print("Superato il limite di chiamate dell'api BioPortal")
                return None
            tags = json.loads(req.text)
            tags = list(map(lambda tag: {
                "id": None,
                "concept": tag["annotatedClass"]["@id"].split('#')[1],
                "self": tag["annotatedClass"]["@id"],
                "ancestor":
                {
                    "id": None,
                    "self": tag["hierarchy"][0]["annotatedClass"]["@id"] if len(tag["hierarchy"])>0 else "",
                    "concept": tag["hierarchy"][0]["annotatedClass"]["@id"].split('#')[1] if len(tag["hierarchy"])>0 else "",
                }
            }, tags))    
        except:
            print("Eccezione")
            if(n_attempt<=2):
                print(n_attempt)
                time.sleep(10*n_attempt)
                self.getSemanticTag(ing, n_attempt+1)
            else:
                return None
        return tags
        
            
    def setSemanticTag(self, ing, tags):
        print("to do")
    def getQuery(self,text):
        #ogni singolo ingrediente dovrebbe essere separato da & OF SNOMEDCT
        return self.url+"?text="+urllib.parse.quote(text)+"&apikey="+self.api_key+"&ontologies=OF&longest_only=true&exclude_numbers=false&whole_word_only=false&exclude_synonyms=false&expand_class_hierarchy=true&class_hierarchy_max_level=1"