from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import re

@dataclass
class Client:
    first_name: str
    last_name: str
    email: str
    status: int = 1 # 1 for active, 0 for inactive
    id: Optional[int] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.email = self.email.strip().lower()
        if self.status not in (0, 1):
            raise ValueError(f"Invalid status: {self.status}") 
        if not self.first_name:
            raise ValueError("First name cannot be empty")
        if not self.last_name:
            raise ValueError("Last name cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email):
            raise ValueError(f"Invalid email format: {self.email}. Expected format: something@something.com")
