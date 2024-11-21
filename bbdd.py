from google.cloud import bigquery
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
    if client == 'BONOXS':
        query = """SELECT * 
                   FROM `bonoxs-boomit.Dashboard.Vista_General_Unificada_Web-App_v2`
                   WHERE Date >= (DATE_ADD(CURRENT_DATE(), INTERVAL -10 DAY))"""
    elif client == 'LAFISE PN':
        query = """SELECT * 
                   FROM `lafise-panama.Dashboard.vista_test_IA`
                   WHERE date >= (DATE_ADD(CURRENT_DATE(), INTERVAL -60 DAY))"""
    elif client == 'PEIGO':
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
                    ) 
                    GROUP BY fecha, Campaign, plataforma"""
    elif client == 'TRDELPAL':
        query = """ TODO """
    elif client == 'THE YARD':
        query = """SELECT 
                    Date as Fecha,
                    Session_campaign as Campania,
                    plataforma as Plataforma,
                    SUM(cost) AS inversion,
                    SUM(lead_typ) AS evento_objetivo,
                    CASE 
                        WHEN SUM(lead_typ) = 0 OR SUM(Sessions) = 0 THEN 0
                        ELSE SUM(lead_typ) / SUM(Sessions) 
                    END AS cvr 
                    FROM (
                    SELECT 
                    Date,
                    Session_campaign,
                    (SELECT `dimensiones.Data_Cruda.codigo_plataforma`(SPLIT(Session_campaign, '_')[OFFSET(3)])) AS plataforma,
                    lead_typ,
                    CASE 
                        WHEN lead_status = "Tour Scheduled" THEN leads 
                        ELSE 0 
                    END as Tour_Scheduled,
                    cost,
                    Sessions
                    FROM `the-yard-boomit.Dash.vista_final` 
                    WHERE Session_campaign LIKE '%BOOMIT%'
                    AND Date >= (DATE_ADD(CURRENT_DATE(), INTERVAL -15 DAY)) 
                    ) 
                    where lead_typ != 0 
                    GROUP BY fecha, Campania, plataforma
                    order by fecha, Campania, plataforma"""
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
