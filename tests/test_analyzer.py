import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock
import tempfile
import stat

from app.analyzer import ExternalAnalyzer

class TestExternalAnalyzer:

    @pytest.fixture(autouse=True)
    def setup_fake_binary(self):
        """Setup que crea el stub del binario para las pruebas"""
        # Crea directorio temporal para el stub
        self.temp_dir = tempfile.mkdtemp()
        self.fake_binary_path = os.path.join(self.temp_dir, "fake-analyzer")

        # Copiar el stub y darle permisos de ejecución
        stub_source = os.path.join(os.path.dirname(__file__), "stubs", "fake-anaylzer.sh")
        if os.path.exists(stub_source):
            import shutil
            shutil.copy2(stub_source, self.fake_binary_path)

        else:
            # Crear el stub si no existe
            with open(self.fake_binary_path, 'w') as f:
                f.write("""#!/bin/bash
                case "$1" in
                    *"error"*)
                        echo "Error de análisis" >&2
                        exit 1
                        ;;
                    *"system_error"*)
                        echo "Error del sistema" >&2
                        exit 2
                        ;;
                    *"valid"*)
                        echo "Análisis exitoso"
                        exit 0
                        ;;
                    *)
                        echo "Análisis completado" >&2    
                        exit 0  
                        ;;
                esac
                """)

        # Dar permisos de ejecución al stub
        os.chmod(self.fake_binary_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        yield
        
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_successful_analysis(self, temp_data_file):
        """Prueba análisis exitoso con datos válidos"""
        analyzer = ExternalAnalyzer(binary_path=self.fake_binary_path)
        
        # Renombrar archivo temporal para que contenga "valid"
        valid_file = temp_data_file.replace('.txt', '_valid.txt')
        os.rename(temp_data_file, valid_file)
        
        result = analyzer.analyze_data(valid_file)
        
        assert "95% precisión" in result
        assert "exitosamente" in result
        
        # Limpieza
        os.unlink(valid_file)

    def test_analysis_error_exit_code_1(self, temp_data_file):
        """Prueba manejo de error con código de salida 1"""
        analyzer = ExternalAnalyzer(binary_path=self.fake_binary_path)
        
        # Renombrar archivo para que contenga "error"
        error_file = temp_data_file.replace('.txt', '_error.txt')
        os.rename(temp_data_file, error_file)
        
        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze_data(error_file)
        
        assert "Error de análisis" in str(exc_info.value)
        
        os.unlink(error_file)

    def test_system_error_exit_code_2(self, temp_data_file):
        """Prueba manejo de error del sistema con código de salida 2"""
        analyzer = ExternalAnalyzer(binary_path=self.fake_binary_path)
        
        # Renombrar archivo para que contenga "system_error"
        system_error_file = temp_data_file.replace('.txt', '_system_error.txt')
        os.rename(temp_data_file, system_error_file)
        
        with pytest.raises(RuntimeError) as exc_info:
            analyzer.analyze_data(system_error_file)
        
        assert "Error del sistema" in str(exc_info.value)
        
        os.unlink(system_error_file)

    def test_default_analysis(self, temp_data_file):
        """Prueba análisis con datos normales (caso por defecto)"""
        analyzer = ExternalAnalyzer(binary_path=self.fake_binary_path)
        
        result = analyzer.analyze_data(temp_data_file)
        
        assert "80% precisión" in result
        assert "Análisis completado" in result

    @patch('app.analyzer.subprocess.run')
    def test_binary_not_found(self, mock_run, temp_data_file):
        """Prueba comportamiento cuando el binario no existe"""
        mock_run.side_effect = FileNotFoundError("Binary not found")
        
        analyzer = ExternalAnalyzer(binary_path="/non/existent/binary")
        
        with pytest.raises(FileNotFoundError):
            analyzer.analyze_data(temp_data_file)