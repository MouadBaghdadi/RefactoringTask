from refactor_library.level_one import LevelOne
from refactor_library.level_two import LevelTwo

class RefactorFactory:
    @staticmethod
    def chooseLevel(level:str):
        
        if level == "1.1" or level == "1.2":
            return LevelOne()
        
        elif level == "2.1" or level == "2.2":
            return LevelTwo()
        else:
            raise NotImplementedError(f"Level{level} not implemented")
    