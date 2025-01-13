from ...promptsManager.prompt1 import Prompt1
from ..client import Client
from ...promptsManager.propmtBase import prompts
import bbdd

class AligeSkandiaAhorro(Client):
    def __init__(self) -> None:
        pass
    
    def obtenerPrompt(self, promptKey):
        if promptKey == 'Comparativa de rendimiento entre medios':
            promptManager = Prompt1()
            return promptManager.createPrompt([[""],["1"], [["11"], ["11"], ["1111"]], [["111"],["111"]], [[["111"], ["1111"], ["1"]]]])
        else:
            return prompts[promptKey]
        
    def obtenerFechas(self, promptKey, client):
        if promptKey == 'Comparativa de rendimiento entre medios':
            dates = bbdd.get_data_range(client)
            data_dict = dates.iloc[0].to_dict()
            return data_dict
        elif promptKey == 'Mejor y peor campaña de los últimos 7 días':
            dates = bbdd.get_data_range(client)
            data_dict = dates.iloc[0].to_dict()
            return data_dict
        elif promptKey == 'Análisis de Variación de CVR': # se necesita el inicio y fin del periodo entero
            dates = bbdd.get_data_range(client)
            data_dict = dates.iloc[0].to_dict()
            return {
                'start_date': data_dict['period_previous_start'],
                'end_date': data_dict['period_current_end']
            }
        elif promptKey == 'Reporte de Análisis Publicitario':
            dates = bbdd.get_data_range(client)
            data_dict = dates.iloc[0].to_dict()
            return data_dict
        else:
            return None