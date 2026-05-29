"""
Profile View for Imperial Heights Hotel Management System
Customer view for viewing and editing profile information
Includes password change with visibility toggle on all password fields
No unnecessary borders, proper textbox height for 1920x1080
Fixed label alignment and button visibility issues
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, get_icon


class PasswordInput(QWidget):
    """
    Password input field with show/hide toggle button.
    Used on all password fields throughout the application.
    Height optimized for 1920x1080 displays - 38px.
    """

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.init_ui(placeholder)

    def init_ui(self, placeholder):
        """Build password input with toggle."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Password input - hidden by default
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder)
        self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px 0px 0px 8px;
                padding: 0px 14px;
                font-size: 13px;
                color: {COLORS['text_primary']};
                min-height: 38px;
                max-height: 38px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
                background-color: {COLORS['bg_card']};
            }}
        """)
        layout.addWidget(self.input_field, 1)

        # Toggle visibility button
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setFixedWidth(48)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_secondary']};
                border: none;
                border-left: 1px solid {COLORS['border_light']};
                border-radius: 0px 8px 8px 0px;
                padding: 0px 6px;
                font-size: 10px;
                font-weight: 500;
                min-height: 38px;
                max-height: 38px;
            }}
            QPushButton:hover {{
                color: {COLORS['accent_gold_dark']};
            }}
        """)
        self.toggle_btn.clicked.connect(self.toggle_visibility)
        layout.addWidget(self.toggle_btn)

    def toggle_visibility(self):
        """Toggle password between hidden and shown."""
        if self.input_field.echoMode() == QLineEdit.EchoMode.Password:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")
        else:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")

    def text(self):
        """Get password text."""
        return self.input_field.text()

    def clear(self):
        """Clear password field."""
        self.input_field.clear()


class ProfileView(QWidget):
    """
    View for user profile management.
    Allows editing personal info and changing password.
    Password fields all have visibility toggle.
    No unnecessary borders, clean layout.
    Fixed textbox heights and button visibility.
    """

    update_profile = pyqtSignal(dict)           # Profile data to update
    change_password = pyqtSignal(str, str)      # old_password, new_password

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None
        self.init_ui()

    def init_ui(self):
        """Build profile view with personal info and password cards."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(20)

        # Header
        header = QLabel("My Profile")
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        subtitle = QLabel("Manage your account information")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(16)

        # Personal Information Card
        profile_card = self.create_profile_card()
        layout.addWidget(profile_card)

        layout.addSpacing(16)

        # Change Password Card
        password_card = self.create_password_card()
        layout.addWidget(password_card)

        layout.addStretch()

    def create_profile_card(self):
        """Create personal information editing card with proper spacing."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 14px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(14)

        # Section header with user icon
        section_header = QHBoxLayout()
        user_icon = QLabel()
        user_icon.setPixmap(get_icon('user', COLORS['accent_gold_dark']).pixmap(18, 18))
        section_header.addWidget(user_icon)
        section_title = QLabel("Personal Information")
        section_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        section_header.addWidget(section_title)
        section_header.addStretch()
        card_layout.addLayout(section_header)

        card_layout.addSpacing(8)

        # Name row (first + last side by side)
        name_layout = QHBoxLayout()
        name_layout.setSpacing(14)

        # First name
        firstname_layout = QVBoxLayout()
        firstname_layout.setSpacing(4)
        firstname_label = QLabel("First Name")
        firstname_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        firstname_layout.addWidget(firstname_label)

        self.firstname_input = QLineEdit()
        self.firstname_input.setStyleSheet(self.get_input_style())
        firstname_layout.addWidget(self.firstname_input)
        name_layout.addLayout(firstname_layout, 1)

        # Last name
        lastname_layout = QVBoxLayout()
        lastname_layout.setSpacing(4)
        lastname_label = QLabel("Last Name")
        lastname_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        lastname_layout.addWidget(lastname_label)

        self.lastname_input = QLineEdit()
        self.lastname_input.setStyleSheet(self.get_input_style())
        lastname_layout.addWidget(self.lastname_input)
        name_layout.addLayout(lastname_layout, 1)

        card_layout.addLayout(name_layout)

        # Email (disabled - cannot change)
        email_label = QLabel("Email Address")
        email_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setEnabled(False)  # Email cannot be changed
        card_layout.addWidget(self.email_input)

        # Phone
        phone_label = QLabel("Phone Number")
        phone_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(phone_label)

        self.phone_input = QLineEdit()
        self.phone_input.setStyleSheet(self.get_input_style())
        card_layout.addWidget(self.phone_input)

        card_layout.addSpacing(6)

        # Save button - visible and prominent with icon
        save_btn = QPushButton("  Save Changes")
        save_btn.setIcon(get_icon('save', COLORS['text_primary']))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_gold']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 10px;
                padding: 10px 22px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold_hover']};
            }}
        """)
        save_btn.setFixedHeight(42)
        save_btn.clicked.connect(self.on_save_clicked)
        card_layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        return card

    def create_password_card(self):
        """Create password change card with toggle visibility on all fields."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border-radius: 14px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(12)

        # Section header with lock icon
        section_header = QHBoxLayout()
        lock_icon = QLabel()
        lock_icon.setPixmap(get_icon('lock', COLORS['accent_gold_dark']).pixmap(18, 18))
        section_header.addWidget(lock_icon)
        password_title = QLabel("Change Password")
        password_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        section_header.addWidget(password_title)
        section_header.addStretch()
        card_layout.addLayout(section_header)

        card_layout.addSpacing(6)

        # Current password (with toggle)
        current_label = QLabel("Current Password")
        current_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(current_label)

        self.current_password = PasswordInput("Enter current password")
        card_layout.addWidget(self.current_password)

        # New password (with toggle)
        new_label = QLabel("New Password")
        new_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(new_label)

        self.new_password = PasswordInput("Min. 6 characters")
        card_layout.addWidget(self.new_password)

        # Confirm password (with toggle)
        confirm_label = QLabel("Confirm New Password")
        confirm_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(confirm_label)

        self.confirm_password = PasswordInput("Confirm new password")
        card_layout.addWidget(self.confirm_password)

        card_layout.addSpacing(6)

        # Change password button - visible and prominent with icon
        change_btn = QPushButton("  Change Password")
        change_btn.setIcon(get_icon('lock', COLORS['text_light']))
        change_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        change_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary_dark']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: 10px;
                padding: 10px 22px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """)
        change_btn.setFixedHeight(42)
        change_btn.clicked.connect(self.on_change_password_clicked)
        card_layout.addWidget(change_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        return card

    def get_input_style(self):
        """
        Standard input field styling.
        No border by default, gold border on focus.
        Height optimized for 1920x1080 - 38px to prevent overlap.
        """
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 0px 14px;
                font-size: 13px;
                color: {COLORS['text_primary']};
                min-height: 38px;
                max-height: 38px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
                background-color: {COLORS['bg_card']};
            }}
            QLineEdit:disabled {{
                background-color: {COLORS['bg_hover']};
                color: {COLORS['text_muted']};
            }}
        """

    def set_user(self, user):
        """Populate fields with current user data."""
        self.user = user
        if user:
            self.firstname_input.setText(user.first_name)
            self.lastname_input.setText(user.last_name)
            self.email_input.setText(user.email)
            self.phone_input.setText(user.phone or "")

    def on_save_clicked(self):
        """Handle save profile button click."""
        if not self.user:
            return

        profile_data = {
            'first_name': self.firstname_input.text().strip(),
            'last_name': self.lastname_input.text().strip(),
            'phone': self.phone_input.text().strip()
        }

        if not profile_data['first_name'] or not profile_data['last_name']:
            QMessageBox.warning(self, "Missing Information", "Please enter your first and last name.")
            return

        self.update_profile.emit(profile_data)
        QMessageBox.information(self, "Success", "Profile updated successfully!")

    def on_change_password_clicked(self):
        """Handle change password button click."""
        current = self.current_password.text()
        new = self.new_password.text()
        confirm = self.confirm_password.text()

        if not current or not new or not confirm:
            QMessageBox.warning(self, "Missing Information", "Please fill in all password fields.")
            return

        if new != confirm:
            QMessageBox.warning(self, "Password Mismatch", "New passwords do not match.")
            return

        if len(new) < 6:
            QMessageBox.warning(self, "Weak Password", "New password must be at least 6 characters.")
            return

        self.change_password.emit(current, new)
        self.current_password.clear()
        self.new_password.clear()
        self.confirm_password.clear()
