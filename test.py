class Log:
    _instance = None
    txt = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    
    @staticmethod
    def print(value):
        Log.txt.append(value)
        print(Log.txt)        
    
Log.print(123)
Log.print(456)
