import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO

def test_new_report_page(auth_client):
    with patch("server.app.routers.reports.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/reports/new")
        assert response.status_code == 200

def test_upload_report_no_file(auth_client):
    with patch("server.app.routers.reports.run_query") as mock_query, \
         patch("server.app.routers.reports.run_write") as mock_write:
        mock_query.return_value = [{"max_id": 0}]
        data = {"title": "T", "author": "A", "group": 101, "subject": "S"}
        response = auth_client.post("/reports/upload", data=data, follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"].startswith("/reports/")

def test_upload_report_with_docx(auth_client):
    with patch("server.app.routers.reports.run_query") as mock_query, \
         patch("server.app.routers.reports.run_write") as mock_write, \
         patch("server.app.routers.reports.process_docx") as mock_proc:
        mock_query.return_value = [{"max_id": 0}]
        mock_proc.return_value = {
            "title": "T", "author": "A", "group": 101, "subject": "S",
            "parts": [], "words_count": 100, "flesh_index": 50, "keyword_density": 10,
            "introduction": True, "conclusion": True, "bibliography": True
        }
        file_content = b"fake docx content"
        files = {"file": ("test.docx", BytesIO(file_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"title": "T", "author": "A", "group": 101, "subject": "S"}
        response = auth_client.post("/reports/upload", data=data, files=files, follow_redirects=False)
        assert response.status_code == 302

def test_report_detail_not_found(auth_client):
    with patch("server.app.routers.reports.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/reports/999")
        assert response.status_code == 404

def test_report_detail_success(auth_client):
    with patch("server.app.routers.reports.run_query") as mock_query:
        mock_query.side_effect = [
            [{"r": {"id": 1, "title": "T", "upload_date": 1600000000}, "s": None}],
            [{"suspect_id": 2, "suspect_title": "S", "suspect_author": "A", "shared_chunks": 5}],
            [{"cnt": 10}]
        ]
        response = auth_client.get("/reports/1")
        assert response.status_code == 200

def test_save_comment(auth_client):
    with patch("server.app.routers.reports.run_write") as mock_write:
        response = auth_client.post("/reports/1/comment", data={"comment": "Nice"}, follow_redirects=False)
        assert response.status_code == 302
        assert "saved=1" in response.headers["location"]

def test_edit_report_submit(auth_client):
    with patch("server.app.routers.reports.run_write") as mock_write:
        data = {"title": "New T", "author": "A", "group": 101, "subject": "S", "comment": "C", "student_id": 1}
        response = auth_client.post("/reports/1/edit", data=data, follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/reports/1"

def test_delete_report(auth_client):
    with patch("server.app.routers.reports.run_write") as mock_write:
        response = auth_client.post("/reports/1/delete", follow_redirects=False)
        assert response.status_code == 302
