"""
CSV Handler - Deprecated

This module is no longer used. The app now accepts database URLs directly
instead of uploading CSV files.
"""

# Legacy constants kept for reference
from pathlib import Path

DB_PATH = Path(__file__).parent / "current.db"
DB_URL = f"sqlite:///{DB_PATH}"

