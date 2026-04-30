import sys
from unittest.mock import MagicMock, patch


def _reload_agent():
    """Force a fresh import of agent module to avoid patch-cache issues."""
    if "agent" in sys.modules:
        del sys.modules["agent"]
    import agent
    return agent


def test_get_agent_returns_agent_instance():
    """get_agent should construct and return an agno Agent."""
    with patch.dict("sys.modules", {
        "agno": MagicMock(),
        "agno.agent": MagicMock(),
        "agno.models": MagicMock(),
        "agno.models.openrouter": MagicMock(),
        "agno.tools": MagicMock(),
        "agno.tools.sql": MagicMock(),
    }):
        agent_mod = _reload_agent()
        mock_agent_instance = MagicMock()
        agent_mod.Agent = MagicMock(return_value=mock_agent_instance)
        agent_mod.OpenRouter = MagicMock()
        agent_mod.SQLTools = MagicMock()

        result = agent_mod.get_agent("sqlite:///test.db")
        assert result is mock_agent_instance
        agent_mod.Agent.assert_called_once()


def test_get_agent_passes_db_url_to_sql_tools():
    """get_agent should pass db_url exactly as given to SQLTools."""
    with patch.dict("sys.modules", {
        "agno": MagicMock(),
        "agno.agent": MagicMock(),
        "agno.models": MagicMock(),
        "agno.models.openrouter": MagicMock(),
        "agno.tools": MagicMock(),
        "agno.tools.sql": MagicMock(),
    }):
        agent_mod = _reload_agent()
        agent_mod.Agent = MagicMock()
        agent_mod.OpenRouter = MagicMock()
        mock_sql_tools = MagicMock()
        agent_mod.SQLTools = MagicMock(return_value=mock_sql_tools)

        agent_mod.get_agent("sqlite:///mydb.db")
        agent_mod.SQLTools.assert_called_once_with(db_url="sqlite:///mydb.db")


def test_get_agent_returns_fresh_instance_each_call():
    """get_agent must not cache — two calls must return different objects."""
    with patch.dict("sys.modules", {
        "agno": MagicMock(),
        "agno.agent": MagicMock(),
        "agno.models": MagicMock(),
        "agno.models.openrouter": MagicMock(),
        "agno.tools": MagicMock(),
        "agno.tools.sql": MagicMock(),
    }):
        agent_mod = _reload_agent()
        agent_mod.OpenRouter = MagicMock()
        agent_mod.SQLTools = MagicMock()
        agent_mod.Agent = MagicMock(side_effect=[MagicMock(), MagicMock()])

        a1 = agent_mod.get_agent("sqlite:///db1.db")
        a2 = agent_mod.get_agent("sqlite:///db2.db")
        assert a1 is not a2
