from unittest.mock import patch

def test_seed_data_skips_if_exists():
    with patch("server.app.services.seeder.run_query") as mock_query:
        mock_query.return_value = [{"cnt": 10}]
        from server.app.services.seeder import seed_data
        seed_data()
        assert mock_query.call_count == 1

def test_seed_data_runs_if_empty():
    with (
        patch("server.app.services.seeder.run_query") as mock_query,
        patch("server.app.services.seeder.run_write") as mock_write
        ):
        mock_query.side_effect = lambda *args, **kwargs: [{"cnt": 0}] if mock_query.call_count == 0 else []
        from server.app.services.seeder import seed_data
        seed_data()
        assert mock_write.called
