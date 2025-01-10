import pandas as pd
from io import StringIO

# Convert the CSV data to a pandas DataFrame
data = pd.read_csv(StringIO(csv_data))

# Convert the 'Fecha' column to datetime format
data['Fecha'] = pd.to_datetime(data['Fecha'])

# Identify the most recent date in the dataset
most_recent_date = data['Fecha'].max()

# Define the two periods for analysis
current_period_end = most_recent_date
current_period_start = current_period_end - pd.Timedelta(days=6)
previous_period_end = current_period_start - pd.Timedelta(days=1)
previous_period_start = previous_period_end - pd.Timedelta(days=6)

# Filter data for the two periods
current_period_data = data[(data['Fecha'] >= current_period_start) & (data['Fecha'] <= current_period_end)]
previous_period_data = data[(data['Fecha'] >= previous_period_start) & (data['Fecha'] <= previous_period_end)]

# Display the date ranges for the periods
(current_period_start, current_period_end), (previous_period_start, previous_period_end)

# Exclude campaigns based on the given criteria
# 1. Campaigns with zero investment
# 2. Campaigns with zero events_objetivo
# 3. Campaigns with less than 3 days of data in either period

# Function to filter campaigns based on the criteria
def filter_campaigns(data, period_start, period_end):
    # Group by campaign and platform
    grouped = data.groupby(['Campania', 'Plataforma'])

    # Calculate the number of days, total investment, and total events_objetivo for each campaign
    summary = grouped.agg(
        days_active=('Fecha', 'nunique'),
        total_investment=('inversion', 'sum'),
        total_events=('evento_objetivo', 'sum')
    ).reset_index()

    # Apply the exclusion criteria
    filtered = summary[
        (summary['total_investment'] > 0) &
        (summary['total_events'] > 0) &
        (summary['days_active'] >= 3)
    ]

    return filtered

# Filter campaigns for both periods
filtered_current_period = filter_campaigns(current_period_data, current_period_start, current_period_end)
filtered_previous_period = filter_campaigns(previous_period_data, previous_period_start, previous_period_end)

# Merge the filtered data from both periods to find campaigns with data in both periods
merged_filtered = pd.merge(
    filtered_current_period,
    filtered_previous_period,
    on=['Campania', 'Plataforma'],
    suffixes=('_current', '_previous')
)

# Calculate cost per objective and percentage variation for each campaign
merged_filtered['costo_por_objetivo_current'] = merged_filtered['total_investment_current'] / merged_filtered['total_events_current']
merged_filtered['costo_por_objetivo_previous'] = merged_filtered['total_investment_previous'] / merged_filtered['total_events_previous']
merged_filtered['variacion_porcentual'] = ((merged_filtered['costo_por_objetivo_current'] - merged_filtered['costo_por_objetivo_previous']) / merged_filtered['costo_por_objetivo_previous']) * 100

# Round the percentage variation to two decimal places
merged_filtered['variacion_porcentual'] = merged_filtered['variacion_porcentual'].round(2)

# Determine the best and worst campaigns based on cost per objective in the current period
best_campaign = merged_filtered.loc[merged_filtered['costo_por_objetivo_current'].idxmin()]
worst_campaign = merged_filtered.loc[merged_filtered['costo_por_objetivo_current'].idxmax()]

# Count initial and excluded campaigns
total_initial_campaigns = data['Campania'].nunique()
excluded_campaigns = total_initial_campaigns - merged_filtered['Campania'].nunique()

# Count exclusions by criteria
excluded_no_investment = total_initial_campaigns - data[data['inversion'] > 0]['Campania'].nunique()
excluded_no_events = total_initial_campaigns - data[data['evento_objetivo'] > 0]['Campania'].nunique()
excluded_incomplete_data = total_initial_campaigns - data[data['Fecha'].between(previous_period_start, current_period_end)]['Campania'].nunique()

# Prepare the summary of exclusions
exclusion_summary = {
    "total_initial_campaigns": total_initial_campaigns,
    "excluded_campaigns": excluded_campaigns,
    "excluded_no_investment": excluded_no_investment,
    "excluded_no_events": excluded_no_events,
    "excluded_incomplete_data": excluded_incomplete_data,
    "remaining_campaigns": merged_filtered['Campania'].nunique()
}

previous_period_start.strftime('%Y-%m-%d') + ' to ' + previous_period_end.strftime('%Y-%m-%d'), current_period_start.strftime('%Y-%m-%d') + ' to ' + current_period_end.strftime('%Y-%m-%d'), best_campaign, worst_campaign, exclusion_summary