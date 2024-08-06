from abc import ABC, abstractmethod

class Refactor(ABC):
    """A base class for refactoring code that exposes a single public method refactor"""
    
    @abstractmethod
    def refactor(self, text: str) -> str:
       """
        Takes a string of code and returns a simplified version of the code.
        
        Parameters:
            text (str): The code to be refactored.
        
        Returns:
            str: The simplified version of the code.
        
        Examples:
        --------
        >>> refactor("print(2 + 2)")
        'print(4)'
        
        """

    
