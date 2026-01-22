from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class MaintenanceRecord:
    vehicle_id: int
    description: str
    cost: float
    maintenance_date: date
    id: Optional[int] = None
    duration_days: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.description = self.description.strip()

        if self.vehicle_id <= 0:
            raise ValueError(f"Invalid vehicle ID: {self.vehicle_id}")

        if not self.description:
            raise ValueError("Description cannot be empty")

        if self.cost < 0:
            raise ValueError(f"Cost cannot be negative: {self.cost}")

        if self.maintenance_date > date.today():
            raise ValueError("Maintenance date cannot be in the future")

        if self.duration_days is not None and self.duration_days <= 0:
            raise ValueError(f"Duration days must be positive: {self.duration_days}")