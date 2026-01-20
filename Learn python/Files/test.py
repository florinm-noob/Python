import unittest
import os
import csv
import io
import sys
from unittest.mock import patch
from collections import defaultdict
from main1 import citeste_csv, proceseaza_people

class TestMain1(unittest.TestCase):

    def test_citeste_csv_valid(self):
        # Create a sample CSV content
        csv_content = """name,city,age
John,Doe,25
Jane,Smith,30
"""
        # Use StringIO to simulate file
        from io import StringIO
        file_like = StringIO(csv_content)
        # Since citeste_csv opens the file, we need to mock or create temp file
        # Better to create a temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False, suffix='.csv') as f:
            f.write(csv_content)
            temp_file = f.name
        
        result = citeste_csv(temp_file)
        os.unlink(temp_file)  # Clean up
        
        expected = [
            {'name': 'john', 'city': 'Doe', 'age': '25'},
            {'name': 'jane', 'city': 'Smith', 'age': '30'}
        ]
        self.assertEqual(result, expected)

    def test_citeste_csv_invalid_rows(self):
        csv_content = """name,city,age
John,,25
,Jane,30
Bob,Smith,abc
"""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False, suffix='.csv') as f:
            f.write(csv_content)
            temp_file = f.name
        
        result = citeste_csv(temp_file)
        os.unlink(temp_file)
        
        # Should skip invalid rows
        self.assertEqual(result, [])

    def test_citeste_csv_file_not_found(self):
        result = citeste_csv("nonexistent.csv")
        self.assertEqual(result, [])

    def test_proceseaza_people(self):
        linii = [
            {'name': 'john', 'city': 'New York', 'age': '25'},
            {'name': 'jane', 'city': 'New York', 'age': '30'},
            {'name': 'bob', 'city': 'Los Angeles', 'age': '35'}
        ]
        
        expected_output = """Numar total de persoane: 3
Varsta medie: 30.0
Numar persoane pe orase:
  New York: 2
  Los Angeles: 1
"""
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            proceseaza_people(linii)
        
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()