from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Vehicle:
    license_plate: str
    brand: str
    model: str
    year: int
    daily_rate: float
    id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.license_plate = self.license_plate.strip().upper()
        self.brand = self.brand.strip().title()
        self.model = self.model.strip().title()
        if self.year < 1900 or self.year > datetime.now().year + 1:
            raise ValueError(f"Invalid year: {self.year}")
        if self.daily_rate <= 0:
            raise ValueError(f"Daily rate must be greater than zero: {self.daily_rate}")
        if self.status and self.status not in ['none','rented', 'maintenance']:
            raise ValueError(f"Invalid status: {self.status}")
        if not self.license_plate or self.license_plate == "":
            raise ValueError("License plate cannot be empty")