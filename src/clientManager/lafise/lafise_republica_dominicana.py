from ...promptsManager.prompt1 import Prompt1
from ..client import Client
from ...promptsManager.propmtBase import prompts
import bbdd

class LafiseRepublicaDominicana(Client):
    def __init__(self) -> None:
        pass
    
    def obtenerPrompt(self, promptKey):
        return prompts[promptKey]
        
    def obtenerFechas(self, promptKey, client):
        if promptKey == 'Análisis de Variación de CVR': # se necesita el inicio y fin del periodo entero
            dates = bbdd.get_data_range(client)
            data_dict = dates.iloc[0].to_dict()
            return {
                'start_date': data_dict['period_previous_start'],
                'end_date': data_dict['period_current_end']
            }
        else:
            dates = bbdd.get_data_range(client)
            data_dict = dates.iloc[0].to_dict()
            return data_dict