from google.cloud import bigquery
from src.config.proyectos_names import ProyectosNames
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
                    SUM(virtualcard_activation_success_UU) AS evento_objetivo,
                    SUM(install) AS Instalaciones,
                    CASE 
                        WHEN SUM(virtualcard_activation_success_UU) = 0 OR SUM(install) = 0 THEN 0
                        ELSE SUM(virtualcard_activation_success_UU) / SUM(install) 
                    END AS cvr 
                    FROM (
                    SELECT 
                        fecha,
                        Campaign,
                        (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(Campaign, '_')[OFFSET(3)])) AS plataforma,
                        total_cost,
                        virtualcard_activation_success_UU,
                        install
                    FROM `peigo-boomit.Datos_Dash.Android_IOS_Raw_AF`
                    WHERE Campaign LIKE '%BOOMIT%'
                        AND fecha >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                        AND (SELECT `dimensiones.Data_Cruda.codigo_estrategia`(SPLIT(Campaign, '_')[OFFSET(4)])) 
                            IN UNNEST(['PERFORMANCE', 'PURCHASE', 'TRAFICO', 'ADQUISICION', 'RETENCION', 
                            'RECOMPRADORES', 'RETENCION Y RECOMPRADORES', 'CAPTACION', 'RETARGETING'])
                    ) 
                    GROUP BY fecha, Campaign, plataforma"""
    elif client == ProyectosNames.THEYARD.value:
        query = """ TODO """
    elif client == 'TRDELPAL':
        query = """ TODO """
    elif client == 'LAFISE PN':
        query = """ TODO"""
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
