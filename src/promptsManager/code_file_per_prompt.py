import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

prompt1 = PROJECT_ROOT / 'optimization' / 'codigo' / 'prompt1.py'
prompt2 = PROJECT_ROOT / 'optimization' / 'codigo' / 'prompt2.py'
prompt3 = PROJECT_ROOT / 'optimization' / 'codigo' / 'prompt3.py'
prompt4 = PROJECT_ROOT / 'optimization' / 'codigo' / 'prompt4.py'

def leer_prompt1():
    return prompt1.read_text(encoding='utf-8')
    
def leer_prompt2():
    return prompt2.read_text(encoding='utf-8')
    
def leer_prompt3():
    return prompt3.read_text(encoding='utf-8')
    
def leer_prompt4():
    return prompt4.read_text(encoding='utf-8')

code = {
    'Comparativa de rendimiento entre medios': leer_prompt1(),
    'Mejor y peor campaña de los últimos 7 días': leer_prompt2(),
    'Análisis de Variación de CVR': leer_prompt3(),
    'Reporte de Análisis Publicitario': leer_prompt4()
}