import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Enums for type safety - defines valid values for database fields
# ============================================================================

class RoomType(Enum):
    """Enum for room types available in the hotel"""
    SINGLE = "Single"
    DOUBLE = "Double"
    SUITE = "Suite"


class RoomStatus(Enum):
    """Enum for room status values"""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"


class BookingStatus(Enum):
    """Enum for booking status values throughout the booking lifecycle"""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    CHECKED_OUT = "Checked Out"
    CANCELLED = "Cancelled"


# ============================================================================
# Data Classes - represent database records as Python objects
# ============================================================================

@dataclass
class User:
    """Represents a user in the system - can be customer or admin"""
    id: int
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    is_admin: bool
    created_at: str


@dataclass
class Room:
    """Represents a hotel room with all its properties"""
    id: int
    room_number: str
    room_type: str
    price_per_night: float
    capacity: int
    description: str
    amenities: str
    status: str
    image_path: str


@dataclass
class Booking:
    """Represents a room booking with guest and date information"""
    id: int
    user_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str
    created_at: str
    guest_name: str
    guest_email: str
    guest_phone: str
    num_guests: int


@dataclass
class Activity:
    """Represents a system activity log entry for the dashboard"""
    id: int
    description: str
    activity_type: str
    timestamp: str
    user_name: str
    room_number: str


# ============================================================================
# Database Class - Pure data access, no business logic
# ============================================================================

class Database:
    """
    Main database class - handles all database operations.
    Pure data access only - no business logic.
    Uses SQLite for local storage.
    """

    def __init__(self, db_path: str = None):
        """
        Initialize database connection and create tables.

        Args:
            db_path: Path to SQLite database file (auto-generated if None)
        """
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'hotel.db')
        self.db_path = db_path
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection with row factory for dict access.

        Returns:
            sqlite3.Connection configured with Row factory
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """
        Initialize database tables and insert sample data.
        Called once on first run to set up the database.
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create users table - stores both customers and admins
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create rooms table - stores all hotel rooms
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE NOT NULL,
                room_type TEXT NOT NULL,
                price_per_night REAL NOT NULL,
                capacity INTEGER NOT NULL,
                description TEXT,
                amenities TEXT,
                status TEXT DEFAULT 'Available',
                image_path TEXT
            )
        ''')

        # Create bookings table - stores all room bookings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                total_price REAL NOT NULL,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                guest_name TEXT NOT NULL,
                guest_email TEXT,
                guest_phone TEXT,
                num_guests INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (room_id) REFERENCES rooms (id)
            )
        ''')

        # Create activities table - stores activity log for dashboard
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_name TEXT,
                room_number TEXT
            )
        ''')

        conn.commit()
        self._insert_sample_data(cursor)
        conn.commit()
        conn.close()

    # ============================================================================
    # Sample Data Insertion - populates database on first run
    # ============================================================================

    def _insert_sample_data(self, cursor):
        """
        Insert sample data if tables are empty.
        Provides demo data for testing the application.
        """
        # Insert admin user and sample customers
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        if cursor.fetchone()[0] == 0:
            # Admin password placeholder - controller hashes real password
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, is_admin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin@imperialheights.com', 'HASH_PLACEHOLDER', 'Admin', 'User', '0917-555-0100', True))

            # Sample customer accounts
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, is_admin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('juan.delacruz@email.com', 'HASH_PLACEHOLDER', 'Juan', 'Dela Cruz', '0918-555-0101', False))

            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name, phone, is_admin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('maria.clara@email.com', 'HASH_PLACEHOLDER', 'Maria', 'Clara', '0919-555-0102', False))

        # Insert sample rooms with Philippine Peso pricing
        cursor.execute("SELECT COUNT(*) FROM rooms")
        if cursor.fetchone()[0] == 0:
            rooms_data = [
                ('101', 'Single', 1500.0, 1, 'Cozy single room perfect for solo travelers. Features modern amenities and comfortable bedding.', 'WiFi, TV, AC', 'Available'),
                ('102', 'Single', 1500.0, 1, 'Cozy single room perfect for solo travelers. Features modern amenities and comfortable bedding.', 'WiFi, TV, AC', 'Occupied'),
                ('103', 'Double', 2800.0, 2, 'Spacious double room with premium amenities. Ideal for couples or business travelers.', 'WiFi, TV, AC, Coffee', 'Available'),
                ('104', 'Double', 2800.0, 2, 'Spacious double room with premium amenities. Ideal for couples or business travelers.', 'WiFi, TV, AC, Coffee', 'Available'),
                ('105', 'Double', 2800.0, 2, 'Spacious double room with premium amenities. Ideal for couples or business travelers.', 'WiFi, TV, AC, Coffee', 'Occupied'),
                ('201', 'Suite', 5500.0, 4, 'Luxurious suite with separate living area. Perfect for families or extended stays.', 'WiFi, TV, AC, Coffee, Mini Bar', 'Available'),
                ('202', 'Suite', 5500.0, 4, 'Luxurious suite with separate living area. Perfect for families or extended stays.', 'WiFi, TV, AC, Coffee, Mini Bar', 'Occupied'),
                ('203', 'Suite', 6500.0, 4, 'Premium suite with panoramic views and exclusive amenities.', 'WiFi, TV, AC, Coffee, Mini Bar, Jacuzzi', 'Available'),
                ('301', 'Double', 3200.0, 2, 'Executive double room with city views and premium furnishings.', 'WiFi, TV, AC, Coffee, Mini Bar', 'Available'),
                ('302', 'Double', 3200.0, 2, 'Executive double room with city views and premium furnishings.', 'WiFi, TV, AC, Coffee, Mini Bar', 'Occupied'),
                ('303', 'Single', 1800.0, 1, 'Deluxe single room with upgraded amenities and workspace.', 'WiFi, TV, AC, Coffee', 'Available'),
                ('401', 'Suite', 7500.0, 6, 'Presidential suite with multiple bedrooms and butler service.', 'WiFi, TV, AC, Coffee, Mini Bar, Jacuzzi, Butler', 'Available'),
            ]

            for room in rooms_data:
                cursor.execute('''
                    INSERT INTO rooms (room_number, room_type, price_per_night, capacity, description, amenities, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', room)

        # Insert sample bookings
        cursor.execute("SELECT COUNT(*) FROM bookings")
        if cursor.fetchone()[0] == 0:
            today = datetime.now()
            bookings_data = [
                (2, 2, (today - timedelta(days=2)).strftime('%Y-%m-%d'), (today + timedelta(days=1)).strftime('%Y-%m-%d'), 4500.0, 'Checked In', 'Juan Dela Cruz', 'juan.delacruz@email.com', '0918-555-1001', 1),
                (2, 5, (today - timedelta(days=1)).strftime('%Y-%m-%d'), (today + timedelta(days=2)).strftime('%Y-%m-%d'), 8400.0, 'Checked In', 'Maria Clara', 'maria.clara@email.com', '0919-555-1002', 2),
                (3, 7, (today - timedelta(days=3)).strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), 16500.0, 'Checked Out', 'Pedro Santos', 'pedro.santos@email.com', '0917-555-1003', 2),
                (3, 9, today.strftime('%Y-%m-%d'), (today + timedelta(days=3)).strftime('%Y-%m-%d'), 9600.0, 'Confirmed', 'Roberto Reyes', 'roberto.reyes@email.com', '0918-555-1004', 2),
                (2, 10, today.strftime('%Y-%m-%d'), (today + timedelta(days=2)).strftime('%Y-%m-%d'), 6400.0, 'Pending', 'Lisa Aquino', 'lisa.aquino@email.com', '0919-555-1005', 1),
                (3, 12, today.strftime('%Y-%m-%d'), (today + timedelta(days=5)).strftime('%Y-%m-%d'), 37500.0, 'Confirmed', 'Jose Ramos', 'jose.ramos@email.com', '0917-555-1006', 4),
            ]

            for booking in bookings_data:
                cursor.execute('''
                    INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date, total_price, status, guest_name, guest_email, guest_phone, num_guests)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', booking)

        # Insert sample activities for the dashboard
        cursor.execute("SELECT COUNT(*) FROM activities")
        if cursor.fetchone()[0] == 0:
            today = datetime.now()
            activities_data = [
                ('Checked in - Room 205', 'checkin', (today - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), 'Juan Dela Cruz', '205'),
                ('New booking - Room 312', 'booking', (today - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'), 'Maria Clara', '312'),
                ('Checked out - Room 108', 'checkout', (today - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'), 'Pedro Santos', '108'),
                ('Checked in - Room 420', 'checkin', (today - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'), 'Sarah Santos', '420'),
                ('New booking - Room 215', 'booking', (today - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'), 'David Lee', '215'),
            ]

            for activity in activities_data:
                cursor.execute('''
                    INSERT INTO activities (description, activity_type, timestamp, user_name, room_number)
                    VALUES (?, ?, ?, ?, ?)
                ''', activity)

    # ============================================================================
    # User Operations - CRUD for user accounts
    # ============================================================================

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(**dict(row))
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User's unique ID

        Returns:
            User object if found, None otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(**dict(row))
        return None

    def create_user(self, email: str, password: str, first_name: str, last_name: str,
                    phone: str = "", is_admin: bool = False) -> int:
        """
        Create a new user in the database.

        Args:
            email: User's email (unique)
            password: Hashed password
            first_name: First name
            last_name: Last name
            phone: Phone number (optional)
            is_admin: Admin flag (default False)

        Returns:
            ID of the newly created user
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, password, first_name, last_name, phone, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, password, first_name, last_name, phone, is_admin))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    def update_user(self, user_id: int, **kwargs) -> bool:
        """
        Update user information.

        Args:
            user_id: User's unique ID
            **kwargs: Fields to update (email, password, first_name, last_name, phone)

        Returns:
            True if update was successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        allowed_fields = ['email', 'password', 'first_name', 'last_name', 'phone']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if updates:
            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [user_id]
            cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    # ============================================================================
    # Room Operations - CRUD for hotel rooms
    # ============================================================================

    def get_all_rooms(self) -> List[Room]:
        """
        Get all rooms ordered by room number.

        Returns:
            List of Room objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms ORDER BY room_number")
        rows = cursor.fetchall()
        conn.close()
        return [Room(**dict(row)) for row in rows]

    def get_rooms_by_type(self, room_type: str) -> List[Room]:
        """
        Get rooms filtered by type.

        Args:
            room_type: Room type to filter by

        Returns:
            List of Room objects matching the type
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE room_type = ? ORDER BY room_number", (room_type,))
        rows = cursor.fetchall()
        conn.close()
        return [Room(**dict(row)) for row in rows]

    def get_available_rooms(self, check_in: str = None, check_out: str = None) -> List[Room]:
        """
        Get available rooms for date range.

        Args:
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)

        Returns:
            List of available Room objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        if check_in and check_out:
            cursor.execute('''
                SELECT * FROM rooms
                WHERE id NOT IN (
                    SELECT room_id FROM bookings
                    WHERE status IN ('Confirmed', 'Checked In', 'Pending')
                    AND ((check_in_date <= ? AND check_out_date >= ?)
                         OR (check_in_date <= ? AND check_out_date >= ?)
                         OR (check_in_date >= ? AND check_out_date <= ?))
                )
                AND status = 'Available'
                ORDER BY room_number
            ''', (check_out, check_in, check_out, check_in, check_in, check_out))
        else:
            cursor.execute("SELECT * FROM rooms WHERE status = 'Available' ORDER BY room_number")
        rows = cursor.fetchall()
        conn.close()
        return [Room(**dict(row)) for row in rows]

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        """
        Get room by ID.

        Args:
            room_id: Room's unique ID

        Returns:
            Room object if found, None otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Room(**dict(row))
        return None

    def update_room_status(self, room_id: int, status: str) -> bool:
        """
        Update room status.

        Args:
            room_id: Room's unique ID
            status: New status string

        Returns:
            True if update was successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE rooms SET status = ? WHERE id = ?", (status, room_id))
        conn.commit()
        conn.close()
        return True

    def create_room(self, room_number: str, room_type: str, price_per_night: float,
                    capacity: int, description: str, amenities: str) -> int:
        """
        Create a new room.

        Args:
            room_number: Room number string
            room_type: Type of room
            price_per_night: Price in Philippine Peso
            capacity: Maximum guests
            description: Room description
            amenities: Comma-separated amenities list

        Returns:
            ID of the newly created room
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rooms (room_number, room_type, price_per_night, capacity, description, amenities, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Available')
        ''', (room_number, room_type, price_per_night, capacity, description, amenities))
        room_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return room_id

    # ============================================================================
    # Booking Operations - CRUD for bookings
    # ============================================================================

    def create_booking(self, user_id: int, room_id: int, check_in_date: str,
                       check_out_date: str, total_price: float, guest_name: str,
                       guest_email: str = "", guest_phone: str = "",
                       num_guests: int = 1) -> int:
        """
        Create a new booking.

        Args:
            user_id: ID of the booking user
            room_id: ID of the room to book
            check_in_date: Check-in date (YYYY-MM-DD)
            check_out_date: Check-out date (YYYY-MM-DD)
            total_price: Calculated total price
            guest_name: Primary guest name
            guest_email: Guest email (optional)
            guest_phone: Guest phone (optional)
            num_guests: Number of guests (default 1)

        Returns:
            ID of the newly created booking
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date,
                                total_price, status, guest_name, guest_email,
                                guest_phone, num_guests)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?, ?, ?, ?)
        ''', (user_id, room_id, check_in_date, check_out_date, total_price,
              guest_name, guest_email, guest_phone, num_guests))
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return booking_id

    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """
        Get booking by ID.

        Args:
            booking_id: Booking's unique ID

        Returns:
            Booking object if found, None otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Booking(**dict(row))
        return None

    def get_user_bookings(self, user_id: int) -> List[Booking]:
        """
        Get all bookings for a specific user.

        Args:
            user_id: User's unique ID

        Returns:
            List of Booking objects for the user
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM bookings
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Booking(**dict(row)) for row in rows]

    def get_all_bookings(self) -> List[Booking]:
        """
        Get all bookings.

        Returns:
            List of all Booking objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM bookings
            ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [Booking(**dict(row)) for row in rows]

    def get_today_checkins(self) -> List[Dict]:
        """
        Get today's check-ins.

        Returns:
            List of dicts with booking and room info
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT b.*, r.room_number
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.check_in_date = ? AND b.status IN ('Confirmed', 'Pending')
            ORDER BY b.check_in_date
        ''', (today,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_today_checkouts(self) -> List[Dict]:
        """
        Get today's check-outs.

        Returns:
            List of dicts with booking and room info
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT b.*, r.room_number
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.check_out_date = ? AND b.status = 'Checked In'
            ORDER BY b.check_out_date
        ''', (today,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_booking_status(self, booking_id: int, status: str) -> bool:
        """
        Update booking status.

        Args:
            booking_id: Booking's unique ID
            status: New status string

        Returns:
            True if update was successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
        conn.commit()
        conn.close()
        return True

    # ============================================================================
    # Activity Operations - Dashboard activity log
    # ============================================================================

    def add_activity(self, description: str, activity_type: str,
                     user_name: str = "", room_number: str = "") -> int:
        """
        Add a new activity log entry.

        Args:
            description: Activity description
            activity_type: Type of activity (checkin, checkout, booking, etc.)
            user_name: User associated with the activity
            room_number: Room associated with the activity

        Returns:
            ID of the newly created activity
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activities (description, activity_type, user_name, room_number)
            VALUES (?, ?, ?, ?)
        ''', (description, activity_type, user_name, room_number))
        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return activity_id

    def get_recent_activities(self, limit: int = 10) -> List[Activity]:
        """
        Get recent activities.

        Args:
            limit: Maximum number of activities to return

        Returns:
            List of Activity objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM activities
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [Activity(**dict(row)) for row in rows]

    # ============================================================================
    # Statistics - Dashboard data aggregation
    # ============================================================================

    def get_dashboard_stats(self) -> Dict:
        """
        Get dashboard statistics.

        Returns:
            Dict with keys: total_rooms, occupied_rooms, total_guests,
            checking_out_today, total_bookings, pending_bookings, weekly_revenue
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rooms")
        total_rooms = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM rooms WHERE status = 'Occupied'")
        occupied_rooms = cursor.fetchone()[0]
        cursor.execute('''
            SELECT COALESCE(SUM(num_guests), 0) FROM bookings
            WHERE status = 'Checked In'
        ''')
        total_guests = cursor.fetchone()[0]
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) FROM bookings
            WHERE check_out_date = ? AND status = 'Checked In'
        ''', (today,))
        checking_out_today = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bookings")
        total_bookings = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Pending'")
        pending_bookings = cursor.fetchone()[0]
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COALESCE(SUM(total_price), 0) FROM bookings
            WHERE status IN ('Checked Out', 'Checked In', 'Confirmed')
            AND created_at >= ?
        ''', (week_ago,))
        weekly_revenue = cursor.fetchone()[0]
        conn.close()
        return {
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'total_guests': total_guests,
            'checking_out_today': checking_out_today,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'weekly_revenue': weekly_revenue
        }

    def get_all_guests(self) -> List[Dict]:
        """
        Get all guests with booking info.

        Returns:
            List of dicts with guest info and booking statistics
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT u.id, u.first_name, u.last_name, u.email, u.phone,
                   COUNT(b.id) as total_bookings,
                   MAX(b.check_in_date) as last_checkin
            FROM users u
            LEFT JOIN bookings b ON u.id = b.user_id
            WHERE u.is_admin = 0
            GROUP BY u.id
            ORDER BY u.last_name
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ============================================================================
    # Export Operations - Data export for reports
    # ============================================================================

    def get_bookings_in_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get bookings within a date range for export.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of dicts with booking data
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, r.room_number
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.created_at >= ? AND b.created_at <= ?
            ORDER BY b.created_at DESC
        ''', (start_date, end_date))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


# ============================================================================
# Global database instance - shared across the application
# ============================================================================
db = Database()
