from ...promptsManager.prompt1 import Prompt1
from ..client import Client
from ...promptsManager.propmtBase import prompts

class AligeAllianzAhorro(Client):
    def __init__(self) -> None:
        pass

    def obtenerPrompt(self, promptKey):
        if promptKey == 'Comparativa de rendimiento entre medios':
            promptManager = Prompt1()
            return promptManager.createPrompt([[""],["1"], [["11"], ["11"], ["1111"]], [["111"],["111"]], [[["111"], ["1111"], ["1"]]]])
        else:
            return prompts[promptKey]