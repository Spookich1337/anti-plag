from unittest.mock import patch

def test_statistics_page_success(auth_client):
    with patch("server.app.routers.statistics.run_query") as mock_query:
        mock_query.side_effect = [
            [{"g": 101}, {"g": 102}],
            [{"group": 101, "report_count": 5, "avg_words": 1000, "avg_originality": 80.0, "avg_flesh": 50.0, "has_bibliography": 4, "has_introduction": 5, "has_conclusion": 4, "min_originality": 70.0, "max_originality": 90.0}],
            []
        ]
        response = auth_client.get("/statistics/")
        assert response.status_code == 200

def test_statistics_group_filter(auth_client):
    with patch("server.app.routers.statistics.run_query") as mock_query:
        mock_query.side_effect = [
            [{"g": 101}],
            [{"group": 101, "report_count": 5}],
            [{"student": "I Ivanov", "title": "T", "words": 1000, "originality": 80.0, "flesh": 50.0, "bib": True, "intro": True, "conc": True}]
        ]
        response = auth_client.get("/statistics/", params={"group": "101"})
        assert response.status_code == 200
