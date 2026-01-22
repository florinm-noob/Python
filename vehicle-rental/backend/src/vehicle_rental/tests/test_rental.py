import unittest
from datetime import datetime
from vehicle_rental.models import Rental

class TestRental(unittest.TestCase):
    def test_valid_rental_creation(self):
        """Test creating a valid rental"""
        r = Rental(
            vehicle_id=1,
            client_id=1,
            rental_date=datetime(2024, 1, 1).date(),
            status="active"
        )
        self.assertEqual(r.vehicle_id, 1)
        self.assertEqual(r.client_id, 1)
        self.assertEqual(r.rental_date, datetime(2024, 1, 1).date())
        self.assertEqual(r.status, "active")
        self.assertIsNone(r.id)
        self.assertIsNone(r.created_at)
        self.assertIsNone(r.return_date)

    def test_rental_with_defaults(self):
        """Test rental with default values"""
        r = Rental(
            vehicle_id=2,
            client_id=2,
            rental_date=datetime(2024, 2, 1).date()
        )
        self.assertIsNone(r.return_date)
        self.assertEqual(r.status, "active")
        self.assertIsNone(r.id)
        self.assertIsNone(r.created_at)

    def test_invalid_status(self):
        """Test invalid status"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=3,
                client_id=3,
                rental_date=datetime(2024, 3, 1).date(),
                status="invalid_status"
            )
        self.assertIn("Invalid status", str(cm.exception))

    def test_rental_with_all_fields(self):
        """Test rental with all fields including id and created_at"""
        created_time = datetime.now()
        r = Rental(
            vehicle_id=4,
            client_id=4,
            rental_date=datetime(2024, 4, 1).date(),
            return_date=datetime(2024, 4, 15).date(),
            status="completed",
            id=456,
            created_at=created_time
        )
        self.assertEqual(r.id, 456)
        self.assertEqual(r.created_at, created_time)

    def test_invalid_return_date(self):
        """Test that return_date cannot be before rental_date"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=5,
                client_id=5,
                rental_date=datetime(2024, 5, 1).date(),
                return_date=datetime(2024, 4, 30).date(),
                status="completed"
            )
        self.assertIn("Return date cannot be before rental date", str(cm.exception))

    def test_rental_return(self):
        """Test returning a rental by updating status and return_date"""
        r = Rental(
            vehicle_id=6,
            client_id=6,
            rental_date=datetime(2024, 6, 1).date(),
            status="completed",
            return_date=datetime(2024, 6, 10).date()
        )
        self.assertEqual(r.status, "completed")
        self.assertEqual(r.return_date, datetime(2024, 6, 10).date())

    def test_active_with_return_date_raises(self):
        """Test that an active rental cannot have a return_date"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=7,
                client_id=7,
                rental_date=datetime(2024, 7, 1).date(),
                status="active",
                return_date=datetime(2024, 7, 10).date()
            )
        self.assertIn("Return date must be None when status is active", str(cm.exception))

    def test_completed_without_return_date_raises(self):
        """Test that a completed rental must have a return_date"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=8,
                client_id=8,
                rental_date=datetime(2024, 8, 1).date(),
                status="completed"
            )
        self.assertIn("Return date must be set when status is completed", str(cm.exception))
    
    def test_cancelled_without_return_date_raises(self):
        """Test that a cancelled rental must have a return_date"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=9,
                client_id=9,
                rental_date=datetime(2024, 9, 1).date(),
                status="cancelled"
            )
        self.assertIn("Return date must be set when status is cancelled", str(cm.exception))

    def test_completed_with_return_date_ok(self):
        """Test that a completed rental with return_date is valid"""
        r = Rental(
            vehicle_id=10,
            client_id=10,
            rental_date=datetime(2024, 10, 1).date(),
            status="completed",
            return_date=datetime(2024, 10, 15).date()
        )
        self.assertEqual(r.status, "completed")
        self.assertEqual(r.return_date, datetime(2024, 10, 15).date())
    
    def test_cancelled_with_return_date_ok(self):
        """Test that a cancelled rental with return_date is valid"""
        r = Rental(
            vehicle_id=11,
            client_id=11,
            rental_date=datetime(2024, 11, 1).date(),
            status="cancelled",
            return_date=datetime(2024, 11, 5).date()
        )
        self.assertEqual(r.status, "cancelled")
        self.assertEqual(r.return_date, datetime(2024, 11, 5).date())

    def test_invalid_vehicle_id(self):
        """Test that invalid vehicle_id raises ValueError"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=0,
                client_id=12,
                rental_date=datetime(2024, 12, 1).date()
            )
        self.assertIn("Invalid vehicle ID", str(cm.exception))
    
    def test_invalid_client_id(self):
        """Test that invalid client_id raises ValueError"""
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=12,
                client_id=-1,
                rental_date=datetime(2024, 12, 1).date()
            )
        self.assertIn("Invalid client ID", str(cm.exception))
    
    def test_rental_date_in_future(self):
        """Test that rental_date in the future raises ValueError"""
        future_date = datetime.now().date().replace(year=datetime.now().year + 1)
        with self.assertRaises(ValueError) as cm:
            Rental(
                vehicle_id=13,
                client_id=13,
                rental_date=future_date
            )
        self.assertIn("Rental date cannot be in the future", str(cm.exception))

if __name__ == '__main__':
    unittest.main()