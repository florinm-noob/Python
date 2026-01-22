import os

# paths.py este în:
# backend/src/vehicle_rental/db/paths.py

# Plecăm de la acest fișier și urcăm până la backend/
CURRENT_FILE = os.path.abspath(__file__)

# .../backend/src/vehicle_rental/db
DB_DIR = os.path.dirname(CURRENT_FILE)

# .../backend/src/vehicle_rental
PACKAGE_DIR = os.path.dirname(DB_DIR)

# .../backend/src
SRC_DIR = os.path.dirname(PACKAGE_DIR)

# .../backend
BACKEND_DIR = os.path.dirname(SRC_DIR)

# backend/data și backend/logs
DATA_DIR = os.path.join(BACKEND_DIR, "data")
LOGS_DIR = os.path.join(BACKEND_DIR, "logs")

# DB path
DB_PATH = os.path.join(DATA_DIR, "vehicle_rental.db")
