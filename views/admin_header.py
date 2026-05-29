"""
Admin Header for Imperial Heights Hotel Management System
Navigation header for admin views with export button
Features FontAwesome icons, no unnecessary borders, clean layout
Export functionality is admin-only - customers cannot export data
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, get_icon


class AdminHeader(QWidget):
    """
    Header widget for admin views.
    Includes export button for data export functionality (admin only).
    No borders, clean styling with FontAwesome icons.
    """

    # Signals for navigation and actions
    navigate = pyqtSignal(str)            # Page navigation: dashboard, rooms, bookings, guests
    logout = pyqtSignal()                 # Logout request
    switch_to_customer = pyqtSignal()     # Switch to customer view
    export_data = pyqtSignal()            # Export data request (admin only)

    def __init__(self, user_name="Admin", parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.current_page = 'dashboard'
        self.init_ui()

    def init_ui(self):
        """Build header with top bar and navigation tabs."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar with logo, export, and user actions
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # Navigation bar with icons
        nav_bar = self.create_nav_bar()
        main_layout.addWidget(nav_bar)

    def create_top_bar(self):
        """Create top bar with logo, export, and user actions."""
        bar = QFrame()
        bar.setStyleSheet(f"background-color: {COLORS['bg_card']};")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(48, 16, 48, 16)
        layout.setSpacing(16)

        # Logo with hotel icon
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(10)

        logo_frame = QFrame()
        logo_frame.setFixedSize(36, 36)
        logo_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_dark']};
                border-radius: 8px;
            }}
        """)
        logo_inner = QVBoxLayout(logo_frame)
        logo_inner.setContentsMargins(0, 0, 0, 0)
        logo_icon = QLabel()
        logo_icon.setPixmap(get_icon('hotel', COLORS['accent_gold']).pixmap(18, 18))
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_inner.addWidget(logo_icon)
        logo_layout.addWidget(logo_frame)

        name_layout = QVBoxLayout()
        name_layout.setSpacing(2)

        hotel_name = QLabel("Imperial Heights")
        hotel_name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold;")
        name_layout.addWidget(hotel_name)

        system_text = QLabel("Management System")
        system_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        name_layout.addWidget(system_text)

        logo_layout.addLayout(name_layout)
        layout.addLayout(logo_layout)

        layout.addStretch()

        # Export button - admin only, gold accent for visibility
        export_btn = QPushButton("  Export")
        export_btn.setIcon(get_icon('export', COLORS['text_primary']))
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_gold']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold_hover']};
            }}
        """)
        export_btn.clicked.connect(self.export_data.emit)
        layout.addWidget(export_btn)

        # Switch to customer view
        switch_btn = QPushButton("Customer View")
        switch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        switch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_gold_dark']};
                border: none;
                font-size: 12px;
                font-weight: 500;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        switch_btn.clicked.connect(self.switch_to_customer.emit)
        layout.addWidget(switch_btn)

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: none;
                font-size: 12px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                color: {COLORS['text_primary']};
            }}
        """)
        logout_btn.clicked.connect(self.logout.emit)
        layout.addWidget(logout_btn)

        return bar

    def create_nav_bar(self):
        """Create navigation bar with admin tabs and icons."""
        nav = QFrame()
        nav.setStyleSheet(f"background-color: {COLORS['bg_card']};")

        layout = QHBoxLayout(nav)
        layout.setContentsMargins(48, 0, 48, 0)
        layout.setSpacing(0)

        # Navigation buttons with FontAwesome icons
        self.dashboard_btn = QPushButton("  Dashboard")
        self.dashboard_btn.setIcon(get_icon('dashboard', COLORS['text_secondary']))
        self.dashboard_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dashboard_btn.clicked.connect(lambda: self.on_nav_clicked('dashboard'))
        layout.addWidget(self.dashboard_btn)

        self.rooms_btn = QPushButton("  Rooms")
        self.rooms_btn.setIcon(get_icon('rooms', COLORS['text_secondary']))
        self.rooms_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rooms_btn.clicked.connect(lambda: self.on_nav_clicked('rooms'))
        layout.addWidget(self.rooms_btn)

        self.bookings_btn = QPushButton("  Bookings")
        self.bookings_btn.setIcon(get_icon('bookings', COLORS['text_secondary']))
        self.bookings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bookings_btn.clicked.connect(lambda: self.on_nav_clicked('bookings'))
        layout.addWidget(self.bookings_btn)

        self.guests_btn = QPushButton("  Guests")
        self.guests_btn.setIcon(get_icon('guests', COLORS['text_secondary']))
        self.guests_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.guests_btn.clicked.connect(lambda: self.on_nav_clicked('guests'))
        layout.addWidget(self.guests_btn)

        layout.addStretch()
        self.update_nav_styles()
        return nav

    def on_nav_clicked(self, page):
        """Handle navigation button click."""
        self.current_page = page
        self.update_nav_styles()
        self.navigate.emit(page)

    def update_nav_styles(self):
        """
        Update navigation button styles.
        Active tab has gold underline and gold icon for clear visual indication.
        """
        buttons = {
            'dashboard': (self.dashboard_btn, 'dashboard'),
            'rooms': (self.rooms_btn, 'rooms'),
            'bookings': (self.bookings_btn, 'bookings'),
            'guests': (self.guests_btn, 'guests')
        }

        for page, (btn, icon_name) in buttons.items():
            if page == self.current_page:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {COLORS['accent_gold_dark']};
                        border: none;
                        border-bottom: 3px solid {COLORS['accent_gold']};
                        padding: 12px 20px;
                        font-size: 13px;
                        font-weight: 600;
                    }}
                """)
                btn.setIcon(get_icon(icon_name, COLORS['accent_gold_dark']))
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {COLORS['text_secondary']};
                        border: none;
                        border-bottom: 3px solid transparent;
                        padding: 12px 20px;
                        font-size: 13px;
                        font-weight: 500;
                    }}
                    QPushButton:hover {{
                        color: {COLORS['text_primary']};
                    }}
                """)
                btn.setIcon(get_icon(icon_name, COLORS['text_secondary']))

    def set_current_page(self, page):
        """Set current active page."""
        self.current_page = page
        self.update_nav_styles()
