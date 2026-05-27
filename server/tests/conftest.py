import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from server.app.main import app

@pytest.fixture
def client():
    import os
    os.environ["SKIP_DB_INIT"] = "true"
    with patch("server.app.database.get_driver"), \
         patch("server.app.database.run_query"), \
         patch("server.app.database.run_write"), \
         patch("server.app.database.wait_for_neo4j"), \
         patch("server.app.database.init_db"), \
         patch("server.app.services.seeder.seed_data"), \
         patch("fastapi.templating.Jinja2Templates.TemplateResponse") as mock_template:
        mock_template.side_effect = lambda name, context, **kwargs: MagicMock(template_name=name, context=context)
        with TestClient(app) as c:
            yield c

@pytest.fixture
def auth_client(client):
    client.post("/login", data={"username": "admin", "password": "admin123"})
    return client
