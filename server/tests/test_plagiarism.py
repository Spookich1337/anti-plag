import pytest
from unittest.mock import patch

def test_plagiarism_page_success(auth_client):
    with patch("server.app.routers.plagiarism.run_query") as mock_query:
        mock_query.side_effect = [
            [{"r": {"id": 1, "title": "T"}}],
            [{"cnt": 10}],
            [{"suspect_id": 2, "suspect_title": "S", "suspect_author": "A", "shared_chunks": 5}]
        ]
        response = auth_client.get("/plagiarism/1")
        assert response.status_code == 200

def test_plagiarism_page_not_found(auth_client):
    with patch("server.app.routers.plagiarism.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/plagiarism/999")
        assert response.status_code == 404

def test_compare_reports_success(auth_client):
    with patch("server.app.routers.plagiarism.run_query") as mock_query:
        mock_query.side_effect = [
            [{"r": {"id": 1, "title": "T1"}}],
            [{"r": {"id": 2, "title": "T2"}}],
            [{"hash": "h1"}],
            [{"id": 10, "text": "T", "hash": "h1", "part_type": "P"}],
            [{"id": 20, "text": "T", "hash": "h1", "part_type": "P"}]
        ]
        response = auth_client.get("/plagiarism/1/compare/2")
        assert response.status_code == 200

def test_compare_reports_not_found(auth_client):
    with patch("server.app.routers.plagiarism.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/plagiarism/1/compare/999")
        assert response.status_code == 404
