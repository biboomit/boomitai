descripcion="""
Analiza los costos diarios de un conjunto de datos publicitarios a nivel de plataforma y proporciona puntos de interés. 
Identifica atentamente la fecha más reciente respecto a hoy (tendría que ser la fecha de ayer. Por ejemplo, si hoy es 16 de julio, la fecha máxima tendría que ser 15 de julio.) y realiza todo el análisis comparando los datos de los últimos 7 días con los datos de los 7 días inmediatamente anteriores. Si no hay datos de la fecha de ayer, realiza todas las comparaciones tomando la última fecha que haya como ayer.
Sigue estas instrucciones:
"""

paso1 = """
1. Exclusión de datos:
   - Excluye los medios sin inversión o con inversión prácticamente nula (0 o cercana a 0).
   - En el caso de que haya datos con 0 eventos_objetivo, exclúyelos del análisis. 
"""

paso2 = """
2. Plataformas a analizar:
   - Incluye todas las plataformas presentes en los datos (por ejemplo, TikTok, Google, Meta/Facebook, etc.).
"""

paso3 = """
3. Análisis por plataforma:
   - Para cada plataforma, calcula y reporta para ambos períodos de 7 días:
     Período anterior (especificar fechas):
     a) Costo medio por evento_objetivo = (Suma total de inversión del período) / (Suma total de eventos_objetivo del período)
        * Excluir del cálculo todas las filas donde inversión = 0 o eventos_objetivo = 0
     b) Inversión total del período
        * Excluir del cálculo todas las filas donde inversión = 0

     Período actual (especificar fechas):
     a) Costo medio por evento_objetivo = (Suma total de inversión del período) / (Suma total de eventos_objetivo del período)
        * Excluir del cálculo todas las filas donde inversión = 0 o eventos_objetivo = 0
     b) Inversión total del período
        * Excluir del cálculo todas las filas donde inversión = 0
     
   - Compara los períodos:
     * Calcula el porcentaje de variación del costo medio entre períodos usando las fórmulas ajustadas anteriores
     * Identifica si la tendencia es creciente (>5%), decreciente (<-5%) o estable (entre -5% y 5%)
     * Define si el cambio es significativo (>15% de variación) o moderado (5-15% de variación)
     * Calcula el porcentaje de variación de la inversión total entre períodos
"""

paso4 = """
4. Puntos de interés a destacar:
   - Para cada plataforma, analiza y reporta:
     a) La variación porcentual del costo medio entre períodos
     b) La magnitud del cambio (significativo, moderado o estable)
     c) El contraste con la variación en la inversión
   - Ejemplos de análisis esperados:
     * "Facebook tuvo una disminución significativa del 20% en el costo medio, a pesar de mantener una inversión estable"
     * "TikTok mostró un aumento moderado del 8% en el costo medio, mientras que su inversión aumentó un 15%"
     * "Google mantuvo costos estables con una variación de solo 2%, con una inversión similar en ambos períodos"
"""

paso5 = """
5. Formato de respuesta:
   Estructura tu respuesta de la siguiente manera:
   a) Resumen general:
      - Especificar el rango total de fechas analizadas
      - Indicar claramente los dos períodos que se comparan (período anterior y período actual)
      - Resumen de las tendencias principales observadas en las plataformas
   
   b) Análisis por plataforma:
      Para cada plataforma, usar el siguiente formato:
      [Nombre de la Plataforma]:
      Un párrafo que describa:
      * La dirección del cambio en el costo medio (aumento/disminución)
      * La magnitud del cambio (significativo/moderado/estable)
      * La relación con los cambios en la inversión
      * Interpretación de las implicaciones

   c) Conclusiones y recomendaciones basadas en el análisis.
"""

ejemplo ="""
Ejemplo de respuesta:

Resumen general:
Durante el período total analizado del 14 al 27 de octubre de 2024 (comparando el período anterior del 14 al 20 de octubre con el período actual del 21 al 27 de octubre), se observaron tendencias decrecientes en los costos medios por evento_objetivo en todas las plataformas, con variaciones significativas en Meta y Google Ads, y un cambio moderado en TikTok Ads.

Análisis por plataforma:

Meta:
Mostró una disminución significativa del 15.89% en el costo medio, mientras que la inversión promedio diaria aumentó un 29.55%. Esta divergencia sugiere una mejora en la eficiencia del gasto, ya que se logró reducir el costo por evento a pesar de un aumento en la inversión.

TikTok Ads:
Presentó una disminución moderada del 12.93% en el costo medio, con una ligera disminución del 4.00% en la inversión promedio diaria. Esto indica una mejora en la eficiencia, aunque el cambio en la inversión fue menos pronunciado.

Google Ads:
Experimentó una disminución significativa del 19.99% en el costo medio, con una inversión promedio diaria ligeramente menor en un 2.42%. La reducción en el costo medio sugiere una mejora notable en la eficiencia de la inversión.

Conclusiones y recomendaciones: 
Se recomienda continuar monitoreando las estrategias de inversión en Meta y Google Ads, dado el aumento en la eficiencia de costos. Para TikTok Ads, aunque la eficiencia ha mejorado, sería prudente investigar formas de optimizar aún más la inversión para mantener esta tendencia positiva.
"""


###################################################

from enum import Enum

class Titles(Enum):
   PASO1 = "paso1"
   PASO2 = "paso2"
   PASO3 = "paso3"
   PASO4 = "paso4"
   PASO5 = "paso5"

class Prompt1:
   def __init__(self):
      self.whitespace = "    "
      
      self.prompt = [
         # Paso 1: Exclusion de datos
         [
            "Excluye los medios sin inversión o con inversión prácticamente nula (0 o cercana a 0).",
            "Excluye los medios con 0 eventos_objetivo del análisis."
         ],
         # Paso 2: Plataformas a analizar  
         [
            "Incluye todas las plataformas presentes en los datos. Por ejemplo, TikTok, Google, Meta/Facebook, etc."
         ],
         # Paso 3: Analisis por plataforma
         [
            # Calculos comparación períodos
            [
               "Costo medio por evento_objetivo = (Suma total de inversión del período) / (Suma total de eventos_objetivo del período)",
               "Inversión total del período"
            ],
            # Calculos período actual
            [
               "Costo medio por evento_objetivo = (Suma total de inversión del período) / (Suma total de eventos_objetivo del período)", 
               "Inversión total del período"
            ],
            # Comparación períodos
            [
               "Calcula el porcentaje de variación del costo medio entre períodos usando las fórmulas ajustadas anteriores",
               "Identifica si la tendencia es creciente (>5%), decreciente (<-5%) o estable (entre -5% y 5%)",
               "Define si el cambio es significativo (>15% de variación) o moderado (5-15% de variación)",
               "Calcula el porcentaje de variación de la inversión total entre períodos"
            ]
         ],
         # Paso 4: Puntos de interés
         [
            [
               "a) La variación porcentual del costo medio entre períodos",
               "b) La magnitud del cambio (significativo, moderado o estable)",
               "c) El contraste con la variación en la inversión"
            ]
         ],
         # Paso 5: Formato respuesta
         [
            [
               # Resumen general
               [
                     "- Especificar el rango total de fechas analizadas",
                     "- Indicar claramente los dos períodos que se comparan (período anterior y período actual)",
                     "- Resumen de las tendencias principales observadas en las plataformas"
               ],
               # Análisis por plataforma
               [
                     "* La dirección del cambio en el costo medio (aumento/disminución)",
                     "* La magnitud del cambio (significativo/moderado/estable)", 
                     "* La relación con los cambios en la inversión"
               ]
            ]
         ]
      ]
      # [[0101], [111]]
      
      self.titles = [
         "Exclusion de datos:",
         "Plataformas a analizar:",
         f'Analisis por plataforma: \n   - Para cada plataforma, calcula y reporta para ambos períodos de 7 días:',
         "Puntos de interés a destacar:",
         f'Formato de respuesta: \n{self.whitespace}Estructura tu respuesta de la siguiente manera:'
      ]
      
      self.subTitles = [
         [],
         [],
         [
            "- Calculos para el periodo anterior:",
            "- Calculos para el periodo actual:",
            "- Compara los períodos:"
         ],
         [
            "- Para cada plataforma, analiza y reporta:",
            "- Ejemplo de análisis esperado:"
         ],
         [
            [
               "Resumen general:",
               f'Analisis por plataforma: \n{self.whitespace}Para cada plataforma, usar el siguiente formato: \n{self.whitespace}[Nombre de la Plataforma]: \n{self.whitespace}Un párrafo que describa:',
               "Conclusiones y recomendaciones basadas en el análisis."
            ]
         ]
      ]
      
      self.whitespace = "   "
      
      # Ejemplo de uso: [[01], [0101], [000], [111], [1]]
      
   # el key es una cadena binaria que representa que elementos se quieren incluir
   # 0 -> no incluir
   # 1 -> incluir
   # el orden es de izquierda a derecha
   # Ejemplo:
   # 0000 -> no incluir nada
   # 0100 -> incluir solo el segundo componente de paso 1
   # 01 -> incluir solo el segundo componente de paso 1
   # 1111 -> incluir los primeros 4 componentes de paso 1
   # Ejemplo de uso: [[01], [0101], [000], [111], [1]]
   def createPrompt(self, keys):
      self.verifyKeys(keys)
      prompt = ""
      for i in range(len(keys)):
         prompt += (i+1).__str__() + "- " + self.titles[i] + "\n"
         prompt += self.obtainComponentHandler(keys[i], i) + "\n"
      return prompt
   
   # Ejemplo de uso: [0101]
   # Al verificar por == 1, si es cualquier otro valor se excluye asumiendo como 0
   def obtainComponent(self, key, paso, index = 0):
      prompt = ""
      if paso == 0 or paso == 1: #paso1 y paso2
         for i in range(len(key)):
            if key[i] == '1':
               prompt += self.whitespace * 2
               prompt += self.prompt[paso][i] + "\n"
      elif paso == 2 or paso == 3: #paso3 y paso4
         if '1' in key:
            prompt += self.whitespace
            prompt += self.subTitles[paso][index] + "\n"
            for i in range(len(key)):
               if key[i] == '1':
                  prompt += self.whitespace * 2
                  prompt += self.prompt[paso][index][i] + "\n"
      elif paso == 4: #paso5
         if '1' in key:
            prompt += self.whitespace
            prompt += chr(96 + (index + 1)) + ") " + self.subTitles[paso][0][index] + "\n"
            if index != 2: # El ultimo componente solo tiene un subtitulo
               for i in range(len(key)):
                  if key[i] == '1':
                     prompt += self.whitespace * 2
                     prompt += self.prompt[paso][0][index][i] + "\n"
      return prompt   
   
   def obtainComponentHandler(self, key, paso):
      if paso == 0 or paso == 1:
         return self.obtainComponent(key[0], paso)  
      if paso == 2 or paso == 3:
         prompt = ""
         for i in range(len(key)):
            prompt += self.obtainComponent(key[i][0], paso, i)
         return prompt
      if paso == 4:
         prompt = ""
         for i in range(len(key[0])):
            prompt += self.obtainComponent(key[0][i][0], paso, i)
         return prompt
      
      raise ValueError("El paso no existe")
   
   def verifyKeys(self, keys):
      if len(keys) != len(self.prompt):
         raise ValueError("El número de pasos no coincide con el número de keys")
      
      for i in range(len(keys)):
         if i in [0, 1]:
            if len(keys[i]) == 0:
               raise ValueError("No se puede tener un paso sin keys")
         elif i in [2, 3]:
            for j in range(len(keys[i])):
               if len(keys[i][j]) == 0:
                  raise ValueError("No se puede tener un paso sin keys")
         elif i == 4:
            for j in range(len(keys[i])):
               for k in range(len(keys[i][j])):
                  if len(keys[i][j][k]) == 0:
                     raise ValueError("No se puede tener un paso sin keys")
         else:
            raise ValueError("El paso no existe")
               
   def needSubTitles(self, paso):
      if paso in [2, 3, 4]:
         return True
      else: False