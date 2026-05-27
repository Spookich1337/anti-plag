from unittest.mock import patch
from io import BytesIO

def test_import_page(auth_client):
    response = auth_client.get("/import")
    assert response.status_code == 200

def test_mass_upload_unauthorized(client):
    response = client.post("/import/upload", files={"files": []})
    assert response.status_code == 401

def test_mass_upload_success(auth_client):
    with (
        patch("server.app.routers.import_export.run_query") as mock_query,
        patch("server.app.routers.import_export.run_write"),
        patch("server.app.routers.import_export.process_docx") as mock_proc
        ):
        mock_query.return_value = [{"m": 0}]
        mock_proc.return_value = {
            "title": "T", "author": "A", "group": 3341, "subject": "S",
            "parts": [], "words_count": 100, "flesh_index": 50, "keyword_density": 10,
            "introduction": True, "conclusion": True, "bibliography": True
        }
        files = [("files", ("test.docx", BytesIO(b"content"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))]
        response = auth_client.post("/import/upload", files=files, data={"default_group": 3341, "default_subject": "S"})
        assert response.status_code == 200
        assert response.json()["results"][0]["status"] == "Готов"

def test_mass_upload_wrong_ext(auth_client):
    files = [("files", ("test.txt", BytesIO(b"content"), "text/plain"))]
    response = auth_client.post("/import/upload", files=files)
    assert response.status_code == 200
    assert response.json()["results"][0]["status"] == "Ошибка"
def test_export_all(auth_client):
    with patch("server.app.routers.import_export.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/export")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

def test_import_json_success(auth_client):
    with patch("server.app.routers.import_export.run_write"):
        json_data = {
            "students": [{"id": 1, "name": "N", "surname": "S", "group": 101}],
            "reports": [{"id": 1, "title": "T"}],
            "parts": [], "chunks": [], "relationships": {}
        }
        files = {"file": ("data.json", BytesIO(str(json_data).replace("'", '"').encode()), "application/json")}
        response = auth_client.post("/import/json", files=files)
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_import_json_invalid(auth_client):
    files = {"file": ("data.json", BytesIO(b"invalid json"), "application/json")}
    response = auth_client.post("/import/json", files=files)
    assert response.status_code == 400
