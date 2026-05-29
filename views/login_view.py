"""
Login View for Imperial Heights Hotel Management System
Features dark blue themed login screen with:
- Password visibility toggle on all password fields
- No unnecessary borders - clean modern look
- Proper alignment optimized for 1920x1080
- FontAwesome icons via qtawesome (bed, email, lock, star, etc.)
- Philippine Peso pricing references
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QStackedWidget, QFrame, QCheckBox, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from views.styles import COLORS, get_icon


class PasswordInput(QWidget):
    """
    Custom password input widget with visibility toggle.
    Features a Show/Hide button to toggle password visibility.
    Used on all password fields throughout the application.
    Height optimized for 1920x1080 displays.
    """

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.init_ui(placeholder)

    def init_ui(self, placeholder):
        """Build the password input with toggle button."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Password input field - uses Password echo mode by default
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder)
        self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_field.setStyleSheet(self.get_input_style())
        layout.addWidget(self.input_field, 1)

        # Toggle visibility button - sits next to the input field
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setFixedWidth(50)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_secondary']};
                border: none;
                border-left: 1px solid {COLORS['border_light']};
                border-radius: 0px 8px 8px 0px;
                padding: 0px 6px;
                font-size: 11px;
                font-weight: 500;
                min-height: 40px;
                max-height: 40px;
            }}
            QPushButton:hover {{
                color: {COLORS['accent_gold_dark']};
                background-color: {COLORS['bg_hover']};
            }}
        """)
        self.toggle_btn.clicked.connect(self.toggle_visibility)
        layout.addWidget(self.toggle_btn)

    def get_input_style(self):
        """
        Style for password input field.
        No right border on the input - it connects seamlessly to the toggle button.
        Height optimized for 1920x1080 displays - 40px for better proportions.
        """
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px 0px 0px 8px;
                padding: 0px 14px;
                font-size: 14px;
                color: {COLORS['text_primary']};
                min-height: 40px;
                max-height: 40px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
                background-color: {COLORS['bg_card']};
            }}
        """

    def toggle_visibility(self):
        """Toggle password visibility between hidden and shown."""
        if self.input_field.echoMode() == QLineEdit.EchoMode.Password:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")
        else:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")

    def text(self):
        """Get the password text."""
        return self.input_field.text()

    def clear(self):
        """Clear the password field."""
        self.input_field.clear()

    def setText(self, text):
        """Set the password text."""
        self.input_field.setText(text)


class LoginView(QWidget):
    """
    Login and Registration view.
    Features dark blue theme with gold accents.
    Two-panel layout: branding on left, forms on right.
    Uses FontAwesome icons throughout.
    """

    # Signals for controller communication
    login_requested = pyqtSignal(str, str)           # email, password
    register_requested = pyqtSignal(str, str, str, str, str, str)  # email, pwd, confirm, first, last, phone
    admin_login_clicked = pyqtSignal()                # Admin shortcut clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loginContainer")
        self.init_ui()

    def init_ui(self):
        """Initialize the login view with two-panel layout."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left panel - branding and info
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)

        # Right panel - login/register form
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)

    # ============================================================================
    # Left Panel - Branding with hotel info and stats
    # ============================================================================

    def create_left_panel(self):
        """Create the left branding panel with hotel info and icons."""
        panel = QWidget()
        panel.setStyleSheet(f"background-color: {COLORS['primary_dark']};")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(80, 80, 80, 80)
        layout.setSpacing(24)

        # Logo section with bed icon
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(16)

        # Hotel icon using FontAwesome bed icon
        logo_frame = QFrame()
        logo_frame.setFixedSize(56, 56)
        logo_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['accent_gold']};
                border-radius: 14px;
            }}
        """)
        logo_inner = QVBoxLayout(logo_frame)
        logo_inner.setContentsMargins(0, 0, 0, 0)
        logo_icon = QLabel()
        logo_icon.setPixmap(get_icon('bed', COLORS['text_light']).pixmap(28, 28))
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_inner.addWidget(logo_icon)
        logo_layout.addWidget(logo_frame)

        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)

        hotel_name = QLabel("Imperial Heights")
        hotel_name.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 26px; font-weight: bold;")
        name_layout.addWidget(hotel_name)

        hotel_tagline = QLabel("Luxury Resort & Spa")
        hotel_tagline.setStyleSheet(f"color: {COLORS['accent_gold']}; font-size: 14px;")
        name_layout.addWidget(hotel_tagline)

        logo_layout.addLayout(name_layout)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)

        # Spacer
        layout.addSpacing(60)

        # Main heading
        title = QLabel("Experience Unparalleled")
        title.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 42px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("Luxury & Comfort")
        subtitle.setStyleSheet(f"color: {COLORS['accent_gold']}; font-size: 42px; font-weight: normal;")
        layout.addWidget(subtitle)

        layout.addSpacing(24)

        # Description
        description = QLabel(
            "Indulge in world-class amenities, exceptional service, and "
            "breathtaking views. Your perfect escape awaits at Imperial Heights."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 15px; line-height: 1.6;")
        layout.addWidget(description)

        layout.addSpacing(48)

        # Stats grid with FontAwesome icons - 2x2 layout
        stats_row1 = QHBoxLayout()
        stats_row1.setSpacing(24)
        stats_row1.addWidget(self.create_stat_card("4.9", "Guest Rating", "star"))
        stats_row1.addWidget(self.create_stat_card("48", "Luxury Suites", "bed"))
        layout.addLayout(stats_row1)

        stats_row2 = QHBoxLayout()
        stats_row2.setSpacing(24)
        stats_row2.addWidget(self.create_stat_card("24/7", "Concierge", "clock"))
        stats_row2.addWidget(self.create_stat_card("15+", "Years Excellence", "shield"))
        layout.addLayout(stats_row2)

        # Push everything up
        layout.addStretch()

        # Admin login link at bottom with arrow icon
        admin_link = QPushButton("Staff & Admin Login")
        admin_link.setCursor(Qt.CursorShape.PointingHandCursor)
        admin_link.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_gold']};
                border: none;
                font-size: 14px;
                text-align: left;
                padding: 0;
            }}
            QPushButton:hover {{
                color: {COLORS['accent_gold_light']};
                text-decoration: underline;
            }}
        """)
        admin_link.clicked.connect(self.admin_login_clicked.emit)
        layout.addWidget(admin_link)

        return panel

    def create_stat_card(self, value, label, icon_name):
        """
        Create a stat display card for the left panel.
        Shows a value and label with high contrast for visibility.
        Uses FontAwesome icons instead of letter placeholders.
        """
        card = QFrame()
        card.setFixedSize(160, 110)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_light']};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        # FontAwesome icon
        icon_label = QLabel()
        icon_label.setPixmap(get_icon(icon_name, COLORS['accent_gold']).pixmap(18, 18))
        layout.addWidget(icon_label)

        # Value - large and bold with high contrast
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 28px; font-weight: bold;")
        layout.addWidget(value_label)

        # Label - muted but readable
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        layout.addWidget(label_widget)

        return card

    # ============================================================================
    # Right Panel - Login/Register Forms
    # ============================================================================

    def create_right_panel(self):
        """Create the right panel with login/register card."""
        panel = QWidget()
        panel.setStyleSheet(f"background-color: {COLORS['bg_main']};")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login card (white rounded box)
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 18px;
            }}
        """)
        card.setFixedWidth(440)
        card.setMinimumHeight(560)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(16)

        # Welcome text
        welcome = QLabel("Welcome Back")
        welcome.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: bold;")
        card_layout.addWidget(welcome)

        subtitle = QLabel("Sign in to access your reservations")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(24)

        # Tab buttons (Sign In / Register)
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(0)

        self.signin_tab = QPushButton("Sign In")
        self.signin_tab.setCheckable(True)
        self.signin_tab.setChecked(True)
        self.signin_tab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.signin_tab.setStyleSheet(self.get_tab_style(True))
        self.signin_tab.clicked.connect(lambda: self.switch_tab(0))
        tab_layout.addWidget(self.signin_tab)

        self.register_tab = QPushButton("Register")
        self.register_tab.setCheckable(True)
        self.register_tab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_tab.setStyleSheet(self.get_tab_style(False))
        self.register_tab.clicked.connect(lambda: self.switch_tab(1))
        tab_layout.addWidget(self.register_tab)

        card_layout.addLayout(tab_layout)
        card_layout.addSpacing(20)

        # Stacked widget for forms - switches between sign in and register
        self.forms_stack = QStackedWidget()
        self.forms_stack.addWidget(self.create_signin_form())
        self.forms_stack.addWidget(self.create_register_form())
        card_layout.addWidget(self.forms_stack, 1)

        layout.addWidget(card)
        return panel

    # ============================================================================
    # Sign In Form
    # ============================================================================

    def create_signin_form(self):
        """Create the sign in form with password toggle and icons."""
        form = QWidget()
        layout = QVBoxLayout(form)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Email field with icon
        email_label = QLabel("Email Address")
        email_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your@email.com")
        self.email_input.setStyleSheet(self.get_input_style())
        layout.addWidget(self.email_input)

        # Password field with toggle
        password_label = QLabel("Password")
        password_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        layout.addWidget(password_label)

        self.password_input = PasswordInput("Enter your password")
        layout.addWidget(self.password_input)

        # Remember me and forgot password row
        options_layout = QHBoxLayout()
        options_layout.setSpacing(0)

        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        options_layout.addWidget(self.remember_checkbox)

        options_layout.addStretch()

        forgot_btn = QPushButton("Forgot password?")
        forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forgot_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_gold_dark']};
                border: none;
                font-size: 12px;
                padding: 0;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        options_layout.addWidget(forgot_btn)
        layout.addLayout(options_layout)

        layout.addSpacing(12)

        # Sign In button - prominent action button
        signin_btn = QPushButton("Sign In to Your Account")
        signin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        signin_btn.setStyleSheet(self.get_primary_button_style())
        signin_btn.setFixedHeight(46)
        signin_btn.clicked.connect(self.on_signin_clicked)
        layout.addWidget(signin_btn)

        # Register link
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        no_account = QLabel("Don't have an account?")
        no_account.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        register_layout.addWidget(no_account)

        register_link = QPushButton("Register now")
        register_link.setCursor(Qt.CursorShape.PointingHandCursor)
        register_link.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_gold_dark']};
                border: none;
                font-size: 13px;
                font-weight: 500;
                padding: 4px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        register_link.clicked.connect(lambda: self.switch_tab(1))
        register_layout.addWidget(register_link)
        layout.addLayout(register_layout)

        layout.addStretch()
        return form

    # ============================================================================
    # Register Form
    # ============================================================================

    def create_register_form(self):
        """Create the registration form with password toggle."""
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Name row (first + last side by side)
        name_row = QHBoxLayout()
        name_row.setSpacing(12)

        # First Name
        firstname_layout = QVBoxLayout()
        firstname_layout.setSpacing(4)
        firstname_label = QLabel("First Name")
        firstname_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        firstname_layout.addWidget(firstname_label)

        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Juan")
        self.firstname_input.setStyleSheet(self.get_input_style())
        firstname_layout.addWidget(self.firstname_input)
        name_row.addLayout(firstname_layout, 1)

        # Last Name
        lastname_layout = QVBoxLayout()
        lastname_layout.setSpacing(4)
        lastname_label = QLabel("Last Name")
        lastname_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        lastname_layout.addWidget(lastname_label)

        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Dela Cruz")
        self.lastname_input.setStyleSheet(self.get_input_style())
        lastname_layout.addWidget(self.lastname_input)
        name_row.addLayout(lastname_layout, 1)

        layout.addLayout(name_row)

        # Email
        email_label = QLabel("Email Address")
        email_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        layout.addWidget(email_label)

        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("your@email.com")
        self.reg_email_input.setStyleSheet(self.get_input_style())
        layout.addWidget(self.reg_email_input)

        # Phone
        phone_label = QLabel("Phone Number")
        phone_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        layout.addWidget(phone_label)

        self.reg_phone_input = QLineEdit()
        self.reg_phone_input.setPlaceholderText("0917-123-4567")
        self.reg_phone_input.setStyleSheet(self.get_input_style())
        layout.addWidget(self.reg_phone_input)

        # Password with toggle
        password_label = QLabel("Password")
        password_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        layout.addWidget(password_label)

        self.reg_password_input = PasswordInput("Min. 6 characters")
        layout.addWidget(self.reg_password_input)

        # Confirm Password with toggle
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500;")
        layout.addWidget(confirm_label)

        self.confirm_password_input = PasswordInput("Confirm your password")
        layout.addWidget(self.confirm_password_input)

        layout.addSpacing(12)

        # Register button
        register_btn = QPushButton("Create Account")
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.setStyleSheet(self.get_primary_button_style())
        register_btn.setFixedHeight(46)
        register_btn.clicked.connect(self.on_register_clicked)
        layout.addWidget(register_btn)

        # Sign in link
        signin_layout = QHBoxLayout()
        signin_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        have_account = QLabel("Already have an account?")
        have_account.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        signin_layout.addWidget(have_account)

        signin_link = QPushButton("Sign in")
        signin_link.setCursor(Qt.CursorShape.PointingHandCursor)
        signin_link.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_gold_dark']};
                border: none;
                font-size: 13px;
                font-weight: 500;
                padding: 4px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        signin_link.clicked.connect(lambda: self.switch_tab(0))
        signin_layout.addWidget(signin_link)
        layout.addLayout(signin_layout)

        layout.addStretch()
        return scroll_widget

    # ============================================================================
    # Styling Helpers - reusable style generators
    # ============================================================================

    def get_input_style(self):
        """
        Style for text input fields.
        No visible border by default, subtle gold border on focus.
        Height optimized for 1920x1080 displays - 40px.
        """
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 0px 14px;
                font-size: 14px;
                color: {COLORS['text_primary']};
                min-height: 40px;
                max-height: 40px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
                background-color: {COLORS['bg_card']};
            }}
        """

    def get_primary_button_style(self):
        """
        Style for primary action buttons.
        Dark background with white text for high contrast.
        """
        return f"""
            QPushButton {{
                background-color: {COLORS['primary_dark']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: 10px;
                padding: 12px 28px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """

    def get_tab_style(self, active):
        """
        Style for tab buttons (Sign In / Register).
        Active tab has gold underline for clear indication.
        """
        if active:
            return f"""
                QPushButton {{
                    background-color: {COLORS['bg_card']};
                    color: {COLORS['text_primary']};
                    border: none;
                    border-bottom: 3px solid {COLORS['accent_gold']};
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 600;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: {COLORS['bg_input']};
                    color: {COLORS['text_secondary']};
                    border: none;
                    border-bottom: 3px solid transparent;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    color: {COLORS['text_primary']};
                    background-color: {COLORS['bg_hover']};
                }}
            """

    # ============================================================================
    # Actions - button click handlers
    # ============================================================================

    def switch_tab(self, index):
        """Switch between sign in and register tabs."""
        self.forms_stack.setCurrentIndex(index)
        if index == 0:
            self.signin_tab.setChecked(True)
            self.signin_tab.setStyleSheet(self.get_tab_style(True))
            self.register_tab.setChecked(False)
            self.register_tab.setStyleSheet(self.get_tab_style(False))
        else:
            self.signin_tab.setChecked(False)
            self.signin_tab.setStyleSheet(self.get_tab_style(False))
            self.register_tab.setChecked(True)
            self.register_tab.setStyleSheet(self.get_tab_style(True))

    def on_signin_clicked(self):
        """Handle sign in button click - emit credentials to controller."""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        self.login_requested.emit(email, password)

    def on_register_clicked(self):
        """Handle register button click - emit data to controller."""
        email = self.reg_email_input.text().strip()
        password = self.reg_password_input.text()
        confirm = self.confirm_password_input.text()
        first_name = self.firstname_input.text().strip()
        last_name = self.lastname_input.text().strip()
        phone = self.reg_phone_input.text().strip()
        self.register_requested.emit(email, password, confirm, first_name, last_name, phone)

    def clear_fields(self):
        """Clear all input fields after login/logout."""
        self.email_input.clear()
        self.password_input.clear()
        self.reg_email_input.clear()
        self.reg_password_input.clear()
        self.confirm_password_input.clear()
        self.firstname_input.clear()
        self.lastname_input.clear()
        self.reg_phone_input.clear()
        self.remember_checkbox.setChecked(False)
