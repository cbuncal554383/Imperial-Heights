"""
Admin Rooms View for Imperial Heights Hotel Management System
Features room table with status management and add room dialog
No visible IDs, high contrast action buttons, no unnecessary borders
Action buttons are now properly sized and visible
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog,
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit,
    QMessageBox, QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from views.styles import COLORS, peso_format, get_icon


class AddRoomDialog(QDialog):
    """
    Dialog for adding a new room to the hotel.
    Form with all room details including price in PHP.
    No unnecessary borders, clean layout with reduced field heights.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Room")
        self.setFixedSize(460, 520)
        self.init_ui()

    def init_ui(self):
        """Build add room form dialog."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(10)

        title = QLabel("Add New Room")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(12)

        # Room Number
        self.add_field(layout, "Room Number", "number_input", required=True)

        # Room Type dropdown
        type_label = QLabel("Room Type")
        type_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Single", "Double", "Suite"])
        self.type_combo.setStyleSheet(self.get_combo_style())
        layout.addWidget(self.type_combo)

        # Price per night in PHP - compact row
        price_row = QHBoxLayout()
        price_label = QLabel("Price/Night (P)")
        price_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        price_row.addWidget(price_label)

        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(500, 50000)
        self.price_spin.setValue(2000)
        self.price_spin.setPrefix("P")
        self.price_spin.setStyleSheet(self.get_spin_style())
        price_row.addWidget(self.price_spin)
        layout.addLayout(price_row)

        # Capacity - compact row
        cap_row = QHBoxLayout()
        capacity_label = QLabel("Capacity")
        capacity_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        cap_row.addWidget(capacity_label)

        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(1, 10)
        self.capacity_spin.setValue(2)
        self.capacity_spin.setStyleSheet(self.get_spin_style())
        cap_row.addWidget(self.capacity_spin)
        layout.addLayout(cap_row)

        # Description
        desc_label = QLabel("Description")
        desc_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        layout.addWidget(desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(60)
        self.desc_input.setStyleSheet(self.get_textedit_style())
        layout.addWidget(self.desc_input)

        # Amenities
        amenities_label = QLabel("Amenities (comma-separated)")
        amenities_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        layout.addWidget(amenities_label)

        self.amenities_input = QLineEdit()
        self.amenities_input.setPlaceholderText("WiFi, TV, AC, Coffee...")
        self.amenities_input.setStyleSheet(self.get_input_style())
        layout.addWidget(self.amenities_input)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        add_btn = QPushButton("  Add Room")
        add_btn.setIcon(get_icon('plus', COLORS['text_primary']))
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_gold']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold_hover']};
            }}
        """)
        add_btn.clicked.connect(self.accept)
        btn_layout.addWidget(add_btn)

        layout.addLayout(btn_layout)

    def add_field(self, layout, label_text, attr_name, required=False):
        """Helper to add labeled input field."""
        label = QLabel(f"{label_text} {'*' if required else ''}")
        label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        layout.addWidget(label)

        field = QLineEdit()
        field.setStyleSheet(self.get_input_style())
        setattr(self, attr_name, field)
        layout.addWidget(field)

    def get_input_style(self):
        """Standard input field styling - no border by default."""
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 0px 12px;
                font-size: 13px;
                min-height: 38px;
                max-height: 38px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_gold']};
            }}
        """

    def get_combo_style(self):
        """Combo box styling - no border."""
        return f"""
            QComboBox {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px;
                font-size: 13px;
                min-height: 38px;
            }}
        """

    def get_spin_style(self):
        """Spin box styling - no border."""
        return f"""
            QDoubleSpinBox, QSpinBox {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px;
                font-size: 13px;
                min-height: 36px;
            }}
        """

    def get_textedit_style(self):
        """Text edit styling - no border."""
        return f"""
            QTextEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px;
                font-size: 13px;
            }}
        """

    def get_room_data(self):
        """Get room data from dialog fields."""
        return {
            'room_number': self.number_input.text().strip(),
            'room_type': self.type_combo.currentText(),
            'price_per_night': self.price_spin.value(),
            'capacity': self.capacity_spin.value(),
            'description': self.desc_input.toPlainText().strip(),
            'amenities': self.amenities_input.text().strip()
        }


class AdminRoomsView(QWidget):
    """
    Admin view for managing rooms.
    Displays room table without IDs, with visible action buttons.
    No unnecessary borders, clean modern layout.
    FIXED: Action buttons are now properly sized and always visible.
    """

    add_room = pyqtSignal(dict)
    update_room_status = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rooms = []
        self.init_ui()

    def init_ui(self):
        """Build rooms management view with table."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.setSpacing(20)

        # Header with title and add button
        header_layout = QHBoxLayout()

        title = QLabel("Rooms Management")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        add_btn = QPushButton("  Add Room")
        add_btn.setIcon(get_icon('plus', COLORS['text_primary']))
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_gold']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold_hover']};
            }}
        """)
        add_btn.clicked.connect(self.on_add_room_clicked)
        header_layout.addWidget(add_btn)

        layout.addLayout(header_layout)

        subtitle = QLabel("Manage hotel rooms and their availability")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Rooms table - no ID column visible
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(6)
        self.rooms_table.setHorizontalHeaderLabels([
            "Room", "Type", "Price/Night", "Capacity", "Status", "Actions"
        ])
        self.rooms_table.setStyleSheet(f"""
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
        self.rooms_table.horizontalHeader().setStretchLastSection(True)
        self.rooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.rooms_table.setAlternatingRowColors(True)
        self.rooms_table.verticalHeader().setVisible(False)
        self.rooms_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.rooms_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Set row height for consistent button visibility
        self.rooms_table.verticalHeader().setDefaultSectionSize(48)

        layout.addWidget(self.rooms_table)

    def set_rooms(self, rooms):
        """Set rooms to display."""
        self.rooms = rooms
        self.refresh_table()

    def refresh_table(self):
        """
        Refresh rooms table with visible action buttons.
        Each row has buttons to change room status.
        No ID column - IDs are used internally only.
        FIXED: Buttons now have proper minimum width and are always visible.
        """
        self.rooms_table.setRowCount(len(self.rooms))

        for row, room in enumerate(self.rooms):
            self.rooms_table.setItem(row, 0, QTableWidgetItem(room.room_number))
            self.rooms_table.setItem(row, 1, QTableWidgetItem(room.room_type))
            self.rooms_table.setItem(row, 2, QTableWidgetItem(peso_format(room.price_per_night)))
            self.rooms_table.setItem(row, 3, QTableWidgetItem(str(room.capacity)))

            # Status with color pill background
            status_colors = {
                'Available': COLORS['status_available'],
                'Occupied': COLORS['status_occupied'],
                'Maintenance': COLORS['status_maintenance']
            }
            status_color = status_colors.get(room.status, COLORS['text_secondary'])

            status_label = QLabel(f"  {room.status}  ")
            status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            status_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {status_color};
                    color: white;
                    border-radius: 8px;
                    padding: 2px 8px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """)
            self.rooms_table.setCellWidget(row, 4, status_label)

            # Actions widget - FIXED: Buttons now have explicit minimum widths
            # and no addStretch() that could collapse them
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            if room.status != 'Available':
                available_btn = QPushButton("Avail")
                available_btn.setMinimumWidth(50)
                available_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                available_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['status_available']};
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 4px 8px;
                        font-size: 10px;
                        font-weight: 600;
                    }}
                    QPushButton:hover {{
                        background-color: #1E8449;
                    }}
                """)
                available_btn.clicked.connect(lambda checked, rid=room.id:
                    self.update_room_status.emit(rid, 'Available'))
                actions_layout.addWidget(available_btn)

            if room.status != 'Maintenance':
                maint_btn = QPushButton("Maint")
                maint_btn.setMinimumWidth(50)
                maint_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                maint_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['status_maintenance']};
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 4px 8px;
                        font-size: 10px;
                        font-weight: 600;
                    }}
                    QPushButton:hover {{
                        background-color: #D35400;
                    }}
                """)
                maint_btn.clicked.connect(lambda checked, rid=room.id:
                    self.update_room_status.emit(rid, 'Maintenance'))
                actions_layout.addWidget(maint_btn)

            if room.status == 'Available':
                # Add a spacer label for available rooms (no action needed)
                spacer = QLabel("-")
                spacer.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
                actions_layout.addWidget(spacer)

            self.rooms_table.setCellWidget(row, 5, actions_widget)

    def on_add_room_clicked(self):
        """Show add room dialog."""
        dialog = AddRoomDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            room_data = dialog.get_room_data()
            if room_data['room_number']:
                self.add_room.emit(room_data)
            else:
                QMessageBox.warning(self, "Missing Information", "Please enter a room number.")
