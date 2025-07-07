import pytest
import os
import tempfile
import shutil
from unittest.mock import MagicMock, patch

@pytest.fixture
def user_fixture():
    """Fixture que devuelve información de usuario"""
    return {
        "id": 123,
        "name": "Test User",
        "email": "test@example.com",
        "active": True
        }

@pytest.fixture
def authenticated_client_fixture(user_fixture):
    """Fixture que simula un cliente autenticado"""
    class MockAuthenticatedClient:
        def __init__(self, user_data):
            self.user = user_data
            self.token = "fake_token_123"
            self.authenticated = True

        def get_user(self):
            return self.user
        
        def is_authenticated(self):
            return  self.authenticated
    
    return MockAuthenticatedClient(user_fixture)

@pytest.fixture
def temp_data_file():
    """Fixture para crear un archivo temporal de datos"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("sample data for testing")
        temp_file = f.name

    yield temp_file

    if os.path.exists(temp_file):
        os.unlink(temp_file)