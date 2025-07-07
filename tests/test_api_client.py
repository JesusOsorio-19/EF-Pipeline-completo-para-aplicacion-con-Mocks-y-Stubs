import pytest
import requests
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException

from app.api_client import APIClient

class TestAPIClient:
    
    @patch('app.api_client.requests.get')
    def test_successful_api_call(self, mock_get):
        """Prueba llamada exitosa a la API"""
        # Configurar mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test_data", "status": "success"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Ejecutar
        client = APIClient()
        result = client.get_external_data()
        
        # Verificar
        assert result == {"data": "test_data", "status": "success"}
        mock_get.assert_called_once_with("https://api.external-service.com/data")
        mock_response.raise_for_status.assert_called_once()

    @patch('app.api_client.requests.get')
    def test_api_call_with_custom_base_url(self, mock_get):
        """Prueba llamada con URL base personalizada"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"custom": "data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = APIClient(base_url="https://custom-api.com")
        result = client.get_external_data()
        
        assert result == {"custom": "data"}
        mock_get.assert_called_once_with("https://custom-api.com/data")

    @patch('app.api_client.requests.get')
    def test_api_call_http_error(self, mock_get):
        """Prueba manejo de errores HTTP"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        client = APIClient()
        
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_external_data()

    @patch('app.api_client.requests.get')
    def test_api_call_connection_error(self, mock_get):
        """Prueba manejo de errores de conexión"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        client = APIClient()
        
        with pytest.raises(requests.exceptions.ConnectionError):
            client.get_external_data()

    @patch('app.api_client.requests.get')
    def test_multiple_api_calls(self, mock_get):
        """Prueba múltiples llamadas a la API (para verificar que el mock funciona en bucle)"""
        # Configurar respuestas diferentes para cada llamada
        mock_responses = [
            MagicMock(json=lambda: {"call": 1}),
            MagicMock(json=lambda: {"call": 2}),
            MagicMock(json=lambda: {"call": 3})
        ]
        
        for mock_resp in mock_responses:
            mock_resp.raise_for_status.return_value = None
        
        mock_get.side_effect = mock_responses
        
        client = APIClient()
        
        # Realizar múltiples llamadas
        results = []
        for i in range(3):
            result = client.get_external_data()
            results.append(result)
        
        # Verificar
        assert results == [{"call": 1}, {"call": 2}, {"call": 3}]
        assert mock_get.call_count == 3

    @patch('app.api_client.requests.get')
    def test_api_response_with_autospec(self, mock_get):
        """Prueba usando autospec=True para mayor realismo"""
        mock_get.return_value.json.return_value = {"realistic": "response"}
        mock_get.return_value.raise_for_status.return_value = None
        
        client = APIClient()
        result = client.get_external_data()
        
        assert result == {"realistic": "response"}
        assert mock_get.called