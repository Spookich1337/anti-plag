import pytest
from unittest.mock import patch

def test_graph_page_success(auth_client):
    with patch("server.app.routers.graph.run_query") as mock_query:
        mock_query.return_value = [{"title": "Test Report"}]
        response = auth_client.get("/graph/1")
        assert response.status_code == 200

def test_graph_page_not_found(auth_client):
    with patch("server.app.routers.graph.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/graph/999")
        assert response.status_code == 404

def test_graph_data_success(auth_client):
    with patch("server.app.routers.graph.run_query") as mock_query:
        mock_query.side_effect = [
            [{"id": 1, "title": "Test Report", "author": "Author"}],
            [{"id": 10, "type": "Введение"}],
            [{"id": 100, "text": "Chunk text", "usage": 1}]
        ]
        response = auth_client.get("/graph/1/data")
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data

def test_graph_data_unauthorized(client):
    response = client.get("/graph/1/data")
    assert response.status_code == 401

def test_graph_data_not_found(auth_client):
    with patch("server.app.routers.graph.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/graph/999/data")
        assert response.status_code == 200
        assert response.json() == {"nodes": [], "edges": []}
