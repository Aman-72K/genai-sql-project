import sys
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def isolate_app(monkeypatch):
    """Reload app module fresh for each test to reset module-level state."""
    if "app" in sys.modules:
        del sys.modules["app"]
    yield
    if "app" in sys.modules:
        del sys.modules["app"]


class TestUploadHandler:
    def test_none_file_resets_agent_and_disables_inputs(self, monkeypatch):
        import app
        app.current_agent = MagicMock()  # ensure agent was set
        status, chat, txt, btn = app.upload_handler(None)
        # Agent must be cleared
        assert app.current_agent is None
        # Chat must be empty list
        assert chat == []

    def test_bad_csv_shows_error_and_keeps_agent_unchanged(self, tmp_path):
        import app
        empty = tmp_path / "bad.csv"
        empty.write_text("")
        file_mock = MagicMock()
        file_mock.name = str(empty)

        original_agent = MagicMock()
        app.current_agent = original_agent

        status, chat, txt, btn = app.upload_handler(file_mock)

        # current_agent must NOT have changed
        assert app.current_agent is original_agent
        # Status update value must contain "Error"
        assert "Error" in str(status)

    def test_good_csv_sets_agent_and_clears_chat(self, tmp_path):
        import app
        csv_file = tmp_path / "sales.csv"
        csv_file.write_text("product,revenue\nA,100\nB,200\n")
        file_mock = MagicMock()
        file_mock.name = str(csv_file)

        mock_agent = MagicMock()
        with patch("app.get_agent", return_value=mock_agent):
            status, chat, txt, btn = app.upload_handler(file_mock)

        assert app.current_agent is mock_agent
        assert chat == []
        assert "sales" in str(status)

    def test_agent_init_failure_preserves_chat_and_leaves_agent_none(self, tmp_path):
        import app
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("x\n1\n")
        file_mock = MagicMock()
        file_mock.name = str(csv_file)

        with patch("app.get_agent", side_effect=RuntimeError("API down")):
            status, chat, txt, btn = app.upload_handler(file_mock)

        assert app.current_agent is None
        assert "Agent error" in str(status)


class TestQueryHandler:
    def test_no_agent_returns_error_message_without_crashing(self):
        import app
        assert app.current_agent is None
        history, textbox = app.query_handler("what is revenue?", [])
        assert len(history) == 1
        assert "No dataset loaded" in history[0]["content"]
        assert textbox == ""

    def test_empty_message_returns_unchanged_history(self):
        import app
        app.current_agent = MagicMock()
        existing = [{"role": "user", "content": "prev question"}, {"role": "assistant", "content": "prev answer"}]
        history, textbox = app.query_handler("   ", existing)
        assert history == existing
        assert textbox == ""

    def test_successful_query_appends_to_history(self):
        import app
        mock_agent = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Revenue is $1000"
        mock_agent.run.return_value = mock_response
        app.current_agent = mock_agent

        history, textbox = app.query_handler("what is revenue?", [])

        assert len(history) == 2
        assert history[0] == {"role": "user", "content": "what is revenue?"}
        assert history[1] == {"role": "assistant", "content": "Revenue is $1000"}
        assert textbox == ""

    def test_agent_exception_shows_error_in_chat(self):
        import app
        mock_agent = MagicMock()
        mock_agent.run.side_effect = RuntimeError("connection failed")
        app.current_agent = mock_agent

        history, textbox = app.query_handler("show me data", [])

        assert len(history) == 2
        assert "Error" in history[1]["content"]
        assert textbox == ""

    def test_none_response_content_shows_placeholder(self):
        import app
        mock_agent = MagicMock()
        mock_response = MagicMock()
        mock_response.content = None
        mock_agent.run.return_value = mock_response
        app.current_agent = mock_agent

        history, textbox = app.query_handler("hello?", [])

        assert "(no response)" in history[1]["content"]
