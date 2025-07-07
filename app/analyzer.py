import subprocess
import os

class ExternalAnalyzer:
    def __init__(self, binary_path="/usr/bin/external-analyzer"):
        self.binary_path = binary_path

    def analyze_data(self, data_file):
        # Invoca el binario externo para analizar los datos
        try:
            result = subprocess.run([self.binary_path, data_file], check=True, capture_output=True, text=True)
            return result.stdout
        
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                raise ValueError("Error en el análisis de datos: " + e.stderr)
            else:
                raise RuntimeError("Error desconocido al invocar el analizador externo: " + e.stderr)
            