"""
Admin Dashboard View for Imperial Heights Hotel Management System
Features statistics cards, recent activities, and upcoming check-ins
Uses Philippine Peso formatting and high-contrast colors for visibility
No unnecessary borders, clean modern layout with FontAwesome icons
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, peso_format, get_icon


class StatCard(QFrame):
    """
    Statistics card widget with icon, value, label, and sublabel.
    High contrast colors for visibility.
    No borders - clean card design.
    Uses FontAwesome icons.
    """

    def __init__(self, icon_name, value, label, sublabel="", color=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # FontAwesome icon
        icon_color = color if color else COLORS['accent_gold_dark']
        icon_label = QLabel()
        icon_label.setPixmap(get_icon(icon_name, icon_color).pixmap(24, 24))
        layout.addWidget(icon_label)

        # Value - large and bold with high contrast against white background
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 32px; font-weight: bold;")
        layout.addWidget(value_label)

        # Label - secondary text with good contrast
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(label_widget)

        # Sublabel - accent color for visibility
        if sublabel:
            sublabel_widget = QLabel(sublabel)
            sublabel_widget.setStyleSheet(f"color: {icon_color}; font-size: 12px; font-weight: 500;")
            layout.addWidget(sublabel_widget)

        layout.addStretch()


class ActivityItem(QFrame):
    """
    Single activity log entry widget.
    Shows activity type with colored indicator.
    No borders - clean list design.
    """

    def __init__(self, activity, parent=None):
        super().__init__(parent)
        self.activity = activity
        self.init_ui()

    def init_ui(self):
        """Build activity item with type indicator."""
        self.setStyleSheet("QFrame { background-color: transparent; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(14)

        # Activity type indicator (colored dot)
        activity_type = self.activity.activity_type
        type_colors = {
            'checkin': COLORS['status_available'],
            'checkout': COLORS['status_occupied'],
            'booking': COLORS['status_confirmed'],
            'cancel': COLORS['status_pending'],
            'room_add': COLORS['accent_gold_dark']
        }
        type_color = type_colors.get(activity_type, COLORS['text_muted'])

        indicator = QFrame()
        indicator.setFixedSize(8, 8)
        indicator.setStyleSheet(f"""
            QFrame {{
                background-color: {type_color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(indicator)

        # Activity info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        user_name = self.activity.user_name or "Guest"
        name_label = QLabel(user_name)
        name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        info_layout.addWidget(name_label)

        desc_label = QLabel(self.activity.description)
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        info_layout.addWidget(desc_label)

        layout.addLayout(info_layout, 1)

        # Timestamp
        timestamp = self.activity.timestamp
        if timestamp:
            time_label = QLabel(str(timestamp)[11:16] if len(str(timestamp)) > 10 else str(timestamp))
            time_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
            layout.addWidget(time_label)


class CheckinItem(QFrame):
    """
    Single check-in item widget with action button.
    Shows guest info and check-in button.
    No borders - clean list design.
    """

    checkin_clicked = pyqtSignal(int)  # Emits booking_id

    def __init__(self, checkin, parent=None):
        super().__init__(parent)
        self.checkin = checkin
        self.init_ui()

    def init_ui(self):
        """Build check-in item with guest info and check-in button."""
        self.setStyleSheet("QFrame { background-color: transparent; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(14)

        # Guest info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        guest_name = self.checkin.get('guest_name', 'Guest')
        name_label = QLabel(guest_name)
        name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        info_layout.addWidget(name_label)

        room_number = self.checkin.get('room_number', 'N/A')
        room_label = QLabel(f"Room {room_number}")
        room_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        info_layout.addWidget(room_label)

        layout.addLayout(info_layout, 1)

        # Check-in button - visible with accent color and border
        checkin_btn = QPushButton("Check in")
        checkin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        checkin_btn.setFixedWidth(70)
        checkin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_gold_dark']};
                border: 1px solid {COLORS['accent_gold']};
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold']};
                color: {COLORS['text_primary']};
            }}
        """)
        checkin_btn.clicked.connect(lambda: self.checkin_clicked.emit(self.checkin['id']))
        layout.addWidget(checkin_btn)


class AdminDashboardView(QWidget):
    """
    Admin dashboard with statistics, activities, and check-ins.
    High contrast colors for visibility.
    No unnecessary borders, clean modern layout.
    """

    checkin_guest = pyqtSignal(int)  # Emits booking_id for check-in

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats = {}
        self.activities = []
        self.checkins = []
        self.init_ui()

    def init_ui(self):
        """Build dashboard with stats grid and two-column layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(24)

        # Stats grid (4 cards in a row)
        self.stats_layout = QGridLayout()
        self.stats_layout.setSpacing(20)
        layout.addLayout(self.stats_layout)

        # Bottom section - Activities and Check-ins side by side
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Recent Activities card
        activities_card = self.create_section_card("Recent Activities")
        self.activities_list = QVBoxLayout()
        self.activities_list.setContentsMargins(0, 0, 0, 0)
        self.activities_list.setSpacing(0)
        self.activities_list.setAlignment(Qt.AlignmentFlag.AlignTop)

        activities_card.layout().addLayout(self.activities_list)
        activities_card.layout().addStretch()
        bottom_layout.addWidget(activities_card, 1)

        # Upcoming Check-ins card
        checkins_card = self.create_section_card("Today's Check-ins")
        self.checkins_list = QVBoxLayout()
        self.checkins_list.setContentsMargins(0, 0, 0, 0)
        self.checkins_list.setSpacing(0)
        self.checkins_list.setAlignment(Qt.AlignmentFlag.AlignTop)

        checkins_card.layout().addLayout(self.checkins_list)
        checkins_card.layout().addStretch()
        bottom_layout.addWidget(checkins_card, 1)

        layout.addLayout(bottom_layout)
        layout.addStretch()

    def create_section_card(self, title):
        """
        Create a white card with title for sections.
        No borders, rounded corners for modern look.
        """
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 14px;
            }}
        """)
        card.setMinimumWidth(360)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # Section title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold; padding: 16px 20px;")
        card_layout.addWidget(title_label)

        return card

    def set_stats(self, stats):
        """Set and display dashboard statistics."""
        self.stats = stats
        self.refresh_stats()

    def refresh_stats(self):
        """
        Refresh statistics cards with high-contrast values.
        Each card has a unique FontAwesome icon for visual distinction.
        """
        # Clear existing stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Stats with FontAwesome icons and high contrast colors
        stat_cards = [
            ('door-open', str(self.stats.get('total_rooms', 0)), 'Total Rooms',
             f"{self.stats.get('occupied_rooms', 0)} occupied", COLORS['status_confirmed']),
            ('users', str(self.stats.get('total_guests', 0)), 'Guests',
             f"{self.stats.get('checking_out_today', 0)} checking out", COLORS['status_available']),
            ('calendar-alt', str(self.stats.get('total_bookings', 0)), 'Bookings',
             f"{self.stats.get('pending_bookings', 0)} pending", COLORS['status_pending']),
            ('dollar-sign', peso_format(self.stats.get('weekly_revenue', 0)), 'Revenue', 'This week', COLORS['accent_gold_dark']),
        ]

        for i, (icon, value, label, sublabel, color) in enumerate(stat_cards):
            card = StatCard(icon, value, label, sublabel, color)
            self.stats_layout.addWidget(card, 0, i)

    def set_activities(self, activities):
        """Set recent activities."""
        self.activities = activities
        self.refresh_activities()

    def refresh_activities(self):
        """Refresh activities list."""
        # Clear existing activities
        while self.activities_list.count():
            item = self.activities_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.activities:
            empty = QLabel("No recent activities")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 16px;")
            self.activities_list.addWidget(empty)
            return

        for activity in self.activities[:5]:
            item = ActivityItem(activity)
            self.activities_list.addWidget(item)

    def set_checkins(self, checkins):
        """Set upcoming check-ins."""
        self.checkins = checkins
        self.refresh_checkins()

    def refresh_checkins(self):
        """Refresh check-ins list."""
        # Clear existing checkins
        while self.checkins_list.count():
            item = self.checkins_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.checkins:
            empty = QLabel("No check-ins today")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 16px;")
            self.checkins_list.addWidget(empty)
            return

        for checkin in self.checkins:
            item = CheckinItem(checkin)
            item.checkin_clicked.connect(self.checkin_guest.emit)
            self.checkins_list.addWidget(item)
