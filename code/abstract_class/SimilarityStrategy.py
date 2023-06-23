from abc import ABC, abstractmethod
 
class SimilarityStrategy(ABC):
 
    @abstractmethod
    def compare(self, str1, str2):
        pass
    
    @abstractmethod
    def compareWithTags(self, str1, str2, tags1, tags2):
        pass
    
    @abstractmethod
    def isPresent(self, str1, str2):
        pass