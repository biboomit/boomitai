from abc import ABC, abstractmethod

class Client(ABC):
    
    @abstractmethod
    def obtenerPrompt(self, promptKey):
        pass