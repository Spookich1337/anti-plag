from unittest.mock import patch

def test_students_list(auth_client):
    with patch("server.app.routers.students.run_query") as mock_query:
        mock_query.return_value = [
            {"id": 1, "name": "Ivan", "surname": "Ivanov", "group": 101, "report_count": 2, "last_upload": 1600000000, "created_at": 1600000000, "updated_at": 1600000000}
        ]
        response = auth_client.get("/students/")
        assert response.status_code == 200

def test_students_list_filters(auth_client):
    with patch("server.app.routers.students.run_query") as mock_query:
        mock_query.return_value = []
        params = {
            "name": "a", "surname": "b", "group": "101", 
            "min_reports": "1", "max_reports": "5",
            "last_upload_from": "2023-01-01T00:00",
            "last_upload_to": "2023-12-31T23:59",
            "created_from": "2023-01-01T00:00",
            "created_to": "2023-12-31T23:59",
            "updated_from": "2023-01-01T00:00",
            "updated_to": "2023-12-31T23:59"
        }
        response = auth_client.get("/students/", params=params)
        assert response.status_code == 200

def test_create_student(auth_client):
    with patch("server.app.routers.students.run_query") as mock_query, \
         patch("server.app.routers.students.run_write"):
        mock_query.return_value = [{"max_id": 0}]
        response = auth_client.post("/students/new", data={"name": "Petr", "surname": "Petrov", "group": 102}, follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/students/"

def test_student_detail_not_found(auth_client):
    with patch("server.app.routers.students.run_query") as mock_query:
        mock_query.return_value = []
        response = auth_client.get("/students/999")
        assert response.status_code == 404

def test_student_detail_success(auth_client):
    with patch("server.app.routers.students.run_query") as mock_query:
        mock_query.side_effect = [
            [{"s": {"id": 1, "name": "Ivan", "surname": "Ivanov", "group": 101, "created_at": 1600000000, "updated_at": 1600000000}}],
            [{"id": 10, "title": "Rep", "subject": "Math", "originality": 95.0, "status": "Ready", "upload_date": 1600000000}]
        ]
        response = auth_client.get("/students/1")
        assert response.status_code == 200

def test_edit_student_page(auth_client):
    with patch("server.app.routers.students.run_query") as mock_query:
        mock_query.return_value = [{"s": {"id": 1, "name": "Ivan", "surname": "Ivanov", "group": 101}}]
        response = auth_client.get("/students/1/edit")
        assert response.status_code == 200

def test_edit_student_submit(auth_client):
    with patch("server.app.routers.students.run_write"):
        response = auth_client.post("/students/1/edit", data={"name": "Ivan", "surname": "Ivanov", "group": 105}, follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/students/1"

def test_delete_student(auth_client):
    with patch("server.app.routers.students.run_write"):
        response = auth_client.post("/students/1/delete", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/students/"
