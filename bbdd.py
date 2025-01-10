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
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    # Inicializa el cliente de BigQuery con las credenciales cargadas
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

def query_selector(client):
    query = None
    if client == ProyectosNames.PEIGO.value:
        query = """SELECT 
                    fecha as Fecha,
                    Campaign as Campania,
                    plataforma as Plataforma,
                    SUM(total_cost) AS inversion,
                    SUM(bankaccount_created_UU) AS evento_objetivo,
                    SUM(install) AS Instalaciones,
                    CASE 
                        WHEN SUM(bankaccount_created_UU) = 0 OR SUM(install) = 0 THEN 0
                        ELSE SUM(bankaccount_created_UU) / SUM(install) 
                    END AS cvr 
                    FROM (
                    SELECT 
                        fecha,
                        Campaign,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(Campaign, '_')[OFFSET(3)])) AS plataforma,
                        total_cost,
                        bankaccount_created_UU,
                        install
                    FROM `peigo-boomit.Datos_Dash.Android_IOS_Raw_AF`
                    WHERE Campaign LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(Campaign, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                    ) 
                    GROUP BY fecha, Campaign, plataforma
                    HAVING SUM(total_cost) > 0"""
    elif client == ProyectosNames.THEYARD.value:
        query = """ TODO """
    elif client == 'TRDELPAL':
        query = """ TODO """
    elif client == 'LAFISE PN':
        query = """ TODO"""
    elif client == ProyectosNames.ALIGE_ALLIANZ_AHORRO.value:
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
                    SELECT 
                        fecha,
                        nombre_campana,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
                        costo_total,
                        lead_total_calificado as lead_total_calificado,
                        usuarios_totales
                    FROM `alige-boomit.Dashboard.tabla_final`
                    WHERE nombre_campana LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                        AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_AHORRO.value}'
                    ) 
                    GROUP BY fecha, nombre_campana, plataforma
                    HAVING SUM(costo_total) > 0"""
    elif client == ProyectosNames.ALIGE_ALLIANZ_VIDA.value:
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
                    SELECT 
                        fecha,
                        nombre_campana,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
                        costo_total,
                        lead_total_calificado as lead_total_calificado,
                        usuarios_totales
                    FROM `alige-boomit.Dashboard.tabla_final`
                    WHERE nombre_campana LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                        AND flag_producto = '{SubProyectosNames.ALIGE_ALLIANZ_VIDA.value}'
                    ) 
                    GROUP BY fecha, nombre_campana, plataforma
                    HAVING SUM(costo_total) > 0"""
    elif client == ProyectosNames.ALIGE_SKANDIA_AHORRO.value:
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
                    SELECT 
                        fecha,
                        nombre_campana,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(nombre_campana, '_')[OFFSET(3)])) AS plataforma,
                        costo_total,
                        lead_total_calificado as lead_total_calificado,
                        usuarios_totales
                    FROM `alige-boomit.Dashboard.tabla_final`
                    WHERE nombre_campana LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(nombre_campana, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                        AND flag_producto = '{SubProyectosNames.ALIGE_SKANDIA_AHORRO.value}'
                    ) 
                    GROUP BY fecha, nombre_campana, plataforma
                    HAVING SUM(costo_total) > 0"""
    elif client == ProyectosNames.DEMO.value:
        query = """SELECT 
                    fecha as Fecha,
                    Campaign as Campania,
                    plataforma as Plataforma,
                    SUM(total_cost) AS inversion,
                    SUM(bankaccount_created_UU) AS evento_objetivo,
                    SUM(install) AS Instalaciones,
                    CASE 
                        WHEN SUM(bankaccount_created_UU) = 0 OR SUM(install) = 0 THEN 0
                        ELSE SUM(bankaccount_created_UU) / SUM(install) 
                    END AS cvr 
                    FROM (
                    SELECT 
                        fecha,
                        REGEXP_REPLACE(
                            Campaign, 
                            r'BOOMIT_PEIG_', 
                            'BOOMIT_DEMO_'
                        ) AS Campaign,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(Campaign, '_')[OFFSET(3)])) AS plataforma,
                        total_cost,
                        bankaccount_created_UU,
                        install
                    FROM `peigo-boomit.Datos_Dash.Android_IOS_Raw_AF`
                    WHERE Campaign LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(Campaign, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                    ) 
                    GROUP BY fecha, Campaign, plataforma
                    HAVING SUM(total_cost) > 0"""
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
                    fecha as Fecha,
                    Campaign as Campania,
                    plataforma as Plataforma,
                    SUM(total_cost) AS inversion, 
                    FROM (
                    SELECT 
                        fecha,
                        Campaign,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(Campaign, '_')[OFFSET(3)])) AS plataforma,
                        total_cost,
                        bankaccount_created_UU,
                        install
                    FROM `peigo-boomit.Datos_Dash.Android_IOS_Raw_AF`
                    WHERE Campaign LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(Campaign, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                    ) 
                    GROUP BY fecha, Campaign, plataforma
                    HAVING SUM(total_cost) > 0)"""
    elif client == ProyectosNames.THEYARD.value:
        query = """ TODO """
    elif client == 'TRDELPAL':
        query = """ TODO """
    elif client == 'LAFISE PN':
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
                    fecha as Fecha,
                    Campaign as Campania,
                    plataforma as Plataforma,
                    SUM(total_cost) AS inversion,
                    FROM (
                    SELECT
                        fecha,
                        REGEXP_REPLACE(
                            Campaign,
                            r'BOOMIT_PEIG_',
                            'BOOMIT_DEMO_'
                        ) AS Campaign,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(Campaign, '_')[OFFSET(3)])) AS plataforma,
                        total_cost,
                    FROM `peigo-boomit.Datos_Dash.Android_IOS_Raw_AF`
                    WHERE Campaign LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY))
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(Campaign, '_')[OFFSET(4)]))
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION',
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                    )
                    GROUP BY fecha, Campaign, plataforma
                    HAVING SUM(total_cost) > 0)"""
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
