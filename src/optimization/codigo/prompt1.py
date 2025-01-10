import pandas as pd
from io import StringIO

# Convert the CSV data to a pandas DataFrame
data = pd.read_csv(StringIO(csv_data))

# Convert 'Fecha' to datetime format
data['Fecha'] = pd.to_datetime(data['Fecha'])

# Find the most recent date in the dataset
most_recent_date = data['Fecha'].max()

# Define the two periods for comparison
period_current_end = most_recent_date
period_current_start = period_current_end - pd.Timedelta(days=6)
period_previous_end = period_current_start - pd.Timedelta(days=1)
period_previous_start = period_previous_end - pd.Timedelta(days=6)

# Filter data for the two periods
df_current = data[(data['Fecha'] >= period_current_start) & (data['Fecha'] <= period_current_end)]
df_previous = data[(data['Fecha'] >= period_previous_start) & (data['Fecha'] <= period_previous_end)]

# Convert 'inversion' column to numeric
data['inversion'] = pd.to_numeric(data['inversion'], errors='coerce')
df_current['inversion'] = pd.to_numeric(df_current['inversion'], errors='coerce')
df_previous['inversion'] = pd.to_numeric(df_previous['inversion'], errors='coerce')

# Function to calculate metrics for a given period and platform
def calculate_metrics(df, platform):
    df_platform = df[df['Plataforma'] == platform]
    total_inversion = df_platform['inversion'].sum()
    total_eventos = df_platform['evento_objetivo'].sum()
    costo_medio = total_inversion / total_eventos if total_eventos != 0 else 0
    return total_inversion, costo_medio

# Get unique platforms
platforms = data['Plataforma'].unique()

# Calculate metrics for each platform in both periods
results = {

}
for platform in platforms:
    inv_prev, cost_prev = calculate_metrics(df_previous, platform)
    inv_curr, cost_curr = calculate_metrics(df_current, platform)
    results[platform] = {
        'inv_prev': inv_prev,
        'cost_prev': cost_prev,
        'inv_curr': inv_curr,
        'cost_curr': cost_curr,
        'cost_change_pct': ((cost_curr - cost_prev) / cost_prev * 100) if cost_prev != 0 else 0,
        'inv_change_pct': ((inv_curr - inv_prev) / inv_prev * 100) if inv_prev != 0 else 0
    }

results