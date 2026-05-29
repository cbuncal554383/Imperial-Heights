"""
Styles and Color Palette for Imperial Heights Hotel Management System
Dark blue and gold theme with high contrast for visibility
All pricing uses Philippine Peso (PHP)

This module defines all visual styling constants used across the application.
Centralizing styles ensures consistency and makes theme updates easy.
Uses qtawesome for professional FontAwesome icons.
"""

import qtawesome as qta
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication

# ============================================================================
# Color Palette - Dark Blue & Gold Theme (High Contrast)
# ============================================================================

COLORS = {
    # Primary Colors (Dark Blue/Slate)
    'primary_dark': '#2C3E50',       # Main header, login bg
    'primary_navy': '#34495E',       # Secondary dark
    'primary_light': '#3D566E',      # Cards on dark bg
    'primary_hover': '#4A6B8A',      # Hover state

    # Accent Colors (Gold/Amber)
    'accent_gold': '#D4A574',        # Primary accent
    'accent_gold_hover': '#C4966A',  # Hover state
    'accent_gold_light': '#E8C9A0',  # Light accent
    'accent_gold_dark': '#B08B5F',   # Dark accent

    # Background Colors
    'bg_main': '#F5F5F0',            # Main background (warm gray)
    'bg_card': '#FFFFFF',            # Card backgrounds
    'bg_input': '#F0F0F0',           # Input field backgrounds
    'bg_hover': '#E8E8E8',           # Hover background

    # Text Colors (High Contrast)
    'text_primary': '#2C3E50',       # Dark text - main headings
    'text_secondary': '#5D6D7E',     # Medium gray text - descriptions
    'text_light': '#FFFFFF',         # White text - on dark backgrounds
    'text_muted': '#95A5A6',         # Light gray text - placeholders

    # Status Colors (Highly Visible with Good Contrast)
    'status_available': '#27AE60',   # Green - available/confirmed
    'status_occupied': '#E74C3C',    # Red - occupied/cancelled
    'status_pending': '#F39C12',     # Orange - pending
    'status_confirmed': '#3498DB',   # Blue - confirmed
    'status_checked_in': '#27AE60',  # Green - checked in
    'status_checked_out': '#95A5A6', # Gray - checked out
    'status_maintenance': '#E67E22', # Orange - maintenance

    # Border Colors (Minimal use - mostly removed)
    'border_light': '#E0E0E0',
    'border_medium': '#BDC3C7',
}


# ============================================================================
# Icon Helper - Returns FontAwesome QIcon via qtawesome
# ============================================================================

def get_icon(name: str, color=None) -> QIcon:
    """
    Get a FontAwesome icon by name using qtawesome.
    Returns professional icons matching the reference design.

    Args:
        name: Icon name (e.g., 'user', 'home', 'calendar')
        color: Optional QColor or hex string for icon color

    Returns:
        QIcon instance with FontAwesome glyph
    """
    # Map of icon names to FontAwesome icon names
    icon_map = {
        # Navigation icons
        'home': 'fa5s.home',
        'browse': 'fa5s.bed',
        'bed': 'fa5s.bed',
        'bookings': 'fa5s.calendar-alt',
        'calendar': 'fa5s.calendar-alt',
        'profile': 'fa5s.user',
        'user': 'fa5s.user',
        'dashboard': 'fa5s.chart-line',
        'rooms': 'fa5s.door-open',
        'guests': 'fa5s.users',
        'admin': 'fa5s.user-shield',

        # Action icons
        'logout': 'fa5s.sign-out-alt',
        'login': 'fa5s.sign-in-alt',
        'add': 'fa5s.plus',
        'edit': 'fa5s.pen',
        'delete': 'fa5s.trash',
        'search': 'fa5s.search',
        'export': 'fa5s.file-export',
        'save': 'fa5s.save',
        'cancel': 'fa5s.times',
        'confirm': 'fa5s.check',
        'view': 'fa5s.eye',
        'filter': 'fa5s.filter',
        'download': 'fa5s.download',

        # UI icons
        'email': 'fa5s.envelope',
        'phone': 'fa5s.phone',
        'lock': 'fa5s.lock',
        'unlock': 'fa5s.unlock',
        'eye': 'fa5s.eye',
        'eye_off': 'fa5s.eye-slash',
        'settings': 'fa5s.cog',
        'hotel': 'fa5s.hotel',
        'star': 'fa5s.star',
        'clock': 'fa5s.clock',
        'shield': 'fa5s.shield-alt',
        'dollar': 'fa5s.peso-sign',
        'wifi': 'fa5s.wifi',
        'tv': 'fa5s.tv',
        'ac': 'fa5s.wind',
        'coffee': 'fa5s.coffee',
        'concierge': 'fa5s.concierge-bell',
        'arrow_right': 'fa5s.arrow-right',
        'arrow_left': 'fa5s.arrow-left',
        'arrow_up': 'fa5s.arrow-up',
        'arrow_down': 'fa5s.arrow-down',

        # Status icons
        'success': 'fa5s.check-circle',
        'warning': 'fa5s.exclamation-triangle',
        'error': 'fa5s.times-circle',
        'info': 'fa5s.info-circle',
    }

    icon_name = icon_map.get(name, 'fa5s.circle')

    if color:
        if isinstance(color, str):
            color = QColor(color)
        return qta.icon(icon_name, color=color)
    return qta.icon(icon_name, color=QColor(COLORS['text_secondary']))


def get_icon_pixmap(name: str, size=24, color=None):
    """
    Get a FontAwesome icon as a pixmap for use in labels.

    Args:
        name: Icon name
        size: Size in pixels
        color: Optional QColor or hex string

    Returns:
        QPixmap with the rendered icon
    """
    icon = get_icon(name, color)
    from PyQt6.QtCore import QSize
    return icon.pixmap(QSize(size, size))


# ============================================================================
# Peso Formatting Helper
# ============================================================================

def peso_format(amount: float) -> str:
    """
    Format a number as Philippine Peso currency string.

    Args:
        amount: Numeric value to format

    Returns:
        Formatted peso string (e.g., "P1,500")
    """
    return f"P{amount:,.0f}"


def peso_format_with_decimals(amount: float) -> str:
    """
    Format a number as Philippine Peso with decimal places.

    Args:
        amount: Numeric value to format

    Returns:
        Formatted peso string with decimals (e.g., "P1,500.00")
    """
    return f"P{amount:,.2f}"
