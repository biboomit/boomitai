from ..config.proyectos_names import ProyectosNames, SubProyectosNames

class Manager():
        
    def obtenerPrompt(self, client, prompt):
        promptManager = self.clientManager(client)
        return promptManager.obtenerPrompt(prompt)
    
    def clientManager(self, client):
        if client == ProyectosNames.PEIGO.value:
            from ..clientManager.peigo import Peigo
            return Peigo()
        elif client == ProyectosNames.ALIGE_ALLIANZ_AHORRO.value:
            from ..clientManager.alige.alige_allianz_ahorro import AligeAllianzAhorro
            return AligeAllianzAhorro()
        elif client == ProyectosNames.ALIGE_ALLIANZ_VIDA.value:
            from ..clientManager.alige.alige_allianz_vida import AligeAllianzVida
            return AligeAllianzVida()
        elif client == ProyectosNames.ALIGE_SKANDIA_AHORRO.value:
            from ..clientManager.alige.alige_skandia_ahorro import AligeSkandiaAhorro
            return AligeSkandiaAhorro()
        elif client == ProyectosNames.DEMO.value:
            from ..clientManager.peigo import Peigo
            return Peigo()
        else:
            return None
        
        
        
            
    