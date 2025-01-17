from ..config.proyectos_names import ProyectosNames, SubProyectosNames

class Manager():
        
    def obtenerPrompt(self, client, prompt):
        promptManager, _ = self.clientManager(client)
        return promptManager.obtenerPrompt(prompt)
    
    def clientManager(self, client):
        if client == ProyectosNames.PEIGO.value:
            from ..clientManager.peigo import Peigo
            return Peigo(), ProyectosNames.PEIGO.value
        elif client == ProyectosNames.ALIGE_ALLIANZ_AHORRO.value:
            from ..clientManager.alige.alige_allianz_ahorro import AligeAllianzAhorro
            return AligeAllianzAhorro(), ProyectosNames.ALIGE_ALLIANZ_AHORRO.value
        elif client == ProyectosNames.ALIGE_ALLIANZ_VIDA.value:
            from ..clientManager.alige.alige_allianz_vida import AligeAllianzVida
            return AligeAllianzVida(), ProyectosNames.ALIGE_ALLIANZ_VIDA.value
        elif client == ProyectosNames.ALIGE_SKANDIA_AHORRO.value:
            from ..clientManager.alige.alige_skandia_ahorro import AligeSkandiaAhorro
            return AligeSkandiaAhorro(), ProyectosNames.ALIGE_SKANDIA_AHORRO.value
        elif client == ProyectosNames.DEMO.value:
            from ..clientManager.peigo import Peigo
            return Peigo(), ProyectosNames.DEMO.value
        elif client == ProyectosNames.TRADERPAL.value:
            from ..clientManager.traderpal import TraderPal
            return TraderPal(), ProyectosNames.TRADERPAL.value
        else:
            return None
        
    def obtenerFechas(self, client, prompt):
        promptManager, cliente_actual = self.clientManager(client)
        dic = promptManager.obtenerFechas(prompt, cliente_actual)
        result = 'Periodo de fechas:\n'
        for key, value in dic.items():
            result += f'{key}: {value}\n'
        
        return result
            
        
            
    