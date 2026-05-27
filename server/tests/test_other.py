import pytest
from unittest.mock import patch

def test_dashboard_authenticated(auth_client):
    with patch("server.app.routers.dashboard.run_query") as mock_query:
        mock_query.side_effect = [[{"cnt": 10}], [{"cnt": 5}], [{"cnt": 20}]]
        response = auth_client.get("/dashboard")
        assert response.status_code == 200

def test_search_page(auth_client):
    response = auth_client.get("/search")
    assert response.status_code == 200

def test_search_submit(auth_client):
    with patch("server.app.routers.search.run_query") as mock_query:
        mock_query.return_value = [{"id": 1, "title": "T", "author": "A", "group": 101, "subject": "S", "originality": 90.0, "upload_date": 1600000000}]
        params = {"title": "T", "author": "A", "group": "101", "subject": "S", "word": "X", "min_flesh": "10", "min_originality": "50"}
        response = auth_client.get("/search", params=params)
        assert response.status_code == 200
