from NerRicette.code.abstract_class.SimilarityStrategy import SimilarityStrategy
import spacy

class LemmaSimilarity(SimilarityStrategy):
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
    def compare(self, str1a, str2a):
        doc1 = self.nlp(" ".join(str1a).lower())
        lemmatized_sentence1 = " ".join([token.lemma_ for token in doc1]) 
        doc2 = self.nlp(" ".join(str2a).lower())
        lemmatized_sentence2 = " ".join([token.lemma_ for token in doc2]) 
        return self.DistBatra(lemmatized_sentence1, lemmatized_sentence2)
      
    def compareWithTags(self, str1a, str2a, tags1, tags2):
       return self.compare(str1a, str2a)
    
    def isPresent(self, str1a, str2a):
        THRESHOLD = 1/len(str1a) if len(str1a)> 0 else 1
        lemma1_a = []
        lemma2_a = []
        for str in str1a:
            doc_1 = self.nlp(str.lower())
            for token in doc_1:
              lemma1_a.append(token.lemma_)    
        for str in str2a:
            doc_2 = self.nlp(str.lower())
            for token in doc_2:
              lemma2_a.append(token.lemma_)    
        lemmatized_sentence1 = " ".join(lemma1_a)
        lemmatized_sentence2 = " ".join(lemma2_a)  
        return self.DistBatra(lemmatized_sentence1, lemmatized_sentence2) >= THRESHOLD
 
    def DistBatra(self, str1, str2):
        str1 = set(str1.split())
        str2 = set(str2.split())
        if len(str1)>0:
            return float(len(str1 & str2)) / len(str1)
        return 0