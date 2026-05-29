"""
Admin Bookings View for Imperial Heights Hotel Management System
Features booking table with status filters and action buttons
No visible IDs, high contrast actions, clean styling
FIXED: Action buttons are now properly sized and always visible
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, peso_format, get_icon


class AdminBookingsView(QWidget):
    """
    Admin view for managing all bookings.
    Filterable by status with visible action buttons.
    No ID column visible - IDs used internally only.
    FIXED: Action buttons now render correctly with proper sizing.
    """

    confirm_booking = pyqtSignal(int)
    checkin_booking = pyqtSignal(int)
    checkout_booking = pyqtSignal(int)
    cancel_booking = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bookings = []
        self.current_filter = "All"
        self.init_ui()

    def init_ui(self):
        """Build bookings management view."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(20)

        # Header with filter dropdown
        header_layout = QHBoxLayout()

        title = QLabel("Bookings Management")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        header_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Pending", "Confirmed", "Checked In", "Checked Out", "Cancelled"])
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
                min-width: 140px;
                min-height: 36px;
            }}
        """)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        header_layout.addWidget(self.filter_combo)

        layout.addLayout(header_layout)

        subtitle = QLabel("View and manage all hotel bookings")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Bookings table - no ID column visible
        self.bookings_table = QTableWidget()
        self.bookings_table.setColumnCount(7)
        self.bookings_table.setHorizontalHeaderLabels([
            "Guest", "Room", "Check-in", "Check-out", "Guests", "Total", "Actions"
        ])
        self.bookings_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_card']};
                border-radius: 12px;
                gridline-color: {COLORS['border_light']};
                border: none;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {COLORS['border_light']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_main']};
                color: {COLORS['text_primary']};
                padding: 12px;
                font-weight: 600;
                font-size: 12px;
                border: none;
            }}
        """)
        self.bookings_table.horizontalHeader().setStretchLastSection(True)
        self.bookings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bookings_table.setAlternatingRowColors(True)
        self.bookings_table.verticalHeader().setVisible(False)
        self.bookings_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bookings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Consistent row height for button visibility
        self.bookings_table.verticalHeader().setDefaultSectionSize(48)

        layout.addWidget(self.bookings_table)

    def set_bookings(self, bookings):
        """Set bookings to display."""
        self.bookings = bookings
        self.refresh_table()

    def on_filter_changed(self, filter_text):
        """Handle status filter change."""
        self.current_filter = filter_text
        self.refresh_table()

    def refresh_table(self):
        """
        Refresh bookings table with visible action buttons.
        Buttons change based on booking status.
        No ID column visible.
        FIXED: Action buttons now have explicit minimum widths for visibility.
        """
        if self.current_filter == "All":
            filtered_bookings = self.bookings
        else:
            filtered_bookings = [b for b in self.bookings if b.status == self.current_filter]

        self.bookings_table.setRowCount(len(filtered_bookings))

        for row, booking in enumerate(filtered_bookings):
            self.bookings_table.setItem(row, 0, QTableWidgetItem(booking.guest_name))

            room = self.get_room_number(booking.room_id)
            self.bookings_table.setItem(row, 1, QTableWidgetItem(room))

            self.bookings_table.setItem(row, 2, QTableWidgetItem(booking.check_in_date))
            self.bookings_table.setItem(row, 3, QTableWidgetItem(booking.check_out_date))
            self.bookings_table.setItem(row, 4, QTableWidgetItem(str(booking.num_guests)))
            self.bookings_table.setItem(row, 5, QTableWidgetItem(peso_format(booking.total_price)))

            # Actions widget - FIXED: Explicit minimum widths, no addStretch
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(3)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            if booking.status == 'Pending':
                confirm_btn = QPushButton("Confirm")
                confirm_btn.setMinimumWidth(58)
                confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                confirm_btn.setStyleSheet(self.get_action_btn_style(COLORS['status_confirmed']))
                confirm_btn.clicked.connect(lambda checked, bid=booking.id:
                    self.confirm_booking.emit(bid))
                actions_layout.addWidget(confirm_btn)

            if booking.status == 'Confirmed':
                checkin_btn = QPushButton("Check In")
                checkin_btn.setMinimumWidth(58)
                checkin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                checkin_btn.setStyleSheet(self.get_action_btn_style(COLORS['status_available']))
                checkin_btn.clicked.connect(lambda checked, bid=booking.id:
                    self.checkin_booking.emit(bid))
                actions_layout.addWidget(checkin_btn)

            if booking.status == 'Checked In':
                checkout_btn = QPushButton("Check Out")
                checkout_btn.setMinimumWidth(62)
                checkout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                checkout_btn.setStyleSheet(self.get_action_btn_style(COLORS['text_secondary']))
                checkout_btn.clicked.connect(lambda checked, bid=booking.id:
                    self.checkout_booking.emit(bid))
                actions_layout.addWidget(checkout_btn)

            if booking.status in ['Pending', 'Confirmed']:
                cancel_btn = QPushButton("Cancel")
                cancel_btn.setMinimumWidth(52)
                cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                cancel_btn.setStyleSheet(self.get_action_btn_style(COLORS['status_occupied']))
                cancel_btn.clicked.connect(lambda checked, bid=booking.id:
                    self.on_cancel_clicked(bid))
                actions_layout.addWidget(cancel_btn)

            if booking.status in ['Checked Out', 'Cancelled']:
                spacer = QLabel("-")
                spacer.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
                actions_layout.addWidget(spacer)

            self.bookings_table.setCellWidget(row, 6, actions_widget)

    def get_room_number(self, room_id):
        """Get room number string from room_id."""
        from models.database import db
        room = db.get_room_by_id(room_id)
        return f"Room {room.room_number}" if room else "Unknown"

    def get_action_btn_style(self, color):
        """
        Generate action button style with given color.
        High contrast white text on colored background.
        Compact sizing to fit multiple buttons in a cell.
        """
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {color};
                opacity: 0.85;
            }}
        """

    def on_cancel_clicked(self, booking_id):
        """Show confirmation before cancelling."""
        reply = QMessageBox.question(
            self,
            'Cancel Booking',
            'Are you sure you want to cancel this booking?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.cancel_booking.emit(booking_id)
