from NerRicette.code.abstract_class.SimilarityStrategy import SimilarityStrategy
import spacy

class LemmaSimilarity(SimilarityStrategy):
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
    def compare(self, str1s, str2s):
        doc1 = self.nlp(" ".join(str1s).lower())
        lemmatized_sentence1 = " ".join([token.lemma_ for token in doc1]) 
        doc2 = self.nlp(" ".join(str2s).lower())
        lemmatized_sentence2 = " ".join([token.lemma_ for token in doc2]) 
        return self.DistBatra(lemmatized_sentence1, lemmatized_sentence2)
      
    
    def isPresent(self, str1s, str2s):
        THRESHOLD = 1/len(str1s) if len(str1s)> 0 else 1
        doc1 = self.nlp(" ".join(str1s).lower())
        lemmatized_sentence1 = " ".join([token.lemma_ for token in doc1]) 
        doc2 = self.nlp(" ".join(str2s).lower())
        lemmatized_sentence2 = " ".join([token.lemma_ for token in doc2]) 
        return self.DistBatra(lemmatized_sentence1, lemmatized_sentence2) >= THRESHOLD
 

    
    def DistBatra(self, str1, str2):
        str1 = set(str1.split())
        str2 = set(str2.split())
        if len(str1)>0:
            return float(len(str1 & str2)) / len(str1)
        return 0