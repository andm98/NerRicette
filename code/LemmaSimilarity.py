from NerRicette.code.abstract_class.SimilarityStrategy import SimilarityStrategy
import spacy

class LemmaSimilarity(SimilarityStrategy):
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
    def compare(self, str1, str2):
        doc1 = self.nlp(str1.lower())
        lemmatized_sentence1 = " ".join([token.lemma_ for token in doc1]) 
        doc2 = self.nlp(str2.lower())
        lemmatized_sentence2 = " ".join([token.lemma_ for token in doc2]) 
        return self.DistBatra(lemmatized_sentence1, lemmatized_sentence2)
      
    
    def isPresent(self, str1, str2):
        doc1 = self.nlp(str1.lower())
        lemmatized_sentence1 = " ".join([token.lemma_ for token in doc1]) 
        doc2 = self.nlp(str2.lower())
        lemmatized_sentence2 = " ".join([token.lemma_ for token in doc2]) 
        return self.DistBatra(lemmatized_sentence1, lemmatized_sentence2) == 1
 

    
    def DistBatra(self, str1, str2):
        str1 = set(str1.split())
        str2 = set(str2.split())
        if len(str1)>0:
            return float(len(str1 & str2)) / len(str1)
        return 0