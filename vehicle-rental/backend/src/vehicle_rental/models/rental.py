from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime

@dataclass
class Rental:
    vehicle_id: int
    client_id: int
    rental_date: date
    status: str = 'active'  # 'active', 'completed', 'cancelled'
    id: Optional[int] = None
    return_date: Optional[date] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.status not in ['active', 'completed', 'cancelled']:
            raise ValueError(f"Invalid status: {self.status}")
        if self.rental_date > date.today():
            raise ValueError("Rental date cannot be in the future")
        if self.return_date and self.return_date < self.rental_date:
            raise ValueError("Return date cannot be before rental date")
        if self.vehicle_id <= 0:
            raise ValueError(f"Invalid vehicle ID: {self.vehicle_id}")
        if self.client_id <= 0:
            raise ValueError(f"Invalid client ID: {self.client_id}")
        if self.status == 'active' and self.return_date:
                raise ValueError("Return date must be None when status is active")
        if self.status in ['completed', 'cancelled'] and not self.return_date:
            raise ValueError(f"Return date must be set when status is {self.status}")