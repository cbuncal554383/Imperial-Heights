"""
Export Dialog for Imperial Heights Hotel Management System
Allows exporting data to CSV with date range selection
Admin only feature - customers cannot access this
No unnecessary borders, clean modern layout
FIXED: Dialog sizing and field overlap issues
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDateEdit, QFileDialog, QComboBox, QMessageBox
)
from PyQt6.QtCore import QDate
from views.styles import COLORS, get_icon


class ExportDialog(QDialog):
    """
    Dialog for exporting data to CSV.
    Supports date range selection and data type selection.
    Admin only - not accessible by customers.
    FIXED: Proper dialog size, no overlapping fields.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Data")
        self.setFixedSize(420, 400)
        self.export_type = "bookings"
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        """Build export dialog with date range and type selection."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(10)

        # Title
        title = QLabel("Export Data to CSV")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("Select date range and data type to export")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Export type dropdown
        type_label = QLabel("Data Type")
        type_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Bookings", "Rooms", "Guests"])
        self.type_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
                min-height: 38px;
            }}
        """)
        layout.addWidget(self.type_combo)

        layout.addSpacing(6)

        # Start date picker - compact row
        start_row = QHBoxLayout()
        start_label = QLabel("Start Date")
        start_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        start_row.addWidget(start_label)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setStyleSheet(self.get_date_style())
        start_row.addWidget(self.start_date)
        layout.addLayout(start_row)

        # End date picker - compact row
        end_row = QHBoxLayout()
        end_label = QLabel("End Date")
        end_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        end_row.addWidget(end_label)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(self.get_date_style())
        end_row.addWidget(self.end_date)
        layout.addLayout(end_row)

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
                padding: 10px 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        export_btn = QPushButton("  Export CSV")
        export_btn.setIcon(get_icon('download', COLORS['text_primary']))
        export_btn.setStyleSheet(f"""
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
        export_btn.clicked.connect(self.on_export_clicked)
        btn_layout.addWidget(export_btn)

        layout.addLayout(btn_layout)

    def get_date_style(self):
        """Style for date picker - no border, clean look."""
        return f"""
            QDateEdit {{
                background-color: {COLORS['bg_input']};
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
                min-height: 36px;
            }}
        """

    def on_export_clicked(self):
        """Handle export button - show file dialog."""
        data_type = self.type_combo.currentText().lower()
        default_name = f"{data_type}_export.csv"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            default_name,
            "CSV Files (*.csv)"
        )

        if file_path:
            self.file_path = file_path
            self.export_type = data_type
            self.accept()

    def get_export_params(self):
        """Get export parameters from dialog."""
        return {
            'type': self.export_type,
            'file_path': self.file_path,
            'start_date': self.start_date.date().toString('yyyy-MM-dd'),
            'end_date': self.end_date.date().toString('yyyy-MM-dd')
        }
