import csv
import os
from typing import Generator, Dict, List, Any, Optional
from core.config import settings
from uuid import uuid4

class CSVDatabase:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.fieldnames = [
            'id', 'name', 'description', 'endpoint', 'openapi_url', 
            'org_website', 'org_email', 'tags'
        ]

    def ensure_file_exists(self):
        """Create the CSV file if it doesn't exist"""
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def read_all(self) -> List[Dict[str, Any]]:
        """Read all records from the CSV file"""
        self.ensure_file_exists()
        with open(self.csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def write_all(self, records: List[Dict[str, Any]]):
        """Write all records to the CSV file"""
        with open(self.csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(records)

    def add(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new record to the CSV file"""
        if not record.get('id'):
            record['id'] = str(uuid4())
        
        records = self.read_all()
        records.append(record)
        self.write_all(records)
        return record

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Get a record by its ID"""
        records = self.read_all()
        for record in records:
            if record['id'] == id:
                return record
        return None

    def filter(self, **kwargs) -> List[Dict[str, Any]]:
        """Filter records based on criteria"""
        records = self.read_all()
        result = records

        if kwargs:
            result = []
            for record in records:
                match = True
                for key, value in kwargs.items():
                    if key.endswith('__ilike'):
                        field = key.replace('__ilike', '')
                        if value.startswith('%') and value.endswith('%'):
                            search_term = value[1:-1].lower()
                            if search_term not in record[field].lower():
                                match = False
                                break
                    elif key.endswith('__contains'):
                        field = key.replace('__contains', '')
                        if value not in record[field]:
                            match = False
                            break
                    elif record.get(key) != value:
                        match = False
                        break
                
                if match:
                    result.append(record)
                    
        return result

# Create a database instance with the configured CSV path
csv_db = CSVDatabase(settings.csv_path)

# Simple dependency to get the database - no context manager
def get_db():
    """Get database instance - compatible with FastAPI dependency injection"""
    return csv_db

def init_db():
    """Initialize the database"""
    csv_db.ensure_file_exists()

def get_engine():
    """Compatibility function for code expecting SQLAlchemy engine"""
    return None  # No actual engine needed for CSV operations