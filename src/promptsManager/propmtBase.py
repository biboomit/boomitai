prompts = {
    'Comparativa de rendimiento entre medios': f"""
Analiza los costos diarios de un conjunto de datos publicitarios a nivel de plataforma y proporciona puntos de interés. 
Identifica atentamente la fecha más reciente respecto a hoy (tendría que ser la fecha de ayer. Por ejemplo, si hoy es 16 de julio, la fecha máxima tendría que ser 15 de julio.) y realiza todo el análisis comparando los datos de los últimos 7 días con los datos de los 7 días inmediatamente anteriores. Si no hay datos de la fecha de ayer, realiza todas las comparaciones tomando la última fecha que haya como ayer.
Sigue estas instrucciones:

1. Exclusión de datos:
   - Excluye los medios sin inversión o con inversión prácticamente nula (0 o cercana a 0).
   - En el caso de que haya datos con 0 eventos_objetivo, exclúyelos del análisis. 

2. Plataformas a analizar:
   - Incluye todas las plataformas presentes en los datos (por ejemplo, TikTok, Google, Meta/Facebook, etc.).

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

4. Puntos de interés a destacar:
   - Para cada plataforma, analiza y reporta:
     a) La variación porcentual del costo medio entre períodos
     b) La magnitud del cambio (significativo, moderado o estable)
     c) El contraste con la variación en la inversión
   - Ejemplos de análisis esperados:
     * "Facebook tuvo una disminución significativa del 20% en el costo medio, a pesar de mantener una inversión estable"
     * "TikTok mostró un aumento moderado del 8% en el costo medio, mientras que su inversión aumentó un 15%"
     * "Google mantuvo costos estables con una variación de solo 2%, con una inversión similar en ambos períodos"

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
Se recomienda continuar monitoreando las estrategias de inversión en Meta y Google Ads, dado el aumento en la eficiencia de costos. Para TikTok Ads, aunque la eficiencia ha mejorado, sería prudente investigar formas de optimizar aún más la inversión para mantener esta tendencia positiva.""",
            'Mejor y peor campaña de los últimos 7 días': f"""
Analiza el rendimiento de las campañas publicitarias para identificar los casos de mayor y menor eficiencia en términos de costo por objetivo, proporcionando un análisis comparativo detallado.

1. Criterios de exclusión:
   - Eliminar del análisis:
     * Campañas sin inversión (inversión = 0)
     * Campañas con eventos_objetivo = 0
     * Campañas con menos de 3 días de datos en cualquiera de los períodos
     
2. Períodos de análisis:
   - Período actual: últimos 7 días hasta la fecha más reciente con datos
   - Período anterior: 7 días previos al período actual
   
3. Métricas de evaluación:
   a) Cálculo del costo por objetivo para cada campaña individual:
      * Período actual (últimos 7 días):
        - Costo por objetivo = (Suma de inversión de la campaña en los últimos 7 días) / (Suma de eventos_objetivo de la campaña en los últimos 7 días)
      * Período anterior (7 días previos):
        - Costo por objetivo = (Suma de inversión de la campaña en los 7 días anteriores) / (Suma de eventos_objetivo de la campaña en los 7 días anteriores)
      * Realizar este cálculo para cada campaña de forma independiente
      
   b) Variación porcentual por campaña:
      * Fórmula para cada campaña individual: 
        ((Costo por objetivo actual de la campaña - Costo por objetivo anterior de la campaña) / Costo por objetivo anterior de la campaña) * 100
      * Redondear a dos decimales
      * Calcular solo si la campaña tiene datos en ambos períodos

4. Criterios de selección:
   a) Mejor campaña:
      * Menor costo por objetivo en el período actual
      * Requisitos mínimos:
        - Datos completos en ambos períodos

   b) Peor campaña:
      * Mayor costo por objetivo en el período actual
      * Mismos requisitos mínimos que la mejor campaña

5. Datos a reportar por campaña:
   - Nombre de la campaña
   - Plataforma publicitaria
   - Costo por objetivo actual
   - Costo por objetivo anterior
   - Variación porcentual
   - Inversión total del período
   - Total de eventos_objetivo
   - Días activos en el período

6. Formato de respuesta:
   a) Resumen general:
      - Período total analizado (fechas específicas)
      - Detalle de campañas:
        * Número total inicial de campañas antes de exclusiones
        * Número final de campañas analizadas después de exclusiones
        * Desglose detallado de exclusiones:
          - Primero reportar el total de campañas excluidas
          - Luego desglosar por criterio de exclusión, considerando que una campaña puede cumplir múltiples criterios
          - Para campañas que cumplen múltiples criterios de exclusión, contabilizarlas en cada categoría aplicable
        
        Formato de reporte de exclusiones:
        "De un total de [X] campañas iniciales, se excluyeron [Y] campañas:
        - [N1] campañas sin inversión
        - [N2] campañas sin eventos_objetivo
        - [N3] campañas con datos incompletos
        Nota: La suma de exclusiones puede ser mayor al total de campañas excluidas ya que una campaña puede cumplir múltiples criterios de exclusión.
        
        Se analizaron las [Z] campañas restantes."

   b) Mejor campaña:
      [Nombre de la Campaña] - [Plataforma]:
      * Costo por objetivo actual: $XX.XX
      * Costo por objetivo anterior: $XX.XX
      * Variación: XX.XX%
      * Métricas adicionales:
        - Inversión total: $XX.XX
        - Total eventos_objetivo: XX
        - Días activos: X/7

   c) Peor campaña:
      [Nombre de la Campaña] - [Plataforma]:
      * Costo por objetivo actual: $XX.XX
      * Costo por objetivo anterior: $XX.XX
      * Variación: XX.XX%
      * Métricas adicionales:
        - Inversión total: $XX.XX
        - Total eventos_objetivo: XX
        - Días activos: X/7

   d) Análisis contextual:
      - Factores relevantes que pueden explicar el rendimiento
      - Consideraciones importantes sobre los datos
      - Patrones o tendencias identificadas

Ejemplo de respuesta:

Análisis de Mejor y Peor Campaña: 21-27 octubre 2024

Resumen general:
De un total de 25 campañas iniciales, se excluyeron 21 campañas:
- 15 campañas sin inversión
- 12 campañas sin eventos_objetivo
- 3 campañas con datos incompletos
Nota: La suma de exclusiones (30) es mayor al total de campañas excluidas (21) ya que 9 campañas no tenían ni inversión ni eventos_objetivo.

Se analizaron las 4 campañas restantes que cumplieron todos los criterios de inclusión.

Mejor campaña:
"Promoción Otoño 2024" - Meta
* Costo por objetivo actual: $12.45
* Costo por objetivo anterior: $15.67
* Variación: -20.55%
* Métricas adicionales:
  - Inversión total: $2,500
  - Total eventos_objetivo: 201
  - Días activos: 7/7

Peor campaña:
"BOOMIT_PEIG_EC_GADS_ADQUISI_ANDROID_(FIREBASE-PRIMTARJ)_BROA_REGIST_UAC_SPA" - Google Ads
* Costo por objetivo actual: $45.67
* Costo por objetivo anterior: $38.92
* Variación: +17.34%
* Métricas adicionales:
  - Inversión total: $1,850
  - Total eventos_objetivo: 41
  - Días activos: 7/7

Análisis contextual:
La mejor campaña muestra una optimización efectiva con una reducción significativa en el costo por objetivo, manteniendo un volumen alto de eventos. La peor campaña muestra señales de saturación con costos crecientes y menor eficiencia en la conversión de inversión a objetivos.""",
            'Análisis de Variación de CVR': f"""
Objetivo
Realizar un análisis completo de la campaña con mejor CVR para TODO el periodo de tiempo, incluyendo todas sus métricas y correlaciones en una única respuesta estructurada.

## Instrucciones para el Asistente

### 1. Análisis Previo
Antes de generar la respuesta, debes:
- Identificar la campaña con mejor CVR promedio
- Calcular todas las métricas generales
- Realizar análisis de correlaciones
- Determinar umbrales de inversión y eventos
- Calcular promedios por encima y debajo de umbrales
- Identificar días de mejor y peor rendimiento

### 2. Formato de Respuesta Única
Después de realizar todos los cálculos, presentar una única respuesta estructurada según el siguiente formato:

Resumen de Análisis: Campaña con Mejor CVR
Período analizado: [fecha inicio] al [fecha fin]

Campaña: [Nombre]

Métricas de Rendimiento:
- CVR promedio: XX.XX%
- Mejor día: [fecha] (CVR: XX.XX%)
- Peor día: [fecha] (CVR: XX.XX%)

Métricas Generales:
- Inversión total: $XXX.XX
- Inversión promedio diaria: $XXX.XX
- Total de eventos: XXX
- Promedio diario de eventos: XX.X
- Costo por evento promedio: $XX.XX

Análisis de Correlaciones:
1. Relación Inversión-CVR:
   - Coeficiente de correlación: X.XX
   - Comportamiento con inversión > $XXX: CVR promedio XX.XX%
   - Comportamiento con inversión ≤ $XXX: CVR promedio XX.XX%
   - Interpretación: [breve descripción de la relación observada]

2. Relación Volumen-CVR:
   - Coeficiente de correlación: X.XX
   - Comportamiento con eventos > XX: CVR promedio XX.XX%
   - Comportamiento con eventos ≤ XX: CVR promedio XX.XX%
   - Interpretación: [breve descripción de la relación observada]

## Ejemplo de Respuesta Óptima:

Resumen de Análisis: Campaña con Mejor CVR
Período analizado: 1 al 15 de octubre 2024

Campaña: CAMPAIGN_NAME_001

Métricas de Rendimiento:
- CVR promedio: 18.45%
- Mejor día: 8 de octubre (CVR: 22.31%)
- Peor día: 3 de octubre (CVR: 15.12%)

Métricas Generales:
- Inversión total: $5,234.56
- Inversión promedio diaria: $348.97
- Total de eventos: 856
- Promedio diario de eventos: 57.1
- Costo por evento promedio: $6.11

Análisis de Correlaciones:
1. Relación Inversión-CVR:
   - Coeficiente de correlación: -0.15
   - Comportamiento con inversión > $350: CVR promedio 17.89%
   - Comportamiento con inversión ≤ $350: CVR promedio 19.01%
   - Interpretación: Existe una correlación negativa débil, sugiriendo que el CVR no depende significativamente del nivel de inversión

2. Relación Volumen-CVR:
   - Coeficiente de correlación: 0.78
   - Comportamiento con eventos > 57: CVR promedio 20.12%
   - Comportamiento con eventos ≤ 57: CVR promedio 16.78%
   - Interpretación: Existe una correlación positiva fuerte entre el volumen de eventos y el CVR

## Notas Importantes para el Asistente
1. Realizar todos los cálculos y análisis antes de comenzar a escribir la respuesta
2. Presentar una única respuesta completa y estructurada
3. No incluir pasos intermedios ni cálculos en la respuesta
4. Mantener consistencia en el formato y decimales:
   - Porcentajes: dos decimales
   - Montos: dos decimales
   - Eventos: un decimal para promedios, números enteros para totales
   - Correlaciones: dos decimales
5. No incluir recomendaciones ni sugerencias de optimización""",
"Reporte de Análisis Publicitario": f"""
Objetivo
Realizar un análisis detallado del rendimiento publicitario a nivel de plataforma para informar al equipo de estrategia de comunicación y publicidad digital sobre las acciones específicas a implementar.

1. Criterios de Análisis Temporal
- Identificar la fecha más reciente disponible (fecha de ayer)
- Si no hay datos de ayer, usar la última fecha disponible como referencia

2. Criterios de Exclusión
- Eliminar del análisis:
  * Plataformas sin inversión o con inversión prácticamente nula (0 o cercana a 0).

3. Métricas de Evaluación por Plataforma
3.1 Métricas Base
Para todo el periodo, calcula:
- Volumen total de eventos_objetivo
- Costo medio por evento_objetivo = Inversión total / Total eventos_objetivo
- Costo medio por instalación = Inversión total / Total instalaciones
- Inversión total
- CVR medio = Total eventos_objetivo / Total instalaciones
- Correlación entre Inversión y CVR

3.2 Análisis de Variaciones
Calcular para cada métrica:
- Variación porcentual entre períodos:
  * Costo medio por evento_objetivo
  * Volumen de eventos_objetivo
  * Costo medio por instalación
  * Volumen de instalaciones
  * Inversión total

3.3 Clasificación de Variaciones
Para cada variación porcentual:
- Tendencia:
  * Creciente: >5%
  * Decreciente: <-5%
  * Estable: entre -5% y 5%
- Magnitud del cambio:
  * Significativo: >15%
  * Moderado: 5-15%
  * Estable: <5%

4. Análisis de Saturación de Medio
Evaluar para cada plataforma:
- Relación inversión-resultados:
  * Análisis de variaciones en costos y volúmenes de instalación
  * Análisis de variaciones en costos y volúmenes de eventos_objetivo
  * Identificación de relaciones no lineales entre inversión y resultados

5. Formato de Respuesta

5.1 Resumen General
- Período total analizado (fechas específicas)
- Resumen ejecutivo de tendencias principales por plataforma
- Número total de plataformas analizadas

5.2 Análisis por Plataforma
Para cada plataforma:
[Nombre de la Plataforma]:
1. Análisis de Tendencias:
   - Variaciones porcentuales de todas las métricas
   - Clasificación de cambios (significativo/moderado/estable)
   - Contraste con variaciones en inversión

2. Análisis de Saturación:
   - Evaluación de la relación inversión-resultados
   - Identificación de puntos de saturación
   - Eficiencia en la conversión

5.3 Conclusiones y Recomendaciones
- Análisis de redistribución de inversión entre plataformas
- Tendencias críticas a monitorear
- Evaluación global de eficiencia:
  * Identificación de métricas más y menos eficientes
  * Recomendaciones específicas basadas en datos
  * Priorización de acciones inmediatas

6. Notas Importantes
- Todos los porcentajes deben presentarse con dos decimales
- Montos monetarios con dos decimales
- Eventos en números enteros
- Correlaciones con dos decimales


Respuesta optima:
Período Total Analizado: Del 19 de octubre de 2024 al 26 de octubre de 2024 comparado con el 12 de octubre de 2024 al 18 de octubre de 2024.
Tendencias Principales:
Google Ads: Incremento significativo en inversión total (31.87%) y eventos objetivo (18.13%), pero disminución moderada en CVR medio (-8.29%).
Meta: Estabilidad en la mayoría de las métricas con un ligero aumento en CVR medio (2.81%).
TikTok Ads: Aumento significativo en instalaciones (15.63%) con una disminución moderada en CVR medio (-9.88%).
Número Total de Plataformas Analizadas: 3
Análisis por Plataforma:

Google Ads:

Análisis de Tendencias:

Inversión total aumentó un 31.87%, eventos objetivo un 18.13%, e instalaciones un 28.81%.
CVR medio disminuyó moderadamente (-8.29%).
Costo medio por evento aumentó moderadamente (11.64%), mientras que el costo medio por instalación se mantuvo estable (2.38%).
Análisis de Saturación:

Incremento en inversión resultó en un aumento significativo en eventos e instalaciones, pero con una eficiencia de conversión decreciente.
Meta:

Análisis de Tendencias:

Inversión total y eventos objetivo se mantuvieron estables.
Instalaciones disminuyeron ligeramente (-3.39%).
CVR medio aumentó levemente (2.81%).
Costo medio por evento e instalación mostraron estabilidad y un aumento moderado respectivamente.
Análisis de Saturación:

Relación inversión-resultados estable, pero con una ligera mejora en eficiencia de conversión.
TikTok Ads:

Análisis de Tendencias:

Inversión total se mantuvo estable.
Eventos objetivo aumentaron un 4.20% e instalaciones un 15.63%.
CVR medio disminuyó moderadamente (-9.88%).
Costo medio por evento se mantuvo estable, mientras que el costo medio por instalación disminuyó moderadamente (-13.52%).
Análisis de Saturación:

Aumento en instalaciones con una disminución en eficiencia de conversión.
Conclusiones y Recomendaciones:

Redistribución de Inversión: Considerar aumentar la inversión en Google Ads debido a su incremento en eventos e instalaciones, pero monitorear la eficiencia de conversión.
Tendencias Críticas a Monitorear: La eficiencia de conversión en TikTok Ads y Google Ads.
Evaluación Global de Eficiencia: Google Ads mostró un buen rendimiento en volumen, pero necesita mejorar en eficiencia de conversión. TikTok Ads debe enfocarse en mejorar su CVR medio.
Recomendaciones Específicas: Aumentar inversión en plataformas con crecimiento significativo en eventos e instalaciones, pero con atención a la eficiencia de conversión.
"""
        }