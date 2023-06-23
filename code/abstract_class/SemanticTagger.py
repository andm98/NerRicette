from abc import ABC, abstractmethod
 
class SemanticTagger(ABC):
    
    @abstractmethod
    def matchIngredient(self, str):
        pass
 
    @abstractmethod
    def getSemanticTag(self, ing):
        pass
    
    @abstractmethod
    def setSemanticTag(self, ing, tags):
        pass