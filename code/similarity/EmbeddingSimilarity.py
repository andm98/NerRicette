from NerRicette.code.abstract_class.SimilarityStrategy import SimilarityStrategy
import numpy as np
import torch
from scipy.spatial.distance import cosine
from transformers import AutoTokenizer, AutoModel
import spacy
from django.conf import settings
from pathlib import Path
class EmbeddingSimilarity(SimilarityStrategy):
    def __init__(self):
        PATH =   PATH = Path(settings.BASE_DIR, 'NerRicette','code', 'model')
        
        self.model =  AutoModel.from_pretrained(PATH, output_hidden_states=True)
        self.tokenizer = AutoTokenizer.from_pretrained(PATH)
       
    
    def compare(self, str1a, str2a):
        str1_descr = self.getWordEmb(" ".join(str1a).lower())
        str2_descr = self.getWordEmb(" ".join(str2a).lower())
        distance = cosine(str1_descr, str2_descr)
        return (100-distance)/100
   
    def compareWithTags(self, str1a, str2a, tags1, tags2):
        list1 = list(map(lambda tag: tag["self"].lower() if tag["self"] is not None else "", tags1)) if tags1 is not None else []
        list2 = list(map(lambda tag: tag["self"].lower() if tag["self"] is not None else "", tags2)) if tags2 is not None else []
        diff = set(list2).difference(set(list1))
        anc2 = sum(list(map(lambda tag: self.getWordEmb(tag), diff)))*2 if len(diff)!=0 else None
        str1_descr = self.getWordEmb(" ".join(str1a).lower())
        str2_descr = self.getWordEmb(" ".join(str2a).lower()) - anc2 if anc2 is not None else self.getWordEmb(" ".join(str2a).lower())
        distance = cosine(str1_descr, str2_descr) 
        return (100-distance)/100
    
    def isPresent(self, str1a, str2a):
        print("to do")
        
    def get_hidden_states(self, encoded, model, layers):
        with torch.no_grad():
            output = model(**encoded)
        # Get all hidden states
        states = output.hidden_states
        # Stack and sum all requested layers
        output = torch.stack([states[i] for i in layers]).mean(0).squeeze()
        # Only select the tokens that constitute the requested word
        word_tokens_output = output
        return word_tokens_output.mean(dim=0)
 
 
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

