from abc import ABC, abstractmethod
 
class NutritionalDataset(ABC):
    
    @abstractmethod
    def matchIngredient(self, str, first_strategy, alt_strategy):
        pass
 
    @abstractmethod
    def getNutritional(self, ing, first_strategy, alt_strategy):
        pass
    
    @abstractmethod
    def setNutritional(self, ing, nutrs):
        pass