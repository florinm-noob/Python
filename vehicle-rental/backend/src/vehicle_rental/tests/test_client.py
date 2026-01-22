import unittest
from datetime import datetime
from vehicle_rental.models import Client

class TestClient(unittest.TestCase):
    def test_valid_client_creation(self):
        """Test creating a valid client"""
        c = Client(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            license_number="DL123456"
        )
        self.assertEqual(c.first_name, "John")
        self.assertEqual(c.last_name, "Doe")
        self.assertEqual(c.email, "john.doe@example.com")
        self.assertEqual(c.status, 1)
        self.assertIsNone(c.id)
        self.assertEqual(c.phone, "123-456-7890")
        self.assertEqual(c.license_number, "DL123456")
        self.assertIsNone(c.created_at)

    def test_client_with_whitespace_stripping(self):
        """Test that whitespace is stripped from names and email"""
        c = Client(
            first_name="  John  ",
            last_name="  Doe  ",
            email="  JOHN.DOE@EXAMPLE.COM  "
        )
        self.assertEqual(c.first_name, "John")
        self.assertEqual(c.last_name, "Doe")
        self.assertEqual(c.email, "john.doe@example.com")

    def test_client_with_custom_status(self):
        """Test client with custom status"""
        c = Client(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            status=0
        )
        self.assertEqual(c.status, 0)

    def test_client_with_all_fields(self):
        """Test client with all fields including id and created_at"""
        created_time = datetime.now()
        c = Client(
            first_name="Alice",
            last_name="Wonder",
            email="alice.wonder@example.com",
            status=1,
            id=123,
            phone="987-654-3210",
            license_number="DL789012",
            created_at=created_time
        )
        self.assertEqual(c.id, 123)
        self.assertEqual(c.created_at, created_time)

    def test_invalid_status(self):
        """Test that invalid status raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Client(
                first_name="Bob",
                last_name="Builder",
                email="bob.builder@example.com",
                status=2
            )
        self.assertIn("Invalid status", str(context.exception))

    def test_empty_first_name(self):
        """Test that empty first name raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Client(
                first_name="",
                last_name="Doe",
                email="john.doe@example.com"
            )
        self.assertIn("First name cannot be empty", str(context.exception))

    def test_empty_last_name(self):
        """Test that empty last name raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Client(
                first_name="John",
                last_name="",
                email="john.doe@example.com"
            )
        self.assertIn("Last name cannot be empty", str(context.exception))

    def test_empty_email(self):
        """Test that empty email raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Client(
                first_name="John",
                last_name="Doe",
                email=""
            )
        self.assertIn("Email cannot be empty", str(context.exception))

    def test_invalid_email_format(self):
        """Test that invalid email format raises ValueError"""
        with self.assertRaises(ValueError) as context:
            Client(
                first_name="John",
                last_name="Doe",
                email="invalid-email"
            )
        self.assertIn("Invalid email format", str(context.exception))

    def test_whitespace_only_names(self):
        """Test that whitespace-only names are treated as empty"""
        with self.assertRaises(ValueError):
            Client(
                first_name="   ",
                last_name="Doe",
                email="john.doe@example.com"
            )
        with self.assertRaises(ValueError):
            Client(
                first_name="John",
                last_name="   ",
                email="john.doe@example.com"
            )

if __name__ == '__main__':
    unittest.main()