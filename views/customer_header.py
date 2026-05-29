"""
Customer Header for Imperial Heights Hotel Management System
Navigation header for customer views with FontAwesome icons
No unnecessary borders, clean layout with icon+text navigation
Only customers can navigate - no export functionality
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, get_icon


class CustomerHeader(QWidget):
    """
    Header widget for customer views.
    Contains logo, welcome message, and navigation tabs with icons.
    No export button - customers cannot export data (admin only).
    """

    # Signals for navigation actions
    navigate = pyqtSignal(str)        # Page navigation: browse, bookings, profile
    logout = pyqtSignal()             # Logout request
    switch_to_admin = pyqtSignal()    # Switch to admin view (if user is admin)

    def __init__(self, user_name="Guest", is_admin=False, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.is_admin = is_admin
        self.current_page = 'browse'
        self.init_ui()

    def init_ui(self):
        """Build the header with two rows: top bar and navigation."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar with logo and user actions
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # Navigation bar with icon+text tabs
        nav_bar = self.create_nav_bar()
        main_layout.addWidget(nav_bar)

    def create_top_bar(self):
        """Create top bar with logo and user actions."""
        bar = QFrame()
        bar.setStyleSheet(f"background-color: {COLORS['bg_card']};")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(48, 16, 48, 16)
        layout.setSpacing(16)

        # Logo section with hotel icon
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

        # Hotel name and welcome message
        name_layout = QVBoxLayout()
        name_layout.setSpacing(2)

        hotel_name = QLabel("Imperial Heights")
        hotel_name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold;")
        name_layout.addWidget(hotel_name)

        welcome_text = QLabel(f"Welcome, {self.user_name}")
        welcome_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        name_layout.addWidget(welcome_text)

        logo_layout.addLayout(name_layout)
        layout.addLayout(logo_layout)

        layout.addStretch()

        # Admin view button (only if user is admin)
        if self.is_admin:
            admin_btn = QPushButton("Admin View")
            admin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            admin_btn.setStyleSheet(f"""
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
            admin_btn.clicked.connect(self.switch_to_admin.emit)
            layout.addWidget(admin_btn)

        # Logout button with icon
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
        """Create navigation bar with icon+text tabs for customer sections."""
        nav = QFrame()
        nav.setStyleSheet(f"background-color: {COLORS['bg_card']};")

        layout = QHBoxLayout(nav)
        layout.setContentsMargins(48, 0, 48, 0)
        layout.setSpacing(0)

        # Navigation buttons with FontAwesome icons
        self.browse_btn = QPushButton("  Browse Rooms")
        self.browse_btn.setIcon(get_icon('bed', COLORS['text_secondary']))
        self.browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_btn.clicked.connect(lambda: self.on_nav_clicked('browse'))
        layout.addWidget(self.browse_btn)

        self.bookings_btn = QPushButton("  My Bookings")
        self.bookings_btn.setIcon(get_icon('calendar', COLORS['text_secondary']))
        self.bookings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bookings_btn.clicked.connect(lambda: self.on_nav_clicked('bookings'))
        layout.addWidget(self.bookings_btn)

        self.profile_btn = QPushButton("  Profile")
        self.profile_btn.setIcon(get_icon('user', COLORS['text_secondary']))
        self.profile_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_btn.clicked.connect(lambda: self.on_nav_clicked('profile'))
        layout.addWidget(self.profile_btn)

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
        Update navigation button styles based on current page.
        Active tab has gold underline and gold icon for clear visual indication.
        """
        buttons = {
            'browse': (self.browse_btn, 'bed'),
            'bookings': (self.bookings_btn, 'calendar'),
            'profile': (self.profile_btn, 'user')
        }

        for page, (btn, icon_name) in buttons.items():
            if page == self.current_page:
                # Active tab - gold underline and gold icon
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
                # Inactive tab - subtle styling
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
        """Set the current active page."""
        self.current_page = page
        self.update_nav_styles()
