from NerRicette.code.abstract_class.SimilarityStrategy import SimilarityStrategy
import numpy as np
import torch
from scipy.spatial.distance import cosine
from transformers import AutoTokenizer, AutoModel
class EmbeddingSimilarity(SimilarityStrategy):
    def __init__(self):
        PATH = './'
        self.model =  AutoModel.from_pretrained(PATH + "model/", output_hidden_states=True)
        self.tokenizer = AutoTokenizer.from_pretrained(PATH + "model/")
    
    def compare(self, str1s, str2s):
        str1_descr = self.getWordEmb(" ".join(str1s).lower())
        str2_descr = self.getWordEmb(" ".join(str2s).lower())
        distance = cosine(str1_descr, str2_descr)
        return (100-distance)/100
    
    def isPresent(self, str1s, str2s):
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

