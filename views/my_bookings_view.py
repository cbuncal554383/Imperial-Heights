"""
My Bookings View for Imperial Heights Hotel Management System
Customer view for viewing and managing their reservations
Uses Philippine Peso formatting, no emojis, no visible IDs
Clean card layout with no unnecessary borders
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, peso_format, get_icon


class BookingCard(QFrame):
    """
    Card widget for displaying a single booking.
    No ID shown, clean styling with status badge.
    No unnecessary borders.
    """

    cancel_clicked = pyqtSignal(int)  # Emits booking_id for cancellation

    def __init__(self, booking: dict, parent=None):
        super().__init__(parent)
        self.booking = booking
        self.init_ui()

    def init_ui(self):
        """Build booking card with room info and actions."""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 14px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)

        # Left side - Room and guest info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)

        # Room number and status
        header_layout = QHBoxLayout()

        room_label = QLabel(f"Room {self.booking.get('room_number', 'N/A')}")
        room_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(room_label)

        header_layout.addStretch()

        # Status badge with color - high contrast
        status = self.booking.get('status', 'Pending')
        status_colors = {
            'Pending': COLORS['status_pending'],
            'Confirmed': COLORS['status_confirmed'],
            'Checked In': COLORS['status_available'],
            'Checked Out': COLORS['text_muted'],
            'Cancelled': COLORS['status_occupied']
        }
        status_color = status_colors.get(status, COLORS['text_muted'])

        status_label = QLabel(f"  {status}  ")
        status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color};
                color: white;
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(status_label)
        info_layout.addLayout(header_layout)

        # Guest name
        guest_name = self.booking.get('guest_name', 'Guest')
        guest_label = QLabel(f"Guest: {guest_name}")
        guest_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        info_layout.addWidget(guest_label)

        # Dates with calendar icon
        dates_layout = QHBoxLayout()
        dates_layout.setSpacing(6)
        date_icon = QLabel()
        date_icon.setPixmap(get_icon('calendar', COLORS['text_muted']).pixmap(12, 12))
        dates_layout.addWidget(date_icon)
        check_in = self.booking.get('check_in_date', 'N/A')
        check_out = self.booking.get('check_out_date', 'N/A')
        dates_label = QLabel(f"{check_in}  to  {check_out}")
        dates_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        dates_layout.addWidget(dates_label)
        dates_layout.addStretch()
        info_layout.addLayout(dates_layout)

        # Number of guests
        num_guests = self.booking.get('num_guests', 1)
        guests_label = QLabel(f"{num_guests} Guest{'s' if num_guests > 1 else ''}")
        guests_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        info_layout.addWidget(guests_label)

        layout.addLayout(info_layout, 1)

        # Right side - Price and actions
        action_layout = QVBoxLayout()
        action_layout.setSpacing(10)
        action_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Total price in Philippine Peso
        total_price = self.booking.get('total_price', 0)
        price_label = QLabel(peso_format(total_price))
        price_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 22px; font-weight: bold;")
        action_layout.addWidget(price_label)

        # Cancel button - visible with clear styling (only for pending/confirmed)
        if status in ['Pending', 'Confirmed']:
            cancel_btn = QPushButton("  Cancel")
            cancel_btn.setIcon(get_icon('cancel', COLORS['status_occupied']))
            cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            cancel_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['status_occupied']};
                    border: 1px solid {COLORS['status_occupied']};
                    border-radius: 8px;
                    padding: 6px 14px;
                    font-size: 12px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['status_occupied']};
                    color: white;
                }}
            """)
            cancel_btn.clicked.connect(self.on_cancel_clicked)
            action_layout.addWidget(cancel_btn)

        layout.addLayout(action_layout)

    def on_cancel_clicked(self):
        """Show confirmation dialog before cancelling."""
        reply = QMessageBox.question(
            self,
            'Cancel Booking',
            'Are you sure you want to cancel this booking?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.cancel_clicked.emit(self.booking['id'])


class MyBookingsView(QWidget):
    """
    View for displaying user's bookings.
    No IDs visible, clean card layout.
    No unnecessary borders.
    """

    cancel_booking = pyqtSignal(int)  # Emits booking_id to cancel

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bookings = []
        self.init_ui()

    def init_ui(self):
        """Build the bookings view with header and scrollable cards."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(20)

        # Header
        header = QLabel("My Bookings")
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        subtitle = QLabel("View and manage your reservations")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Scroll area for booking cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.bookings_container = QWidget()
        self.bookings_layout = QVBoxLayout(self.bookings_container)
        self.bookings_layout.setContentsMargins(0, 0, 0, 0)
        self.bookings_layout.setSpacing(12)
        self.bookings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.bookings_container)
        layout.addWidget(scroll)

    def set_bookings(self, bookings: list):
        """Set bookings to display."""
        self.bookings = bookings
        self.refresh_bookings()

    def refresh_bookings(self):
        """Refresh the booking cards display."""
        # Clear existing cards
        while self.bookings_layout.count():
            item = self.bookings_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.bookings:
            # Show empty state
            empty_label = QLabel("No bookings yet. Browse rooms to make a reservation!")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 15px; padding: 50px;")
            self.bookings_layout.addWidget(empty_label)
            return

        # Add booking cards
        for booking in self.bookings:
            card = BookingCard(booking)
            card.cancel_clicked.connect(self.cancel_booking.emit)
            self.bookings_layout.addWidget(card)

        self.bookings_layout.addStretch()
