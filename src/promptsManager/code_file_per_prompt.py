import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

prompt1 = PROJECT_ROOT / 'optimization' / 'codigo' / 'prompt1.py'

# prompt1 = os.path.join('..', 'optimization', 'codigo', 'prompt1.py')
# prompt2 = os.path.join('..', 'optimization', 'codigo', 'prompt2.py')
# prompt3 = os.path.join('..', 'optimization', 'codigo', 'prompt3.py')
# prompt4 = os.path.join('..', 'optimization', 'codigo', 'prompt4.py')
# ruta_normalizada_prompt1 = os.path.normpath(prompt1) 
# ruta_normalizada_prompt2 = os.path.normpath(prompt2)
# ruta_normalizada_prompt3 = os.path.normpath(prompt3)
# ruta_normalizada_prompt4 = os.path.normpath(prompt4)

def leer_prompt1():
    return prompt1.read_text(encoding='utf-8')
    
def leer_prompt2():
    # with open(ruta_normalizada_prompt2, 'r') as archivo:
    #     return archivo.read()
    ...
    
def leer_prompt3():
    # with open(ruta_normalizada_prompt3, 'r') as archivo:
    #     return archivo.read()
    ...
    
def leer_prompt4():
    # with open(ruta_normalizada_prompt4, 'r') as archivo:
    #     return archivo.read()
    ...

code = {
    'Comparativa de rendimiento entre medios': leer_prompt1(),
    'Mejor y peor campaña de los últimos 7 días': leer_prompt2(),
    'Análisis de Variación de CVR': leer_prompt3(),
    'Reporte de Análisis Publicitario': leer_prompt4()
}