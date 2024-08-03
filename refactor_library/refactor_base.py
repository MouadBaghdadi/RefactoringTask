from abc import ABC, abstractmethod
class Refactor(ABC):
    @abstractmethod
    def refactor(self,text:str)->str:
        pass
    
    

    