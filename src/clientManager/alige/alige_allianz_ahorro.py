from ...promptsManager.prompt1 import Prompt1
from ..client import Client

class AligeAllianzAhorro(Client):
    def __init__(self) -> None:
        pass

    def obtenerPrompt(self, promptKey):
        if promptKey == 'Comparativa de rendimiento entre medios':
            promptManager = Prompt1()
            return promptManager.createPrompt() ## TODO completar con el prompt de alige allianz ahorro