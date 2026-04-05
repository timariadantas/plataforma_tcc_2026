import pytest
from unittest.mock import MagicMock
from application.services.client_service import ClientService
from domain.entities.client import Client
from datetime import  datetime

def test_create_client_calls_repository(mocker):
    
    mock_repo = mocker.patch("application.services.client_service.ClientRepository")
    
    
    mock_conn = mocker.MagicMock()
    
    service = ClientService()
    
    
    service.db.get_connection = mocker.MagicMock()
    service.db.get_connection.return_value.__enter__.return_value = mock_conn
    service.db.get_connection.return_value.__exit__.return_value = None

    birthdate = datetime(1990, 1, 1)
    client = Client("Carlos", "Dantas", "c@email.com", birthdate)

    service.create_client(client)

    # MOCK de verdade
    assert mock_repo.return_value.save.call_count == 1
    mock_conn.commit.assert_called_once()
    
def test_get_client_success(mocker):
    
    mock_repo = mocker.patch("application.services.client_service.ClientRepository")

    mock_conn = mocker.MagicMock()

    service = ClientService()

    service.db.get_connection = mocker.MagicMock()
    service.db.get_connection.return_value.__enter__.return_value = mock_conn
    service.db.get_connection.return_value.__exit__.return_value = None

    
    fake_client = Client("Carlos", "Dantas", "c@email.com", datetime.now())

    
    mock_repo.return_value.get_by_id.return_value = fake_client

    result = service.get_client("123")

    assert result == fake_client
    mock_repo.return_value.get_by_id.assert_called_once_with("123", mock_conn)
    
# testar rollback

def test_create_client_rollback_on_error(mocker):
    mock_repo = mocker.patch("application.services.client_service.ClientRepository")
    
    mock_conn = mocker.MagicMock()
    
    service = ClientService()
    
    service.db.get_connection = mocker.MagicMock()
    service.db.get_connection.return_value.__enter__.return_value = mock_conn
    service.db.get_connection.return_value.__exit__.return_value = None
    
    #Erro no save
    mock_repo.return_value.save.side_effect = Exception("Erro no Banco")
    client = Client ("Maria", "Dantas", "abc@gmail.com", datetime.now())
    
    with pytest.raises(Exception):
        service.create_client(client)
    mock_conn.rollback.assert_called_once()