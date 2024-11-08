import os
import warnings
from pandas.errors import SettingWithCopyWarning
from datetime import datetime, timedelta
from PIL import Image
import streamlit as st
import bbdd
import pandas as pd
from obtener_file_id import upload_file
from openai import OpenAI
from utils import (
    delete_files,
    EventHandler,
    moderation_endpoint,
    render_custom_css,
    render_download_files,
    retrieve_messages_from_thread,
    retrieve_assistant_created_files,
)
 
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))
 
# Inicializa una variable de estado para controlar la visibilidad del cuadro de texto
show_password_input = True  # Initially show password input
# Inicializa una variable de estado para controlar la visibilidad del desplegable de clientes
show_client_dropdown = False
 
img_path = r"company_logo.png"
 
st.set_page_config(page_title="BOOMIT AI", page_icon="")
 
img = Image.open(img_path)
st.image(img, width=200, channels="RGB")
st.subheader("BOOMIT AI")
st.markdown("Analítica de marketing inteligente", help="[Source]()")
 
# Apply custom CSS
render_custom_css()
 
if "text_boxes" not in st.session_state:
    st.session_state.text_boxes = []
 
# Initialise session state variables
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
 
if "show_text_input" not in st.session_state:
    st.session_state.show_text_input = False
 
if "assistant_text" not in st.session_state:
    st.session_state.assistant_text = [""]
 
if "code_input" not in st.session_state:
    st.session_state.code_input = []
 
if "code_output" not in st.session_state:
    st.session_state.code_output = []
 
if "disabled" not in st.session_state:
    st.session_state.disabled = False
 
if "gbq_data" not in st.session_state:
    st.session_state.gbq_data = None
    
if "file_id" not in st.session_state:
    st.session_state.file_id = None

if "files_to_delete" not in st.session_state:
    st.session_state.files_to_delete = []
 
if "last_interaction" not in st.session_state:
    st.session_state.last_interaction = datetime.now()
 
 
clientes_por_equipo = {
    "equipo_verde": ["BONOXS", "LAFISE PN", "LAFISE RD", "LAFISE HN", "ALIGE"],
    "equipo_amarillo": ["PEIGO", "KASH", "DLOCALGO", "BANPAIS"],
    "equipo_violeta": ["ZAPIA", "HANDY", "BOOMIT"]
}
 
# Define a placeholder option
placeholder_option = "Seleccione un equipo"
 
# Update the list of team options to include the placeholder
team_options = list(clientes_por_equipo.keys())
team_options.insert(0, placeholder_option)
 
# Selection of team
equipo_seleccionado = st.selectbox("Seleccione un equipo:", team_options, index=0, key="equipo_seleccionado")
 
# Check if the selected team is the placeholder
if equipo_seleccionado == placeholder_option:
    # Set the selected team to None to indicate no selection
    equipo_seleccionado = None
 
# Define team passwords in a dictionary
team_passwords = {
    "equipo_verde": "verde",
    "equipo_amarillo": "amarillo",
    "equipo_violeta": "violeta"
}
 
# Password input and validation
password_input_container = st.empty()  # Create the container initially
 
if equipo_seleccionado:
    if show_password_input:
        password_input = password_input_container.text_input("Ingrese la contraseña del equipo:", type="password")
        if password_input != "":
            if password_input == team_passwords.get(equipo_seleccionado):
                # st.success("Contraseña correcta!")
                show_client_dropdown = True  # Show client dropdown
                password_input_container.empty()  # Clear the container after successful login
            else:
                st.error("Contraseña incorrecta. Intente nuevamente.")
 
# Display client dropdown only if password is correct
if show_client_dropdown:
    # Password validated, display client dropdown
    clientes = clientes_por_equipo.get(equipo_seleccionado, [])
    if clientes:
        cliente_seleccionado = st.selectbox("Selecciona un cliente:", clientes, key="cliente_seleccionado")
        st.write(f"Bienvenido al equipo {equipo_seleccionado.capitalize()}! Has seleccionado al cliente: {cliente_seleccionado}")
 
        # Get data from the database and store it in the session state
        st.session_state.gbq_data = bbdd.get_data(cliente_seleccionado)
        
        # Eliminar caracteres extraños como comillas dobles, barras invertidas, etc.
        st.session_state.gbq_data['inversion'] = st.session_state.gbq_data['inversion'].replace(r'[\"\\]', '', regex=True)
        st.session_state.gbq_data['inversion'] = pd.to_numeric(st.session_state.gbq_data['inversion'], errors='coerce')

        # Display a sample of the data to verify it has been loaded correctly
        st.write(st.session_state.gbq_data)
 
        # Ahora, en lugar de subir el archivo, almacena el DataFrame en la sesión para usarlo en prompts futuros
        st.write("Los datos del cliente han sido cargados y están listos para usar en las consultas.")

        # Obtener la hora actual
        now = datetime.now()
        # Formatear la fecha y hora actual en el formato deseado
        timestamp = now.strftime("%Y%m%d%H%M%S")
        
        file_name = f"{cliente_seleccionado}_{timestamp}_csvEnJsonl.jsonl"

        if not st.session_state.file_id:
            file_info = upload_file(st.session_state.gbq_data.to_csv(index=False), file_name)
            st.session_state.file_id = file_info["id"]
            st.session_state.files_to_delete.append(st.session_state.file_id)

        # Initialise the OpenAI client, and retrieve the assistant
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        assistant = client.beta.assistants.retrieve(st.secrets["ASSISTANT_ID_2"])
        
#         instrucciones = """ # Agregadas como parte de las instrucciones del asistente
# Deberas analizar datos de rendimiento de inversiones publicitarias que te brindare en el prompt.
# IMPORTANTE, es OBLIGATORIO que sigas estas pautas al contestar:
# 1. Para el conjunto de datos proporcionado, Identifica atentamente la fecha más reciente respecto a hoy (tendría que ser la fecha de ayer. Por ejemplo, si hoy es 16 de julio, la fecha máxima tendría que ser 15 de julio.) y realiza todo el análisis comparando los datos de los últimos 7 días con los datos de los 7 días inmediatamente anteriores. Si no hay datos de la fecha de ayer, realiza todas las comparaciones tomando la última fecha que haya como ayer.
# 2. Menciona explicitamente las fechas específicas de los dos intervalos de 7 días a analizar.
# 3. Responde de manera breve y directa con datos precisos según la información proporcionada.
# 4. La respuesta tiene que ser en español y debes evitar el lenguaje técnico.
# 5. NUNCA describas las columnas del conjunto de datos y NUNCA incluyas ningún contexto inicial ni explicaciones sobre cómo realizarás el análisis.
# 6. Dirígete directamente a los insights y observaciones, acompañados de soporte numérico, variaciones porcentuales, diferencias absolutas para el período analizado y el anterior, etc.
# 7. Presenta los números claramente sin separar dígitos ni símbolos.
# 8. No uses caracteres especiales entre números y porcentajes.
# 9. Toda la información que menciones debe ser extraída de los datos proporcionados en el prompt.
# 10. NUNCA describas las columnas del conjunto de datos y NUNCA incluyas ningún contexto inicial o explicaciones de cómo realizarás el análisis.
# 11. Evita cualquier salida inicial que explique el conjunto de datos o sus columnas, o lo que se hará o se hizo relacionado con el proceso de salida.
# 12. Centrate directamente en responder la pregunta del usuario o cumplir la tarea."""
        
        # Define una lista de prompts predefinidos
        prompts_abreviados = {
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
        }
 
        # Selección de prompt abreviado
        titulo_abreviado = st.selectbox("Seleccione un prompt:", list(prompts_abreviados.keys()))
        text_box = st.empty()
        qn_btn = st.empty()
 
        # Container for buttons
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([6, 1])
        with col1:
            if st.button("Preguntar a Boomit AI"):
                question = prompts_abreviados[titulo_abreviado]  # Utiliza el prompt completo asociado al título abreviado
                text_box.empty()
                qn_btn.empty()
 
                if moderation_endpoint(question):
                    st.warning("Your question has been flagged. Refresh page to try again.")
                    st.stop()
 
                # Create a new thread
                if "thread_id" not in st.session_state:
                    thread = client.beta.threads.create()
                    st.session_state.thread_id = thread.id
 
                # Update the thread to attach the file
                client.beta.threads.update(
                    thread_id=st.session_state.thread_id,
                    tool_resources={"code_interpreter": {"file_ids": [st.session_state.file_id]}}
                )
                
                # # Definir el nombre del archivo
                # nombre_archivo = "datos_gbq.csv"

                # # Guardar el DataFrame completo en un archivo CSV
                # st.session_state.gbq_data.to_csv(nombre_archivo, index=False)

                # print(f"Archivo CSV guardado como: {nombre_archivo}")   
                
                client.beta.threads.messages.create(
                    thread_id=st.session_state.thread_id,
                    role="user",
                    content=[
                        {
                            "type": "text",
                            "text": question  
                        }
                    ]
                )
 
                with client.beta.threads.runs.stream(thread_id=st.session_state.thread_id,
                                                    assistant_id=assistant.id,
                                                    tool_choice={"type": "code_interpreter"},
                                                    event_handler=EventHandler(),
                                                    temperature=0.3) as stream:
                    stream.until_done()
                    st.toast("BOOMIT AI ha terminado su análisis", icon="🕵️")
 
                # Asegúrate de que `text_boxes` no esté vacío antes de intentar acceder a sus elementos
                if st.session_state.text_boxes:
                    st.session_state.assistant_text[0] = st.session_state.text_boxes[-1]
                else:
                    st.error("No hay respuestas disponibles del asistente.")
 
                # Save the assistant's response
                st.session_state.assistant_text[0] = st.session_state.text_boxes[-1]
 
                # Prepare the files for download
                with st.spinner("Preparing the files for download..."):
                    # Retrieve the messages by the Assistant from the thread
                    assistant_messages = retrieve_messages_from_thread(st.session_state.thread_id)
                    # For each assistant message, retrieve the file(s) created by the Assistant
                    st.session_state.assistant_created_file_ids = retrieve_assistant_created_files(assistant_messages)
                    # Download these files
                    st.session_state.download_files, st.session_state.download_file_names = render_download_files(st.session_state.assistant_created_file_ids)
 
                # Clean-up
                # Delete the file(s) created by the Assistant
                delete_files(st.session_state.assistant_created_file_ids)
 
                # Set show_text_input to True to show the text input for another query
                st.session_state.show_text_input = True
 
        with col2:
            if st.button("Log Out", key="logout_button", help="Cerrar sesión y limpiar archivos"):
                if st.session_state.files_to_delete:
                    delete_files(st.session_state.files_to_delete)
                    st.success("Done!")
                    st.session_state.files_to_delete = []
 
        # Close the container div
        st.markdown('</div>', unsafe_allow_html=True)
 
# Mostrar cuadro de texto para realizar otra consulta solo si se generó un output previo
if st.session_state.show_text_input:
    consulta_libre = st.text_area("Realice otra consulta:", "")
    if st.button("Preguntar a Boomit AI (consulta libre)"):
        if consulta_libre.strip() != "":
            question = consulta_libre
            text_box.empty()
            qn_btn.empty()
 
            # Crear un nuevo hilo (thread) si no existe uno
            if "thread_id" not in st.session_state:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id
 
            # Actualizar el hilo para adjuntar el archivo
            # client.beta.threads.update(
            #     thread_id=st.session_state.thread_id,
            #     tool_resources={"code_interpreter": {"file_ids": [st.session_state.file_id]}}
            # )
 
            if "text_boxes" not in st.session_state:
                st.session_state.text_boxes = []
 
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=question
            )
 
            st.session_state.text_boxes.append(st.empty())
            #st.session_state.text_boxes[-1].success(f"**> 🤔 User:** {question}")
 
            with client.beta.threads.runs.stream(thread_id=st.session_state.thread_id,
                                                 assistant_id=assistant.id,
                                                 tool_choice={"type": "code_interpreter"},
                                                 event_handler=EventHandler(),
                                                 temperature=0) as stream:
                stream.until_done()
                st.toast("BOOMIT AI ha terminado su análisis", icon="🕵️")
 
            # Prepare the files for download
            with st.spinner("Preparing the files for download..."):
                # Retrieve the messages by the Assistant from the thread
                assistant_messages = retrieve_messages_from_thread(st.session_state.thread_id)
                # For each assistant message, retrieve the file(s) created by the Assistant
                st.session_state.assistant_created_file_ids = retrieve_assistant_created_files(assistant_messages)
                # Download these files
                st.session_state.download_files, st.session_state.download_file_names = render_download_files(st.session_state.assistant_created_file_ids)
 
# Check for inactivity
inactive_time_limit = timedelta(minutes=10)
if datetime.now() - st.session_state.last_interaction > inactive_time_limit:
    if st.session_state.files_to_delete:
        delete_files(st.session_state.files_to_delete)
        st.success("Sesión inactiva. Archivos eliminados correctamente.")
        st.session_state.files_to_delete = []
 
# Update last interaction time
st.session_state.last_interaction = datetime.now()
 
# Optionally, add a cleanup at the end of the script
def cleanup():
    if st.session_state.files_to_delete:
        delete_files(st.session_state.files_to_delete)
        st.session_state.files_to_delete = []
 
# Register the cleanup function to run when the script exits
import atexit
atexit.register(cleanup)
 
 
 