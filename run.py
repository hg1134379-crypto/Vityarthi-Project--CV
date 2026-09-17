import sys
from pathlib import Path

# Add "campus complaint system" package to sys.path
PROJECT_DIR = Path(__file__).resolve().parent / "campus complaint system"
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from app import app

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
