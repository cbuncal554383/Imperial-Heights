"""
Admin Guests View for Imperial Heights Hotel Management System
Features guest table with search functionality
No visible IDs, clean styling, no unnecessary borders
FIXED: Action buttons (View Bookings) are now properly visible
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, get_icon


class AdminGuestsView(QWidget):
    """
    Admin view for managing guests.
    Searchable guest list with view bookings action.
    No ID column visible - IDs used internally only.
    FIXED: View Bookings button now renders correctly.
    """

    view_guest_bookings = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.guests = []
        self.filtered_guests = []
        self.init_ui()

    def init_ui(self):
        """Build guests management view."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(20)

        # Header with search
        header_layout = QHBoxLayout()

        title = QLabel("Guests Management")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Search input with icon
        search_layout = QHBoxLayout()
        search_icon = QLabel()
        search_icon.setPixmap(get_icon('search', COLORS['text_muted']).pixmap(14, 14))
        search_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search guests...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 0px 14px;
                font-size: 13px;
                min-width: 240px;
                min-height: 38px;
                max-height: 38px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
            }}
        """)
        self.search_input.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(self.search_input)
        header_layout.addLayout(search_layout)

        layout.addLayout(header_layout)

        subtitle = QLabel("View and manage hotel guests")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Guests table - no ID column visible
        self.guests_table = QTableWidget()
        self.guests_table.setColumnCount(5)
        self.guests_table.setHorizontalHeaderLabels([
            "Name", "Email", "Phone", "Total Bookings", "Actions"
        ])
        self.guests_table.setStyleSheet(f"""
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
        self.guests_table.horizontalHeader().setStretchLastSection(True)
        self.guests_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.guests_table.setAlternatingRowColors(True)
        self.guests_table.verticalHeader().setVisible(False)
        self.guests_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.guests_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.guests_table.verticalHeader().setDefaultSectionSize(48)

        layout.addWidget(self.guests_table)

    def set_guests(self, guests):
        """Set guests to display."""
        self.guests = guests
        self.filtered_guests = guests
        self.refresh_table()

    def on_search_changed(self, search_text):
        """Filter guests by search text."""
        search_text = search_text.lower()
        if not search_text:
            self.filtered_guests = self.guests
        else:
            self.filtered_guests = [
                g for g in self.guests
                if (search_text in g.get('first_name', '').lower() or
                    search_text in g.get('last_name', '').lower() or
                    search_text in g.get('email', '').lower() or
                    search_text in g.get('phone', '').lower())
            ]
        self.refresh_table()

    def refresh_table(self):
        """
        Refresh guests table with visible action buttons.
        FIXED: View Bookings button now has explicit minimum width.
        """
        self.guests_table.setRowCount(len(self.filtered_guests))

        for row, guest in enumerate(self.filtered_guests):
            # Name - combine first and last name
            first_name = guest.get('first_name', '')
            last_name = guest.get('last_name', '')
            name = f"{first_name} {last_name}".strip()
            self.guests_table.setItem(row, 0, QTableWidgetItem(name))

            # Email
            self.guests_table.setItem(row, 1, QTableWidgetItem(guest.get('email', '')))

            # Phone
            self.guests_table.setItem(row, 2, QTableWidgetItem(guest.get('phone', '')))

            # Total bookings
            self.guests_table.setItem(row, 3, QTableWidgetItem(str(guest.get('total_bookings', 0))))

            # Actions - View Bookings button with explicit sizing
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            view_btn = QPushButton("View")
            view_btn.setMinimumWidth(60)
            view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            view_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_gold']};
                    color: {COLORS['text_primary']};
                    border: none;
                    border-radius: 5px;
                    padding: 4px 10px;
                    font-size: 10px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['accent_gold_hover']};
                }}
            """)
            user_id = guest.get('id')
            view_btn.clicked.connect(lambda checked, uid=user_id:
                self.view_guest_bookings.emit(uid))
            actions_layout.addWidget(view_btn)

            self.guests_table.setCellWidget(row, 4, actions_widget)
