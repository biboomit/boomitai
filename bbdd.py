from google.cloud import bigquery
from src.config.proyectos_names import ProyectosNames, SubProyectosNames
from google.oauth2 import service_account
import json
from google.cloud import bigquery
import streamlit as st
from src.config.secrets import keys


def queryBigQuery(query):
    # Carga las credenciales desde secrets.toml
    credentials_dict = json.loads(st.secrets["BIGQUERY_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict
    )

    # Inicializa el cliente de BigQuery con las credenciales cargadas
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df


def query_selector(client):
    query = None
    
    if query is None:
        raise ValueError(f"Client '{client}' is not recognized.")

    return query


def date_query_selector(client):
    query = None
    if client == ProyectosNames.PEIGO.value:
        query = """SELECT 
max(fecha) as period_current_end,
(DATE_ADD(max(fecha), INTERVAL -6 DAY)) as period_current_start,
(DATE_ADD(max(fecha), INTERVAL -13 DAY)) as period_previous_start,
(DATE_ADD(max(fecha), INTERVAL -7 DAY)) as period_previous_end,
FROM (
SELECT 
    fecha,
    nombre_campana,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    bankaccount_created_UU,
    install
FROM `peigo-boomit.Dashboard.tabla_final`
WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)])) 
        IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
        'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
) 
HAVING SUM(costo_total) > 0"""
    elif client == ProyectosNames.THEYARD.value:
        query = """ TODO """
    elif client == ProyectosNames.TRADERPAL.value:
        query = """SELECT 
    max(fecha) as period_current_end,
    (DATE_ADD(max(fecha), INTERVAL -6 DAY)) as period_current_start,
    (DATE_ADD(max(fecha), INTERVAL -13 DAY)) as period_previous_start,
    (DATE_ADD(max(fecha), INTERVAL -7 DAY)) as period_previous_end,
    FROM (
  SELECT
  fecha,
  nombre_campana,
  (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
  costo_total,
  sng_first_funding,
  installs
  FROM `traderpal-boomit.Dashboard.tabla_final`
  WHERE nombre_campana LIKE '%BOOMIT_%'
  AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
  AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)]))
    IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION',
    'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
)
HAVING SUM(costo_total) > 0"""
    elif client == "LAFISE PN":
        query = """ TODO"""
    elif client == ProyectosNames.ALIGE_ALLIANZ_AHORRO.value:
        query = f"""SELECT 
max(fecha) as period_current_end,
(DATE_ADD(max(fecha), INTERVAL -6 DAY)) as period_current_start,
(DATE_ADD(max(fecha), INTERVAL -13 DAY)) as period_previous_start,
(DATE_ADD(max(fecha), INTERVAL -7 DAY)) as period_previous_end,
FROM (
SELECT 
fecha as Fecha,
nombre_campana as Campania,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
FROM (
    SELECT 
    fecha,
    nombre_campana,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    FROM `alige-boomit.Dashboard.tabla_final`
    WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)])) 
        IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
        'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
    AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_AHORRO.value}'
    ) 
    GROUP BY fecha, nombre_campana, plataforma
    HAVING SUM(costo_total) > 0)"""
    elif client == ProyectosNames.ALIGE_ALLIANZ_VIDA.value:
        query = f"""SELECT
max(fecha) as period_current_end,
(DATE_ADD(max(fecha), INTERVAL -6 DAY)) as period_current_start,
(DATE_ADD(max(fecha), INTERVAL -13 DAY)) as period_previous_start,
(DATE_ADD(max(fecha), INTERVAL -7 DAY)) as period_previous_end,
FROM (
SELECT
fecha as Fecha,
nombre_campana as Campania,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
FROM (
    SELECT
    fecha,
    nombre_campana,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    FROM `alige-boomit.Dashboard.tabla_final`
    WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
    AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)]))
        IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION',
        'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
    AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_VIDA.value}'
)
GROUP BY fecha, nombre_campana, plataforma
HAVING SUM(costo_total) > 0)"""
    elif client == ProyectosNames.ALIGE_SKANDIA_AHORRO.value:
        query = f"""SELECT
max(fecha) as period_current_end,
(DATE_ADD(max(fecha), INTERVAL -6 DAY)) as period_current_start,
(DATE_ADD(max(fecha), INTERVAL -13 DAY)) as period_previous_start,
(DATE_ADD(max(fecha), INTERVAL -7 DAY)) as period_previous_end,
FROM (
SELECT
fecha as Fecha,
nombre_campana as Campania,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
FROM (
    SELECT
    fecha,
    nombre_campana,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    FROM `alige-boomit.Dashboard.tabla_final`
    WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
    AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)]))
        IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION',
        'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
    AND flag_producto = '{SubProyectosNames.ALIGE_SKANDIA_AHORRO.value}'
)
GROUP BY fecha, nombre_campana, plataforma
HAVING SUM(costo_total) > 0)"""
    elif client == ProyectosNames.DEMO.value:
        query = """SELECT 
max(fecha) as period_current_end,
(DATE_ADD(max(fecha), INTERVAL -6 DAY)) as period_current_start,
(DATE_ADD(max(fecha), INTERVAL -13 DAY)) as period_previous_start,
(DATE_ADD(max(fecha), INTERVAL -7 DAY)) as period_previous_end,
FROM (
SELECT 
    fecha,
    nombre_campana,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    bankaccount_created_UU,
    install
FROM `peigo-boomit.Dashboard.tabla_final`
WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)])) 
        IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
        'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
) 
HAVING SUM(costo_total) > 0"""
    if query is None:
        raise ValueError(f"Client '{client}' is not recognized.")

    return query


def get_data(client):
    # Parsear las credenciales desde el formato JSON serializado en secrets.toml
    credentials_dict = json.loads(keys[client])
    bq_client = bigquery.Client.from_service_account_info(credentials_dict)
    query = query_selector(client)
    bx_data = bq_client.query(query).to_dataframe()

    return bx_data


def get_data_range(client):
    # Parsear las credenciales desde el formato JSON serializado en secrets.toml
    credentials_dict = json.loads(keys[client])
    bq_client = bigquery.Client.from_service_account_info(credentials_dict)
    query = date_query_selector(client)
    bx_data = bq_client.query(query).to_dataframe()

    return bx_data

def get_data_with_query(query, client):
    # Parsear las credenciales desde el formato JSON serializado en secrets.toml
    credentials_dict = json.loads(keys[client])
    bq_client = bigquery.Client.from_service_account_info(credentials_dict)
    bx_data = bq_client.query(query).to_dataframe()

    return bx_data


def obtenerQuery(promptKey, client):
    if client == ProyectosNames.PEIGO.value:
        return __peigo(promptKey)
    elif client ==  ProyectosNames.THEYARD.value:
        pass
    elif client ==  ProyectosNames.ALIGE_ALLIANZ_AHORRO.value:
        return __alige_allianz_ahorro(promptKey)
    elif client ==  ProyectosNames.ALIGE_ALLIANZ_VIDA.value:
        return __alige_allianz_vida(promptKey)
    elif client ==  ProyectosNames.ALIGE_SKANDIA_AHORRO.value:
        return __alige_skandia_ahorro(promptKey)
    elif client ==  ProyectosNames.DEMO.value:
        return __demo(promptKey)
    elif client ==  ProyectosNames.TRADERPAL.value:
        return __traderpal(promptKey)
    
    raise ValueError(f"Client '{client}' is not recognized.")
    
        
def __peigo(promptKey):
    query = None
    if promptKey == 'Comparativa de rendimiento entre medios':
        query = f"""SELECT 
fecha as Fecha,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
SUM(bankaccount_created_UU) AS evento_objetivo,
SUM(install) AS Instalaciones,
FROM (
SELECT 
    fecha,
    network AS plataforma,
    costo_total,
    bankaccount_created_UU,
    install
FROM `peigo-boomit.Dashboard.tabla_final`
WHERE flag_tipo_reporte = 'Activity' and network in ('TikTok Ads', 'Google Ads', 'Meta')
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
) 
GROUP BY fecha, plataforma
order by fecha, plataforma"""
    elif promptKey == 'Mejor y peor campaña de los últimos 7 días' or promptKey == 'Análisis de Variación de CVR' or promptKey == 'Reporte de Análisis Publicitario':
        query = f"""SELECT 
    fecha AS Fecha,
    nombre_campana AS Campania,
    plataforma AS Plataforma,
    SUM(costo_total) AS inversion,
    SUM(bankaccount_created_UU) AS evento_objetivo,
    SUM(install) AS Instalaciones,
    CASE 
        WHEN SUM(bankaccount_created_UU) = 0 OR SUM(install) = 0 THEN 0
        ELSE SUM(bankaccount_created_UU) / SUM(install) 
    END AS cvr
FROM (
    WITH campanas AS (
        SELECT 
            nombre_campana AS nombres, 
            SUM(costo_total) AS costo, 
            SUM(install) AS instalaciones, 
            SUM(bankaccount_created_UU) AS evento_objetivo
        FROM `peigo-boomit.Dashboard.tabla_final`
        WHERE flag_tipo_reporte = 'Activity' 
            AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
            AND nombre_campana IS NOT NULL
        GROUP BY nombres
        HAVING costo > 0 AND (instalaciones > 0 OR evento_objetivo > 0)
    )
    SELECT 
        fecha,
        nombre_campana,
        network AS plataforma,
        costo_total,
        bankaccount_created_UU,
        install
    FROM `peigo-boomit.Dashboard.tabla_final` f
    INNER JOIN campanas s ON f.nombre_campana = s.nombres
    WHERE flag_tipo_reporte = 'Activity' 
        AND network IN ('TikTok Ads', 'Google Ads', 'Meta')
        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    ORDER BY nombre_campana, fecha
)
GROUP BY fecha, nombre_campana, plataforma
HAVING inversion > 0 OR evento_objetivo > 0 OR Instalaciones > 0;
"""
    
    if query is None:
        raise ValueError(f"Quer key '{promptKey}' is not recognized.")

    return query

def __alige_allianz_ahorro(promptKey):
    query = None
    if promptKey == 'Comparativa de rendimiento entre medios':
        query = f"""SELECT 
fecha as Fecha,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
SUM(lead_total_calificado) AS evento_objetivo,
SUM(usuarios_totales) AS evento_inicial,
CASE 
    WHEN SUM(lead_total_calificado) = 0 OR SUM(usuarios_totales) = 0 THEN 0
    ELSE SUM(lead_total_calificado) / SUM(usuarios_totales) 
END AS cvr 
FROM (
SELECT 
    fecha,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    lead_total_calificado as lead_total_calificado,
    usuarios_totales
FROM `alige-boomit.Dashboard.tabla_final`
WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_AHORRO.value}'
) 
GROUP BY fecha, plataforma"""
    elif promptKey == 'Mejor y peor campaña de los últimos 7 días' or promptKey == 'Análisis de Variación de CVR' or promptKey == 'Reporte de Análisis Publicitario':
        query = f"""SELECT 
    fecha as Fecha,
    nombre_campana as Campania,
    plataforma as Plataforma,
    SUM(costo_total) AS inversion,
    SUM(lead_total_calificado) AS evento_objetivo,
    SUM(usuarios_totales) AS evento_inicial,
    CASE 
        WHEN SUM(lead_total_calificado) = 0 OR SUM(usuarios_totales) = 0 THEN 0
        ELSE SUM(lead_total_calificado) / SUM(usuarios_totales) 
    END AS cvr 
FROM (
    WITH campanas AS (
        SELECT 
            nombre_campana AS nombres, 
            SUM(costo_total) AS costo, 
            SUM(usuarios_totales) AS evento_base, 
            SUM(lead_total_calificado) AS evento_objetivo
        FROM `alige-boomit.Dashboard.tabla_final`
        WHERE flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_AHORRO.value}'
            AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
            AND nombre_campana IS NOT NULL
        GROUP BY nombres
        HAVING costo > 0 AND (evento_base > 0 OR evento_objetivo > 0)
    )
    SELECT 
        fecha,
        nombre_campana,
        network AS plataforma,
        costo_total,
        lead_total_calificado as lead_total_calificado,
        usuarios_totales
    FROM `alige-boomit.Dashboard.tabla_final` f
    INNER JOIN campanas s on f.nombre_campana = s.nombres
    WHERE nombre_campana LIKE '%BOOMIT%'
        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
        AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_AHORRO.value}'
) 
GROUP BY fecha, nombre_campana, plataforma
having inversion > 0 or evento_objetivo > 0 or evento_inicial > 0"""

    if query is None:
        raise ValueError(f"Quer key '{promptKey}' is not recognized.")

    return query

def __alige_allianz_vida(promptKey):
    query = None
    if promptKey == 'Comparativa de rendimiento entre medios':
        query = f"""SELECT 
fecha as Fecha,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
SUM(lead_total_calificado) AS evento_objetivo,
SUM(usuarios_totales) AS evento_inicial,
CASE 
    WHEN SUM(lead_total_calificado) = 0 OR SUM(usuarios_totales) = 0 THEN 0
    ELSE SUM(lead_total_calificado) / SUM(usuarios_totales) 
END AS cvr 
FROM (
SELECT 
    fecha,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    lead_total_calificado as lead_total_calificado,
    usuarios_totales
FROM `alige-boomit.Dashboard.tabla_final`
WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_VIDA.value}'
) 
GROUP BY fecha, plataforma"""
    elif promptKey == 'Mejor y peor campaña de los últimos 7 días' or promptKey == 'Análisis de Variación de CVR' or promptKey == 'Reporte de Análisis Publicitario':
        query = f"""SELECT 
    fecha as Fecha,
    nombre_campana as Campania,
    plataforma as Plataforma,
    SUM(costo_total) AS inversion,
    SUM(lead_total_calificado) AS evento_objetivo,
    SUM(usuarios_totales) AS evento_inicial,
    CASE 
        WHEN SUM(lead_total_calificado) = 0 OR SUM(usuarios_totales) = 0 THEN 0
        ELSE SUM(lead_total_calificado) / SUM(usuarios_totales) 
    END AS cvr 
FROM (
    WITH campanas AS (
        SELECT 
            nombre_campana AS nombres, 
            SUM(costo_total) AS costo, 
            SUM(usuarios_totales) AS evento_base, 
            SUM(lead_total_calificado) AS evento_objetivo
        FROM `alige-boomit.Dashboard.tabla_final`
        WHERE flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_VIDA.value}'
            AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
            AND nombre_campana IS NOT NULL
        GROUP BY nombres
        HAVING costo > 0 AND (evento_base > 0 OR evento_objetivo > 0)
    )
    SELECT 
        fecha,
        nombre_campana,
        network AS plataforma,
        costo_total,
        lead_total_calificado as lead_total_calificado,
        usuarios_totales
    FROM `alige-boomit.Dashboard.tabla_final` f
    INNER JOIN campanas s on f.nombre_campana = s.nombres
    WHERE nombre_campana LIKE '%BOOMIT%'
        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
        AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_VIDA.value}'
) 
GROUP BY fecha, nombre_campana, plataforma
having inversion > 0 or evento_objetivo > 0 or evento_inicial > 0"""

    if query is None:
        raise ValueError(f"Quer key '{promptKey}' is not recognized.")

    return query

def __alige_skandia_ahorro(promptKey):
    query = None
    if promptKey == 'Comparativa de rendimiento entre medios':
        query = f"""SELECT 
fecha as Fecha,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
SUM(lead_total_calificado) AS evento_objetivo,
SUM(usuarios_totales) AS evento_inicial,
CASE 
    WHEN SUM(lead_total_calificado) = 0 OR SUM(usuarios_totales) = 0 THEN 0
    ELSE SUM(lead_total_calificado) / SUM(usuarios_totales) 
END AS cvr 
FROM (
SELECT 
    fecha,
    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
    costo_total,
    lead_total_calificado as lead_total_calificado,
    usuarios_totales
FROM `alige-boomit.Dashboard.tabla_final`
WHERE nombre_campana LIKE '%BOOMIT%'
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
    AND flag_producto = '{SubProyectosNames.ALIGE_SKANDIA_AHORRO.value}'
) 
GROUP BY fecha, plataforma"""
    elif promptKey == 'Mejor y peor campaña de los últimos 7 días' or promptKey == 'Análisis de Variación de CVR' or promptKey == 'Reporte de Análisis Publicitario':
        query = f"""SELECT 
    fecha as Fecha,
    nombre_campana as Campania,
    plataforma as Plataforma,
    SUM(costo_total) AS inversion,
    SUM(lead_total_calificado) AS evento_objetivo,
    SUM(usuarios_totales) AS evento_inicial,
    CASE 
        WHEN SUM(lead_total_calificado) = 0 OR SUM(usuarios_totales) = 0 THEN 0
        ELSE SUM(lead_total_calificado) / SUM(usuarios_totales) 
    END AS cvr 
FROM (
    WITH campanas AS (
        SELECT 
            nombre_campana AS nombres, 
            SUM(costo_total) AS costo, 
            SUM(usuarios_totales) AS evento_base, 
            SUM(lead_total_calificado) AS evento_objetivo
        FROM `alige-boomit.Dashboard.tabla_final`
        WHERE flag_producto = '{SubProyectosNames.ALIGE_SKANDIA_AHORRO.value}'
            AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
            AND nombre_campana IS NOT NULL
        GROUP BY nombres
        HAVING costo > 0 AND (evento_base > 0 OR evento_objetivo > 0)
    )
    SELECT 
        fecha,
        nombre_campana,
        network AS plataforma,
        costo_total,
        lead_total_calificado as lead_total_calificado,
        usuarios_totales
    FROM `alige-boomit.Dashboard.tabla_final` f
    INNER JOIN campanas s on f.nombre_campana = s.nombres
    WHERE nombre_campana LIKE '%BOOMIT%'
        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
        AND flag_producto = '{SubProyectosNames.ALIGE_SKANDIA_AHORRO.value}'
) 
GROUP BY fecha, nombre_campana, plataforma
having inversion > 0 or evento_objetivo > 0 or evento_inicial > 0"""

    if query is None:
        raise ValueError(f"Quer key '{promptKey}' is not recognized.")

    return query

def __demo(promptKey):
    query = None
    if promptKey == 'Comparativa de rendimiento entre medios':
        query = f"""SELECT 
fecha as Fecha,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
SUM(bankaccount_created_UU) AS evento_objetivo,
SUM(install) AS Instalaciones,
FROM (
SELECT 
    fecha,
    network AS plataforma,
    costo_total,
    bankaccount_created_UU,
    install
FROM `peigo-boomit.Dashboard.tabla_final`
WHERE flag_tipo_reporte = 'Activity' and network in ('TikTok Ads', 'Google Ads', 'Meta')
    AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
) 
GROUP BY fecha, plataforma
order by fecha, plataforma"""
    elif promptKey == 'Mejor y peor campaña de los últimos 7 días' or promptKey == 'Análisis de Variación de CVR' or promptKey == 'Reporte de Análisis Publicitario':
        query = f"""SELECT 
fecha as Fecha,
nombre_campana as Campania,
plataforma as Plataforma,
SUM(costo_total) AS inversion,
SUM(bankaccount_created_UU) AS evento_objetivo,
SUM(install) AS Instalaciones,
CASE 
    WHEN SUM(bankaccount_created_UU) = 0 OR SUM(install) = 0 THEN 0
    ELSE SUM(bankaccount_created_UU) / SUM(install) 
END AS cvr 
FROM (
    WITH campanas AS (
        SELECT 
            nombre_campana AS nombres, 
            SUM(costo_total) AS costo, 
            SUM(install) AS instalaciones, 
            SUM(bankaccount_created_UU) AS evento_objetivo
        FROM `peigo-boomit.Dashboard.tabla_final`
        WHERE flag_tipo_reporte = 'Activity' 
            AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
            AND nombre_campana IS NOT NULL
        GROUP BY nombres
        HAVING costo > 0 AND (instalaciones > 0 OR evento_objetivo > 0)
    )
    SELECT 
        fecha,
        REGEXP_REPLACE(
            nombre_campana, 
            r'BOOMIT_PEIG_', 
            'BOOMIT_DEMO_'
        ) AS nombre_campana,
        network AS plataforma,
        costo_total,
        bankaccount_created_UU,
        install
    FROM `peigo-boomit.Dashboard.tabla_final` f
    INNER JOIN campanas s ON f.nombre_campana = s.nombres
    WHERE flag_tipo_reporte = 'Activity' and network in ('TikTok Ads', 'Google Ads', 'Meta')
        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
) 
GROUP BY fecha, nombre_campana, plataforma
having inversion > 0 or evento_objetivo > 0 or Instalaciones > 0"""
    
    if query is None:
        raise ValueError(f"Quer key '{promptKey}' is not recognized.")

    return query

def __traderpal(promptKey):
    if promptKey == 'Comparativa de rendimiento entre medios':
        query = """select
fecha as Fecha,
plataforma as Plataforma,
sum(costo_total) as inversion,
sum(sng_first_funding) as evento_objetivo,
sum(installs) as evento_inicial,
case
  when sum(sng_first_funding) = 0 or sum(installs) = 0 then 0
  else sum(sng_first_funding) / sum(installs)
end as CVR
from (
  SELECT
  fecha,
  network AS plataforma,
  costo_total,
  sng_first_funding,
  installs
  FROM `traderpal-boomit.Dashboard.tabla_final`
  WHERE fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
  and network in ('TikTok Ads', 'Google Ads', 'Meta')
)
GROUP BY fecha, plataforma
HAVING SUM(costo_total) > 0"""
    elif promptKey == 'Mejor y peor campaña de los últimos 7 días' or promptKey == 'Análisis de Variación de CVR' or promptKey == 'Reporte de Análisis Publicitario':
        query = """select
fecha as Fecha,
nombre_campana as Campania,
plataforma as Plataforma,
sum(costo_total) as inversion,
sum(sng_first_funding) as evento_objetivo,
sum(installs) as evento_inicial,
case
  when sum(sng_first_funding) = 0 or sum(installs) = 0 then 0
  else sum(sng_first_funding) / sum(installs)
end as CVR
from (
  SELECT
  fecha,
  nombre_campana,
  network AS plataforma,
  costo_total,
  sng_first_funding,
  installs
  FROM `traderpal-boomit.Dashboard.tabla_final`
  WHERE network in ('TikTok Ads', 'Google Ads', 'Meta')
  AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
)
GROUP BY fecha, nombre_campana, plataforma
having inversion > 0 or evento_objetivo > 0 or evento_inicial > 0"""

    if query is None:
        raise ValueError(f"Quer key '{promptKey}' is not recognized.")

    return query
