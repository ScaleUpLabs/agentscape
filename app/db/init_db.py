from db.database import CSVDatabase
from core.config import settings

def init_db(csv_path: str = None):
    """Initialize the CSV database file"""
    path = csv_path or settings.csv_path
    db = CSVDatabase(path)
    db.ensure_file_exists()