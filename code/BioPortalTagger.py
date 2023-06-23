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
        self.api_key = 'c74be9f9-108a-4eed-bee3-19feedd5ccec'
        self.url = 'https://data.bioontology.org/annotator'
    
    
    def matchIngredient(self, str):
        print("to do")
 
    
    def getSemanticTag(self, ing):
        time.sleep(5)
        print("attendi tag semantici...")
        tags = None
        try:
            req = requests.get(self.getQuery(ing))
            if(req.status_code != 200):
                print("Superato il limite di chiamate dell'api BioPortal")
                return None
            tags = json.loads(req.text)
            tags = list(map(lambda tag: {
                "self": tag["annotatedClass"]["@id"],
                "ancestor": tag["hierarchy"][0]["annotatedClass"]["@id"]
            }, tags))
            print(ing)
            print(tags)
            print("______________________________________________")
        except:
            time.sleep(20)
  
        return tags
        
            
    def setSemanticTag(self, ing, tags):
        print("to do")
    def getQuery(self,text):
        #ogni singolo ingrediente dovrebbe essere separato da & OF SNOMEDCT
        return self.url+"?text="+urllib.parse.quote(text)+"&apikey="+self.api_key+"&ontologies=OF&longest_only=true&exclude_numbers=false&whole_word_only=false&exclude_synonyms=false&expand_class_hierarchy=true&class_hierarchy_max_level=1"