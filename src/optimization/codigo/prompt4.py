import pandas as pd
from io import StringIO

# Convert the CSV data to a pandas DataFrame
data = pd.read_csv(StringIO(csv_data))

# Convert 'Fecha' to datetime format for easier manipulation
data['Fecha'] = pd.to_datetime(data['Fecha'])

# Find the most recent date in the dataset
most_recent_date = data['Fecha'].max()

# Determine the two periods for comparison
period_end = most_recent_date
period_start = period_end - pd.Timedelta(days=6)
previous_period_end = period_start - pd.Timedelta(days=1)
previous_period_start = previous_period_end - pd.Timedelta(days=6)

# Filter the data for the two periods
current_period_data = data[(data['Fecha'] >= period_start) & (data['Fecha'] <= period_end)]
previous_period_data = data[(data['Fecha'] >= previous_period_start) & (data['Fecha'] <= previous_period_end)]

# Remove platforms with zero or near-zero investment
current_period_data = current_period_data[current_period_data['inversion'] > 0.1]
previous_period_data = previous_period_data[previous_period_data['inversion'] > 0.1]

# Display the date ranges for the periods
period_start, period_end, previous_period_start, previous_period_end

# Group by platform and calculate the required metrics for each period
def calculate_metrics(data):
    metrics = data.groupby('Plataforma').agg({
        'evento_objetivo': 'sum',
        'inversion': 'sum',
        'Instalaciones': 'sum'
    }).reset_index()
    metrics['costo_medio_evento'] = metrics['inversion'] / metrics['evento_objetivo']
    metrics['costo_medio_instalacion'] = metrics['inversion'] / metrics['Instalaciones']
    metrics['cvr_medio'] = metrics['evento_objetivo'] / metrics['Instalaciones']
    return metrics

current_metrics = calculate_metrics(current_period_data)
previous_metrics = calculate_metrics(previous_period_data)

# Calculate percentage changes between the two periods
comparison = current_metrics.set_index('Plataforma').join(previous_metrics.set_index('Plataforma'), lsuffix='_current', rsuffix='_previous')
comparison['var_costo_medio_evento'] = (comparison['costo_medio_evento_current'] - comparison['costo_medio_evento_previous']) / comparison['costo_medio_evento_previous'] * 100
comparison['var_eventos'] = (comparison['evento_objetivo_current'] - comparison['evento_objetivo_previous']) / comparison['evento_objetivo_previous'] * 100
comparison['var_costo_medio_instalacion'] = (comparison['costo_medio_instalacion_current'] - comparison['costo_medio_instalacion_previous']) / comparison['costo_medio_instalacion_previous'] * 100
comparison['var_instalaciones'] = (comparison['Instalaciones_current'] - comparison['Instalaciones_previous']) / comparison['Instalaciones_previous'] * 100
comparison['var_inversion'] = (comparison['inversion_current'] - comparison['inversion_previous']) / comparison['inversion_previous'] * 100

# Display the comparison results
comparison[['var_costo_medio_evento', 'var_eventos', 'var_costo_medio_instalacion', 'var_instalaciones', 'var_inversion']]