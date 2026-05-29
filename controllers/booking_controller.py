"""
Booking Controller for Imperial Heights Hotel Management System
Handles all booking operations, room management, and business logic
Activities are managed here (not in the model) as requested
No database transactions in the model - all business logic is here
"""

from typing import List, Optional, Dict
from datetime import datetime, timedelta
import csv
import os
from PyQt6.QtCore import QObject, pyqtSignal
from models.database import Database, Room, Booking


class BookingController(QObject):
    """
    Controller for handling booking and room operations.
    Contains all business logic - model is pure data access only.
    No transactions in the model layer.
    """

    # Signals for view updates - decouples controller from UI
    booking_created = pyqtSignal(int)           # Emits booking ID
    booking_cancelled = pyqtSignal(int)         # Emits cancelled booking ID
    booking_status_changed = pyqtSignal(int, str)  # booking_id, new_status
    room_updated = pyqtSignal(int)              # Emits room ID
    error_occurred = pyqtSignal(str)            # Error message

    def __init__(self, database: Database):
        """
        Initialize booking controller.

        Args:
            database: Database instance for data operations
        """
        super().__init__()
        self.db = database

    # ============================================================================
    # Room Operations - retrieve room information
    # ============================================================================

    def get_all_rooms(self) -> List[Room]:
        """Get all rooms from database."""
        return self.db.get_all_rooms()

    def get_rooms_by_type(self, room_type: str) -> List[Room]:
        """Get rooms filtered by type."""
        if room_type == "All":
            return self.get_all_rooms()
        return self.db.get_rooms_by_type(room_type)

    def get_available_rooms(self, check_in: str = None, check_out: str = None) -> List[Room]:
        """Get available rooms for a date range."""
        return self.db.get_available_rooms(check_in, check_out)

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        """Get a single room by ID."""
        return self.db.get_room_by_id(room_id)

    # ============================================================================
    # Price Calculations - business logic for pricing
    # ============================================================================

    def calculate_total_price(self, room: Room, check_in: str, check_out: str) -> float:
        """
        Calculate total price for a booking.

        Args:
            room: Room object with price_per_night
            check_in: Check-in date string (YYYY-MM-DD)
            check_out: Check-out date string (YYYY-MM-DD)

        Returns:
            Total price for the stay
        """
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
            nights = (check_out_date - check_in_date).days
            if nights <= 0:
                return 0
            return room.price_per_night * nights
        except:
            return 0

    # ============================================================================
    # Booking Creation - validates and creates bookings
    # ============================================================================

    def create_booking(self, user_id: int, room_id: int, check_in_date: str,
                       check_out_date: str, guest_name: str, guest_email: str = "",
                       guest_phone: str = "", num_guests: int = 1) -> Optional[int]:
        """
        Create a new booking with validation.
        All business logic is here - model just stores data.

        Args:
            user_id: ID of the booking user
            room_id: ID of the room to book
            check_in_date: Check-in date (YYYY-MM-DD)
            check_out_date: Check-out date (YYYY-MM-DD)
            guest_name: Primary guest name
            guest_email: Guest email (optional)
            guest_phone: Guest phone (optional)
            num_guests: Number of guests

        Returns:
            Booking ID if successful, None otherwise
        """
        # Validate dates
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d')

            if check_in < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                self.error_occurred.emit("Check-in date cannot be in the past")
                return None

            if check_out <= check_in:
                self.error_occurred.emit("Check-out date must be after check-in date")
                return None
        except ValueError:
            self.error_occurred.emit("Invalid date format")
            return None

        # Validate room exists
        room = self.db.get_room_by_id(room_id)
        if not room:
            self.error_occurred.emit("Room not found")
            return None

        # Check room availability
        available_rooms = self.db.get_available_rooms(check_in_date, check_out_date)
        if not any(r.id == room_id for r in available_rooms):
            self.error_occurred.emit("Room is not available for selected dates")
            return None

        # Calculate price
        total_price = self.calculate_total_price(room, check_in_date, check_out_date)

        # Create booking in database
        try:
            booking_id = self.db.create_booking(
                user_id=user_id,
                room_id=room_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                total_price=total_price,
                guest_name=guest_name,
                guest_email=guest_email,
                guest_phone=guest_phone,
                num_guests=num_guests
            )

            if booking_id:
                # Log activity (business logic - not in model)
                self.db.add_activity(
                    f'New booking - Room {room.room_number}',
                    'booking',
                    guest_name,
                    room.room_number
                )
                self.booking_created.emit(booking_id)
                return booking_id
            else:
                self.error_occurred.emit("Failed to create booking")
                return None
        except Exception as e:
            self.error_occurred.emit(f"Booking error: {str(e)}")
            return None

    # ============================================================================
    # Booking Retrieval - get booking information
    # ============================================================================

    def get_user_bookings(self, user_id: int) -> List[Booking]:
        """Get all bookings for a specific user."""
        return self.db.get_user_bookings(user_id)

    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings (admin only)."""
        return self.db.get_all_bookings()

    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get a single booking by ID."""
        return self.db.get_booking_by_id(booking_id)

    # ============================================================================
    # Booking Status Changes - checkin, checkout, cancel
    # ============================================================================

    def cancel_booking(self, booking_id: int) -> bool:
        """Cancel a booking."""
        try:
            booking = self.db.get_booking_by_id(booking_id)
            success = self.db.update_booking_status(booking_id, 'Cancelled')
            if success and booking:
                room = self.db.get_room_by_id(booking.room_id)
                if room:
                    self.db.add_activity(
                        f'Booking cancelled - Room {room.room_number}',
                        'cancel',
                        booking.guest_name,
                        room.room_number
                    )
                self.booking_cancelled.emit(booking_id)
            return success
        except Exception as e:
            self.error_occurred.emit(f"Cancel error: {str(e)}")
            return False

    def check_in(self, booking_id: int) -> bool:
        """Check in a guest."""
        try:
            booking = self.db.get_booking_by_id(booking_id)
            success = self.db.update_booking_status(booking_id, 'Checked In')
            if success and booking:
                room = self.db.get_room_by_id(booking.room_id)
                if room:
                    self.db.update_room_status(booking.room_id, 'Occupied')
                    self.db.add_activity(
                        f'Checked in - Room {room.room_number}',
                        'checkin',
                        booking.guest_name,
                        room.room_number
                    )
                self.booking_status_changed.emit(booking_id, 'Checked In')
            return success
        except Exception as e:
            self.error_occurred.emit(f"Check-in error: {str(e)}")
            return False

    def check_out(self, booking_id: int) -> bool:
        """Check out a guest."""
        try:
            booking = self.db.get_booking_by_id(booking_id)
            success = self.db.update_booking_status(booking_id, 'Checked Out')
            if success and booking:
                room = self.db.get_room_by_id(booking.room_id)
                if room:
                    self.db.update_room_status(booking.room_id, 'Available')
                    self.db.add_activity(
                        f'Checked out - Room {room.room_number}',
                        'checkout',
                        booking.guest_name,
                        room.room_number
                    )
                self.booking_status_changed.emit(booking_id, 'Checked Out')
            return success
        except Exception as e:
            self.error_occurred.emit(f"Check-out error: {str(e)}")
            return False

    def confirm_booking(self, booking_id: int) -> bool:
        """Confirm a pending booking."""
        try:
            success = self.db.update_booking_status(booking_id, 'Confirmed')
            if success:
                self.booking_status_changed.emit(booking_id, 'Confirmed')
            return success
        except Exception as e:
            self.error_occurred.emit(f"Confirm error: {str(e)}")
            return False

    # ============================================================================
    # Dashboard Data - statistics and activity feeds
    # ============================================================================

    def get_today_checkins(self) -> List[Dict]:
        """Get today's check-ins."""
        return self.db.get_today_checkins()

    def get_today_checkouts(self) -> List[Dict]:
        """Get today's check-outs."""
        return self.db.get_today_checkouts()

    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics."""
        return self.db.get_dashboard_stats()

    def get_recent_activities(self, limit: int = 10) -> List:
        """Get recent activity log entries."""
        return self.db.get_recent_activities(limit)

    # ============================================================================
    # Room Management (Admin) - create and update rooms
    # ============================================================================

    def create_room(self, room_number: str, room_type: str, price_per_night: float,
                    capacity: int, description: str, amenities: str) -> Optional[int]:
        """Create a new room (admin only)."""
        try:
            room_id = self.db.create_room(
                room_number=room_number,
                room_type=room_type,
                price_per_night=price_per_night,
                capacity=capacity,
                description=description,
                amenities=amenities
            )
            if room_id:
                self.db.add_activity(f'New room added - Room {room_number}', 'room_add', '', room_number)
                self.room_updated.emit(room_id)
                return room_id
            else:
                self.error_occurred.emit("Failed to create room")
                return None
        except Exception as e:
            self.error_occurred.emit(f"Create room error: {str(e)}")
            return None

    def update_room_status(self, room_id: int, status: str) -> bool:
        """Update room status (admin only)."""
        try:
            success = self.db.update_room_status(room_id, status)
            if success:
                self.room_updated.emit(room_id)
            return success
        except Exception as e:
            self.error_occurred.emit(f"Update room error: {str(e)}")
            return False

    # ============================================================================
    # Guest Management (Admin) - view guest information
    # ============================================================================

    def get_all_guests(self) -> List[Dict]:
        """Get all guests (admin only)."""
        return self.db.get_all_guests()

    # ============================================================================
    # Data Export - CSV export for admin use only
    # ============================================================================

    def export_bookings_to_csv(self, start_date: str, end_date: str, file_path: str) -> bool:
        """
        Export bookings in date range to CSV file.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            file_path: Path to save CSV file

        Returns:
            True if export successful, False otherwise
        """
        try:
            bookings = self.db.get_bookings_in_range(start_date, end_date)
            if not bookings:
                return False

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['guest_name', 'room_number', 'check_in_date', 'check_out_date',
                             'total_price', 'status', 'guest_email', 'guest_phone', 'num_guests']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for booking in bookings:
                    row = {k: booking.get(k, '') for k in fieldnames}
                    writer.writerow(row)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Export error: {str(e)}")
            return False

    def export_guests_to_csv(self, file_path: str) -> bool:
        """
        Export all guests to CSV file.

        Args:
            file_path: Path to save CSV file

        Returns:
            True if export successful, False otherwise
        """
        try:
            guests = self.db.get_all_guests()
            if not guests:
                return False

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['first_name', 'last_name', 'email', 'phone', 'total_bookings', 'last_checkin']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for guest in guests:
                    row = {k: guest.get(k, '') for k in fieldnames}
                    writer.writerow(row)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Export error: {str(e)}")
            return False

    def export_rooms_to_csv(self, file_path: str) -> bool:
        """
        Export all rooms to CSV file.

        Args:
            file_path: Path to save CSV file

        Returns:
            True if export successful, False otherwise
        """
        try:
            rooms = self.db.get_all_rooms()
            if not rooms:
                return False

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['room_number', 'room_type', 'price_per_night', 'capacity', 'status', 'amenities']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for room in rooms:
                    row = {
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'price_per_night': room.price_per_night,
                        'capacity': room.capacity,
                        'status': room.status,
                        'amenities': room.amenities
                    }
                    writer.writerow(row)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Export error: {str(e)}")
            return False
