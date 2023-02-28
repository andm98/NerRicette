from abc import ABC, abstractmethod
 
class NutritionalDataset(ABC):
 
    @abstractmethod
    def getNutritional(self, str):
        pass
    
    @abstractmethod
    def setNutritional(self, ingredient, sim_strategy):
        pass