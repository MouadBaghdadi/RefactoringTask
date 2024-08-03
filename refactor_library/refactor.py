from refactor_library.level_one_one import LevelOneOne

class RefactorFactory:
    @staticmethod
    def chooseLevel(level:str):
        
        if level == "1.1":
            return LevelOneOne()
        
        else :
            raise NotImplementedError(f"Level{level} not implemented")
    