import pandas as pd
from io import StringIO

# Convert the CSV data to a pandas DataFrame
data = pd.read_csv(StringIO(csv_data))

# Convert the 'Fecha' column to datetime format for easier manipulation
data['Fecha'] = pd.to_datetime(data['Fecha'])

# Find the campaign with the best average CVR
best_campaign = data.groupby('Campania')['cvr'].mean().idxmax()

# Filter data for the best campaign
best_campaign_data = data[data['Campania'] == best_campaign]

# Calculate the overall metrics for the best campaign
cvr_promedio = best_campaign_data['cvr'].mean()
mejor_dia = best_campaign_data.loc[best_campaign_data['cvr'].idxmax()]
peor_dia = best_campaign_data.loc[best_campaign_data['cvr'].idxmin()]

inversion_total = best_campaign_data['inversion'].sum()
inversion_promedio_diaria = best_campaign_data['inversion'].mean()
total_eventos = best_campaign_data['evento_objetivo'].sum()
promedio_diario_eventos = best_campaign_data['evento_objetivo'].mean()
costo_por_evento_promedio = inversion_total / total_eventos

# Calculate correlations
corr_inversion_cvr = best_campaign_data['inversion'].corr(best_campaign_data['cvr'])
corr_volumen_cvr = best_campaign_data['evento_objetivo'].corr(best_campaign_data['cvr'])

# Determine thresholds
inversion_threshold = best_campaign_data['inversion'].median()
eventos_threshold = best_campaign_data['evento_objetivo'].median()

# Calculate CVR averages above and below thresholds
cvr_above_inversion_threshold = best_campaign_data[best_campaign_data['inversion'] > inversion_threshold]['cvr'].mean()
cvr_below_inversion_threshold = best_campaign_data[best_campaign_data['inversion'] <= inversion_threshold]['cvr'].mean()

cvr_above_eventos_threshold = best_campaign_data[best_campaign_data['evento_objetivo'] > eventos_threshold]['cvr'].mean()
cvr_below_eventos_threshold = best_campaign_data[best_campaign_data['evento_objetivo'] <= eventos_threshold]['cvr'].mean()

# Determine the analysis period
fecha_inicio = best_campaign_data['Fecha'].min().strftime('%d de %B de %Y')
fecha_fin = best_campaign_data['Fecha'].max().strftime('%d de %B de %Y')

results = {
    'best_campaign': best_campaign,
    'cvr_promedio': cvr_promedio,
    'mejor_dia': mejor_dia['Fecha'].strftime('%d de %B'),
    'cvr_mejor_dia': mejor_dia['cvr'],
    'peor_dia': peor_dia['Fecha'].strftime('%d de %B'),
    'cvr_peor_dia': peor_dia['cvr'],

    'inversion_total': inversion_total,
    'inversion_promedio_diaria': inversion_promedio_diaria,
    'total_eventos': total_eventos,
    'promedio_diario_eventos': promedio_diario_eventos,
    'costo_por_evento_promedio': costo_por_evento_promedio,

    'corr_inversion_cvr': corr_inversion_cvr,
    'corr_volumen_cvr': corr_volumen_cvr,

    'investment_threshold': inversion_threshold,
    'events_threshold': eventos_threshold,

    'cvr_above_inversion_threshold': cvr_above_inversion_threshold,
    'cvr_below_inversion_threshold': cvr_below_inversion_threshold,
    'cvr_above_eventos_threshold': cvr_above_eventos_threshold,
    'cvr_below_eventos_threshold': cvr_below_eventos_threshold,

    'fecha_inicio': fecha_inicio,
    'fecha_fin': fecha_fin,
}