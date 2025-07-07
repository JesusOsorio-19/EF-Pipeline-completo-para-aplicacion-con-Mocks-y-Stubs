import subprocess
import sys
from .analyzer import ExternalAnalyzer
from .api_client import APIClient

def main():
    # Función principal de la aplicación
    analyzer = ExternalAnalyzer()
    api_client  = APIClient()

    try:
        # Analizar datos
        result = analyzer.analyze_data("sample_data.txt")

        # Consultar API externa
        api_data = api_client.get_external_data()

        print("Análisis completado con éxito.")
        print("Datos de la API externa:", api_data)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
        
        