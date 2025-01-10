import pandas as pd
from pathlib import Path
import json
from pprint import pprint

PROJECT_ROOT = Path(__file__).parent.parent

# Define paths
prompt1_path = PROJECT_ROOT / 'optimization' / 'codigo' / 'prompt1.py'
datos_path = PROJECT_ROOT / 'optimization' / 'file' / 'bquxjob_157d5c5d_1941367a86e.csv'

# Read the CSV data
csv_data = pd.read_csv(datos_path)

# Read the analysis code
with open(prompt1_path, 'r') as file:
    analysis_code = file.read()

# Create a namespace for execution
namespace = {
    'csv_data': csv_data.to_csv(index=False),
    'pd': pd
}

# Execute the analysis code in the namespace
exec(analysis_code, namespace)
results = namespace.get('results')

# Mostrar los períodos de análisis
print("\n=== Períodos de Análisis ===")
print(f"Período anterior: {results['fecha_inicio']}")
print(f"Período actual: {results['fecha_fin']}")

# Mostrar resultados por plataforma
print("\n=== Resultados por Plataforma ===")
for platform, metrics in results.items():
    if platform not in ['fecha_inicio', 'fecha_fin']:
        print(f"\nPlataforma: {platform}")
        print(f"Inversión:")
        print(f"  Anterior: ${metrics['inv_prev']:.2f}")
        print(f"  Actual: ${metrics['inv_curr']:.2f}")
        print(f"  Variación: {metrics['inv_change_pct']:.2f}%")
        
        print(f"\nCosto Medio:")
        print(f"  Anterior: ${metrics['cost_prev']:.2f}")
        print(f"  Actual: ${metrics['cost_curr']:.2f}")
        print(f"  Variación: {metrics['cost_change_pct']:.2f}%")