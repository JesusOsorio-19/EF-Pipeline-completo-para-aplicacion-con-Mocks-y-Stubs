import requests

class APIClient:
    def __init__(self, base_url = "https://api-external-service.com"):
        self.base_url = base_url

    def get_external_data(self):
        # Consulta API REST externa
        response = requests.get(f"{self.base_url}/data")
        response.raise_for_status()
        return