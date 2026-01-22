def create_tables(conn):
    """
    Create all necessary tables for the vehicle rental system.
    """
    cursor = conn.cursor()

    # Create vehicle table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT UNIQUE NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            daily_rate REAL NOT NULL,
            status TEXT CHECK (status IN ('maintenance', 'sold')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create client table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            license_number TEXT UNIQUE,
            status INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create rental table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rental (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            rental_date DATE NOT NULL,
            return_date DATE,
            status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle (id),
            FOREIGN KEY (client_id) REFERENCES client (id)
        )
    ''')

    # Create maintenance_record table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS maintenance_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL,
            maintenance_date DATE NOT NULL,
            duration_days INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle (id)
        )
    ''')

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ux_rental_active_vehicle
        ON rental(vehicle_id)
        WHERE return_date IS NULL;
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS ix_rental_client_status
        ON rental(client_id, return_date);
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS ix_rental_vehicle_status
        ON rental(vehicle_id, return_date);
    """)

    conn.commit()