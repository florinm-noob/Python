import unittest
from datetime import datetime
from vehicle_rental.models import Vehicle

class TestVehicle(unittest.TestCase):
    def test_valid_vehicle_creation(self):
        """Test creating a valid vehicle"""
        v = Vehicle(
            license_plate="ab123cd",
            brand="toyota",
            model="camry",
            year=2020,
            daily_rate=50.0,
            status="none"
        )
        self.assertEqual(v.license_plate, "AB123CD")  # Should be uppercased
        self.assertEqual(v.brand, "Toyota")  # Should be title case
        self.assertEqual(v.model, "Camry")  # Should be title case
        self.assertEqual(v.year, 2020)
        self.assertEqual(v.daily_rate, 50.0)
        self.assertEqual(v.status, "none")

    def test_vehicle_with_defaults(self):
        """Test vehicle with default values"""
        v = Vehicle(
            license_plate="AB123CD",
            brand="Toyota",
            model="Camry",
            year=2020,
            daily_rate=50.0
        )
        self.assertIsNone(v.id)
        self.assertIsNone(v.status)
        self.assertIsNone(v.created_at)

    def test_invalid_year_too_old(self):
        """Test invalid year (too old)"""
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="AB123CD",
                brand="Toyota",
                model="Camry",
                year=1800,
                daily_rate=50.0
            )
        self.assertIn("Invalid year", str(cm.exception))

    def test_invalid_year_future(self):
        """Test invalid year (future)"""
        future_year = datetime.now().year + 2
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="AB123CD",
                brand="Toyota",
                model="Camry",
                year=future_year,
                daily_rate=50.0
            )
        self.assertIn("Invalid year", str(cm.exception))

    def test_invalid_daily_rate_zero(self):
        """Test invalid daily rate (zero)"""
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="AB123CD",
                brand="Toyota",
                model="Camry",
                year=2020,
                daily_rate=0
            )
        self.assertIn("Daily rate must be greater than zero", str(cm.exception))

    def test_invalid_daily_rate_negative(self):
        """Test invalid daily rate (negative)"""
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="AB123CD",
                brand="Toyota",
                model="Camry",
                year=2020,
                daily_rate=-10.0
            )
        self.assertIn("Daily rate must be greater than zero", str(cm.exception))

    def test_invalid_status(self):
        """Test invalid status"""
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="AB123CD",
                brand="Toyota",
                model="Camry",
                year=2020,
                daily_rate=50.0,
                status="invalid"
            )
        self.assertIn("Invalid status", str(cm.exception))

    def test_valid_statuses(self):
        """Test valid statuses"""
        for status in ['none', 'maintenance', 'sold']:
            v = Vehicle(
                license_plate="AB123CD",
                brand="Toyota",
                model="Camry",
                year=2020,
                daily_rate=50.0,
                status=status
            )
            self.assertEqual(v.status, status)

    def test_empty_license_plate(self):
        """Test empty license plate"""
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="",
                brand="Toyota",
                model="Camry",
                year=2020,
                daily_rate=50.0
            )
        self.assertIn("License plate cannot be empty", str(cm.exception))

    def test_whitespace_license_plate(self):
        """Test license plate with only whitespace"""
        with self.assertRaises(ValueError) as cm:
            Vehicle(
                license_plate="   ",
                brand="Toyota",
                model="Camry",
                year=2020,
                daily_rate=50.0
            )
        self.assertIn("License plate cannot be empty", str(cm.exception))

    def test_normalization(self):
        """Test field normalization"""
        v = Vehicle(
            license_plate=" ab123cd ",
            brand=" toyota ",
            model=" camry ",
            year=2020,
            daily_rate=50.0
        )
        self.assertEqual(v.license_plate, "AB123CD")
        self.assertEqual(v.brand, "Toyota")
        self.assertEqual(v.model, "Camry")

if __name__ == '__main__':
    unittest.main()