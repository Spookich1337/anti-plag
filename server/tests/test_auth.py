
def test_login_page_unauthenticated(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_login_success(client):
    response = client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/"
    assert "session_id" in response.cookies

def test_login_failure(client):
    response = client.post("/login", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401

def test_login_already_authenticated(auth_client):
    response = auth_client.get("/login", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/"

def test_logout(auth_client):
    response = auth_client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"
    assert "session_id" not in response.cookies

def test_require_auth_redirect(client):
    response = client.get("/students/", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"
