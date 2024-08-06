from refactor_library.level_one import LevelOne
from refactor_library.level_two import LevelTwo
from refactor_library.level_three import LevelThree

class RefactorFactory:
    @staticmethod
    def chooseLevel(level:str):
        
        if level == "1.1" or level == "1.2":
            return LevelOne()
        
        elif level == "2.1":
            return LevelTwo()
        
        elif level == "3.1" or level == "3.2":
            return LevelThree()
        else:
            raise NotImplementedError(f"Level{level} not implemented")
    