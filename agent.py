from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.sql import SQLTools
from dotenv import load_dotenv
import os

load_dotenv(".env.local")


def get_agent(db_url: str) -> Agent:
    """
    Create and return a fresh agno Agent pointed at db_url.

    db_url: SQLAlchemy connection string, e.g. "sqlite:////abs/path/current.db"
            or postgres://user:pass@host/dbname
    Returns a new Agent instance on every call. Not cached.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env.local")
        
    return Agent(
        model=OpenRouter(id="minimax/minimax-m2.7"),
        tools=[SQLTools(db_url=db_url)],
        markdown=True,
        instructions=[
            "You are a data analyst. Convert business queries into SQL.",
            "Always list tables first, then describe relevant ones before querying.",
            "Format your response in the following structure:",
            "1. **SQL Query**: Display the final SQL query in a markdown code block with ```sql\n...query...\n```",
            "2. **Tool Result**: Show the data returned from the query execution in a clear, formatted table or structured format.",
            "3. **Final Insights**: Provide 2-3 actionable insights derived from the query results with specific data points.",
            "Always include all three sections in every response.",
        ],
    )

