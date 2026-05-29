"""
Room Browse View for Imperial Heights Hotel Management System
Customer view for browsing and booking rooms
Features Philippine Peso pricing, clean styling with FontAwesome icons
No unnecessary borders, proper alignment
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QGridLayout, QDialog,
    QLineEdit, QDateEdit, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from views.styles import COLORS, peso_format, get_icon


class RoomCard(QFrame):
    """
    Card widget displaying room information.
    Clean styling with no unnecessary borders.
    Shows room image area, info, and book button with icons.
    """

    book_clicked = pyqtSignal(int)  # Emits room_id when book button clicked

    def __init__(self, room, parent=None):
        super().__init__(parent)
        self.room = room
        self.init_ui()

    def init_ui(self):
        """Build room card with image area, info, and book button."""
        self.setFixedWidth(320)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        # Image area with room type badge
        image_frame = QFrame()
        image_frame.setFixedHeight(160)
        image_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_light']};
                border-radius: 14px;
            }}
        """)

        image_layout = QVBoxLayout(image_frame)
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Room type badge (top right)
        badge = QLabel(self.room.room_type)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border-radius: 10px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        image_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        image_layout.addStretch()

        # Hotel icon (centered)
        hotel_icon = QLabel()
        hotel_icon.setPixmap(get_icon('bed', COLORS['accent_gold']).pixmap(32, 32))
        hotel_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(hotel_icon)
        image_layout.addStretch()

        layout.addWidget(image_frame)

        # Room info section
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(16, 16, 16, 0)
        info_layout.setSpacing(8)

        # Room number and price row
        header_layout = QHBoxLayout()

        room_number = QLabel(f"Room {self.room.room_number}")
        room_number.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(room_number)

        header_layout.addStretch()

        # Price in Philippine Peso
        price = QLabel(peso_format(self.room.price_per_night))
        price.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(price)

        per_night = QLabel("/night")
        per_night.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        header_layout.addWidget(per_night)

        info_layout.addLayout(header_layout)

        # Capacity with person icon
        capacity_layout = QHBoxLayout()
        capacity_layout.setSpacing(4)
        cap_icon = QLabel()
        cap_icon.setPixmap(get_icon('user', COLORS['text_muted']).pixmap(12, 12))
        capacity_layout.addWidget(cap_icon)
        capacity = QLabel(f"Up to {self.room.capacity} guest{'s' if self.room.capacity > 1 else ''}")
        capacity.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        capacity_layout.addWidget(capacity)
        capacity_layout.addStretch()
        info_layout.addLayout(capacity_layout)

        # Description
        description = QLabel(self.room.description)
        description.setWordWrap(True)
        description.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; line-height: 1.4;")
        info_layout.addWidget(description)

        # Amenities with icons
        amenities_layout = QHBoxLayout()
        amenities_layout.setSpacing(8)
        amenity_list = [a.strip() for a in self.room.amenities.split(',')]
        for am in amenity_list[:4]:  # Show max 4 amenities
            am_icon = self.get_amenity_icon(am)
            if am_icon:
                amenities_layout.addWidget(am_icon)
        amenities_layout.addStretch()
        info_layout.addLayout(amenities_layout)

        layout.addLayout(info_layout)
        layout.addSpacing(16)

        # Book button - visible and prominent with calendar icon
        book_btn = QPushButton("  Book Now")
        book_btn.setIcon(get_icon('calendar', COLORS['text_light']))
        book_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        book_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary_dark']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: bold;
                margin-left: 16px;
                margin-right: 16px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """)
        book_btn.clicked.connect(lambda: self.book_clicked.emit(self.room.id))
        layout.addWidget(book_btn)

    def get_amenity_icon(self, amenity):
        """Get a small icon label for a given amenity name."""
        icon_map = {
            'WiFi': 'wifi',
            'TV': 'tv',
            'AC': 'ac',
            'Coffee': 'coffee',
        }
        icon_name = icon_map.get(amenity)
        if icon_name:
            icon = QLabel()
            icon.setPixmap(get_icon(icon_name, COLORS['text_muted']).pixmap(14, 14))
            icon.setToolTip(amenity)
            return icon
        return None


class BookingDialog(QDialog):
    """
    Dialog for booking a room.
    Includes date pickers and guest info fields.
    No unnecessary borders, proper spacing with reduced field heights.
    """

    def __init__(self, room, user_id, parent=None):
        super().__init__(parent)
        self.room = room
        self.user_id = user_id
        self.setWindowTitle(f"Book Room {room.room_number}")
        self.setFixedSize(440, 520)
        self.init_ui()

    def init_ui(self):
        """Build the booking dialog form with proper spacing."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(10)

        # Title
        title = QLabel(f"Book Room {self.room.room_number}")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # Price info
        subtitle = QLabel(f"{peso_format(self.room.price_per_night)} per night  |  Up to {self.room.capacity} guests")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Guest Name
        self.add_field(layout, "Guest Name", "full_name", required=True)

        # Email
        self.add_field(layout, "Email", "email", required=False)

        # Phone
        self.add_field(layout, "Phone", "phone", required=False)

        # Number of guests - compact row
        guests_row = QHBoxLayout()
        guests_label = QLabel("Guests")
        guests_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        guests_row.addWidget(guests_label)

        self.guests_spin = QSpinBox()
        self.guests_spin.setRange(1, self.room.capacity)
        self.guests_spin.setValue(1)
        self.guests_spin.setStyleSheet(self.get_spin_style())
        guests_row.addWidget(self.guests_spin)
        guests_row.addStretch()
        layout.addLayout(guests_row)

        # Check-in date - compact row
        checkin_row = QHBoxLayout()
        checkin_label = QLabel("Check-in")
        checkin_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        checkin_row.addWidget(checkin_label)

        self.checkin_date = QDateEdit()
        self.checkin_date.setCalendarPopup(True)
        self.checkin_date.setDate(QDate.currentDate().addDays(1))
        self.checkin_date.setMinimumDate(QDate.currentDate())
        self.checkin_date.setStyleSheet(self.get_date_style())
        checkin_row.addWidget(self.checkin_date)
        layout.addLayout(checkin_row)

        # Check-out date - compact row
        checkout_row = QHBoxLayout()
        checkout_label = QLabel("Check-out")
        checkout_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        checkout_row.addWidget(checkout_label)

        self.checkout_date = QDateEdit()
        self.checkout_date.setCalendarPopup(True)
        self.checkout_date.setDate(QDate.currentDate().addDays(3))
        self.checkout_date.setMinimumDate(QDate.currentDate().addDays(2))
        self.checkout_date.setStyleSheet(self.get_date_style())
        checkout_row.addWidget(self.checkout_date)
        layout.addLayout(checkout_row)

        layout.addStretch()

        # Buttons row
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        confirm_btn = QPushButton("  Confirm Booking")
        confirm_btn.setIcon(get_icon('check', COLORS['text_primary']))
        confirm_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_gold']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold_hover']};
            }}
        """)
        confirm_btn.clicked.connect(self.accept)
        btn_layout.addWidget(confirm_btn)

        layout.addLayout(btn_layout)

    def add_field(self, layout, label, attr_name, required=False):
        """Helper to add a compact labeled input field."""
        label_widget = QLabel(f"{label} {'*' if required else ''}")
        label_widget.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        layout.addWidget(label_widget)

        input_field = QLineEdit()
        input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 0px 12px;
                font-size: 13px;
                color: {COLORS['text_primary']};
                min-height: 38px;
                max-height: 38px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
            }}
        """)
        setattr(self, f"{attr_name}_input", input_field)
        layout.addWidget(input_field)

    def get_spin_style(self):
        """Compact style for spin box."""
        return f"""
            QSpinBox {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px;
                font-size: 13px;
                min-height: 36px;
            }}
        """

    def get_date_style(self):
        """Compact style for date edit."""
        return f"""
            QDateEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
                min-height: 36px;
            }}
            QDateEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
            }}
        """

    def get_booking_data(self):
        """Get the booking data from dialog fields."""
        return {
            'guest_name': getattr(self, 'full_name_input', QLineEdit()).text().strip(),
            'guest_email': getattr(self, 'email_input', QLineEdit()).text().strip(),
            'guest_phone': getattr(self, 'phone_input', QLineEdit()).text().strip(),
            'num_guests': self.guests_spin.value(),
            'check_in': self.checkin_date.date().toString('yyyy-MM-dd'),
            'check_out': self.checkout_date.date().toString('yyyy-MM-dd')
        }


class RoomBrowseView(QWidget):
    """
    View for browsing and booking rooms.
    Features hero section, filters, and room cards grid.
    No borders, clean layout with proper alignment.
    """

    book_room = pyqtSignal(int, dict)  # room_id, booking_data

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rooms = []
        self.user_id = None
        self.current_filter = "All"
        self.init_ui()

    def init_ui(self):
        """Build the room browse view."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(20)

        # Hero section with filters
        hero = self.create_hero_section()
        layout.addWidget(hero)

        # Scroll area for room cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.rooms_container = QWidget()
        self.rooms_layout = QGridLayout(self.rooms_container)
        self.rooms_layout.setContentsMargins(0, 0, 0, 0)
        self.rooms_layout.setSpacing(20)
        self.rooms_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.rooms_container)
        layout.addWidget(scroll)

    def create_hero_section(self):
        """Create the dark hero section with filter buttons."""
        hero = QFrame()
        hero.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_dark']};
                border-radius: 16px;
            }}
        """)
        hero.setFixedHeight(170)

        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(32, 24, 32, 24)
        hero_layout.setSpacing(10)

        hero_title = QLabel("Find Your Perfect Room")
        hero_title.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 28px; font-weight: bold;")
        hero_layout.addWidget(hero_title)

        hero_subtitle = QLabel("Choose from our selection of comfortable and luxurious rooms")
        hero_subtitle.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        hero_layout.addWidget(hero_subtitle)

        hero_layout.addSpacing(16)

        # Filter buttons
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        self.filter_buttons = {}
        filters = ["All Rooms", "Single Rooms", "Double Rooms", "Suites"]

        for filter_name in filters:
            btn = QPushButton(filter_name)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty('filter', filter_name.replace(' Rooms', '').replace('All', 'All'))
            btn.clicked.connect(self.on_filter_clicked)
            filter_layout.addWidget(btn)
            self.filter_buttons[filter_name] = btn

        filter_layout.addStretch()
        hero_layout.addLayout(filter_layout)

        self.update_filter_styles()
        return hero

    def update_filter_styles(self):
        """Update filter button styles based on active filter."""
        for name, btn in self.filter_buttons.items():
            filter_value = btn.property('filter')
            if filter_value == self.current_filter:
                # Active filter - gold background
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['accent_gold']};
                        color: {COLORS['text_primary']};
                        border: none;
                        border-radius: 20px;
                        padding: 8px 22px;
                        font-size: 13px;
                        font-weight: 500;
                    }}
                """)
            else:
                # Inactive filter - transparent with border
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {COLORS['text_light']};
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        border-radius: 20px;
                        padding: 8px 22px;
                        font-size: 13px;
                        font-weight: 500;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(255, 255, 255, 0.1);
                        border-color: rgba(255, 255, 255, 0.5);
                    }}
                """)

    def on_filter_clicked(self):
        """Handle filter button click."""
        sender = self.sender()
        self.current_filter = sender.property('filter')
        self.update_filter_styles()
        self.refresh_rooms()

    def set_rooms(self, rooms):
        """Set rooms to display."""
        self.rooms = rooms
        self.refresh_rooms()

    def set_user_id(self, user_id):
        """Set current user ID for booking."""
        self.user_id = user_id

    def refresh_rooms(self):
        """Refresh the room cards display."""
        # Clear existing cards
        while self.rooms_layout.count():
            item = self.rooms_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Filter rooms based on current filter
        if self.current_filter == "All":
            filtered_rooms = self.rooms
        else:
            filtered_rooms = [r for r in self.rooms if r.room_type == self.current_filter]

        # Add room cards in grid (3 per row)
        row, col = 0, 0
        for room in filtered_rooms:
            card = RoomCard(room)
            card.book_clicked.connect(self.on_book_clicked)
            self.rooms_layout.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def on_book_clicked(self, room_id):
        """Handle book button click - show booking dialog."""
        room = next((r for r in self.rooms if r.id == room_id), None)
        if room and self.user_id:
            dialog = BookingDialog(room, self.user_id, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                booking_data = dialog.get_booking_data()
                if booking_data['guest_name']:
                    self.book_room.emit(room_id, booking_data)
                else:
                    QMessageBox.warning(self, "Missing Information", "Please enter guest name.")
