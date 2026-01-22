#!/usr/bin/env python3
"""
Main entry point for the Vehicle Rental System.
"""

from vehicle_rental.db.connection import initialize_database

def main():
    print("Initializing Vehicle Rental Database...")
    initialize_database()
    print("Application started successfully.")

if __name__ == "__main__":
    main()