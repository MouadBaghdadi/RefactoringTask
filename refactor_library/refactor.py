from refactor_library.level_one import LevelOne

class RefactorFactory:
    @staticmethod
    def chooseLevel(level:str):
        
        if level == "1.1" or level == "1.2":
            return LevelOne()
        
        else :
            raise NotImplementedError(f"Level{level} not implemented")
    