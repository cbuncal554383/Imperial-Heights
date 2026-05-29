import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QStackedWidget, QMessageBox
)
from PyQt6.QtGui import QFont

# Models - pure data access layer
from models.database import Database, db

# Controllers - business logic layer
from controllers.auth_controller import AuthController
from controllers.booking_controller import BookingController

# Views - UI layer
from views.styles import COLORS
from views.login_view import LoginView
from views.customer_header import CustomerHeader
from views.room_browse_view import RoomBrowseView
from views.my_bookings_view import MyBookingsView
from views.profile_view import ProfileView
from views.admin_header import AdminHeader
from views.admin_dashboard_view import AdminDashboardView
from views.admin_rooms_view import AdminRoomsView
from views.admin_bookings_view import AdminBookingsView
from views.admin_guests_view import AdminGuestsView
from views.export_dialog import ExportDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imperial Heights - Hotel Management System")
        self.setMinimumSize(1280, 720)

        # Initialize controllers with database reference
        self.auth_controller = AuthController(db)
        self.booking_controller = BookingController(db)

        # Build UI components
        self.init_ui()
        self.setup_connections()
        self.apply_styles()

    def init_ui(self):
        """Initialize all UI components and layout structure."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Stacked widget for main views (login, customer, admin)
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Index 0: Login view
        self.login_view = LoginView()
        self.stack.addWidget(self.login_view)

        # Index 1: Customer container with header and content stack
        self.customer_container = QWidget()
        self.customer_layout = QVBoxLayout(self.customer_container)
        self.customer_layout.setContentsMargins(0, 0, 0, 0)
        self.customer_layout.setSpacing(0)

        self.customer_header = CustomerHeader()
        self.customer_layout.addWidget(self.customer_header)

        self.customer_stack = QStackedWidget()
        self.customer_layout.addWidget(self.customer_stack)

        # Customer pages
        self.room_browse_view = RoomBrowseView()
        self.customer_stack.addWidget(self.room_browse_view)

        self.my_bookings_view = MyBookingsView()
        self.customer_stack.addWidget(self.my_bookings_view)

        self.profile_view = ProfileView()
        self.customer_stack.addWidget(self.profile_view)

        self.stack.addWidget(self.customer_container)

        # Index 2: Admin container with header and content stack
        self.admin_container = QWidget()
        self.admin_layout = QVBoxLayout(self.admin_container)
        self.admin_layout.setContentsMargins(0, 0, 0, 0)
        self.admin_layout.setSpacing(0)

        self.admin_header = AdminHeader()
        self.admin_layout.addWidget(self.admin_header)

        self.admin_stack = QStackedWidget()
        self.admin_layout.addWidget(self.admin_stack)

        # Admin pages
        self.admin_dashboard_view = AdminDashboardView()
        self.admin_stack.addWidget(self.admin_dashboard_view)

        self.admin_rooms_view = AdminRoomsView()
        self.admin_stack.addWidget(self.admin_rooms_view)

        self.admin_bookings_view = AdminBookingsView()
        self.admin_stack.addWidget(self.admin_bookings_view)

        self.admin_guests_view = AdminGuestsView()
        self.admin_stack.addWidget(self.admin_guests_view)

        self.stack.addWidget(self.admin_container)

    def setup_connections(self):
        """
        Connect all signals between views and controllers.
        This decouples the UI from business logic.
        """
        # Auth controller signals
        self.auth_controller.login_success.connect(self.on_login_success)
        self.auth_controller.login_failed.connect(self.on_login_failed)
        self.auth_controller.registration_success.connect(self.on_registration_success)
        self.auth_controller.registration_failed.connect(self.on_registration_failed)
        self.auth_controller.logout_success.connect(self.on_logout)

        # Login view signals
        self.login_view.login_requested.connect(self.auth_controller.login)
        self.login_view.register_requested.connect(self.on_register_requested)
        self.login_view.admin_login_clicked.connect(self.on_admin_login_clicked)

        # Customer header signals
        self.customer_header.navigate.connect(self.on_customer_navigate)
        self.customer_header.logout.connect(self.auth_controller.logout)
        self.customer_header.switch_to_admin.connect(self.switch_to_admin)

        # Room browse signals
        self.room_browse_view.book_room.connect(self.on_book_room)

        # Bookings signals
        self.my_bookings_view.cancel_booking.connect(self.on_cancel_booking)

        # Profile signals
        self.profile_view.update_profile.connect(self.on_update_profile)
        self.profile_view.change_password.connect(self.on_change_password)

        # Admin header signals
        self.admin_header.navigate.connect(self.on_admin_navigate)
        self.admin_header.logout.connect(self.auth_controller.logout)
        self.admin_header.switch_to_customer.connect(self.switch_to_customer)
        self.admin_header.export_data.connect(self.on_export_data)

        # Admin dashboard signals
        self.admin_dashboard_view.checkin_guest.connect(self.on_admin_checkin)

        # Admin rooms signals
        self.admin_rooms_view.add_room.connect(self.on_add_room)
        self.admin_rooms_view.update_room_status.connect(self.on_update_room_status)

        # Admin bookings signals
        self.admin_bookings_view.confirm_booking.connect(self.on_confirm_booking)
        self.admin_bookings_view.checkin_booking.connect(self.on_admin_checkin)
        self.admin_bookings_view.checkout_booking.connect(self.on_admin_checkout)
        self.admin_bookings_view.cancel_booking.connect(self.on_cancel_booking)

        # Admin guests signals
        self.admin_guests_view.view_guest_bookings.connect(self.on_view_guest_bookings)

        # Booking controller signals
        self.booking_controller.booking_created.connect(self.on_booking_created)
        self.booking_controller.booking_cancelled.connect(self.on_booking_cancelled)
        self.booking_controller.error_occurred.connect(self.on_booking_error)

    def apply_styles(self):
        """Apply global application styles."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_main']};
            }}
            QWidget {{
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
        """)

    # ============================================================================
    # Authentication Handlers - login, logout, registration
    # ============================================================================

    def on_login_success(self, user):
        """
        Handle successful login - setup views and navigate.

        Args:
            user: User object from auth controller
        """
        self.customer_header.user_name = self.auth_controller.get_user_full_name()
        self.customer_header.is_admin = user.is_admin
        self.admin_header.user_name = self.auth_controller.get_user_full_name()

        self.room_browse_view.set_user_id(user.id)
        self.profile_view.set_user(user)

        self.refresh_data()

        if user.is_admin:
            self.stack.setCurrentIndex(2)
            self.admin_header.set_current_page('dashboard')
            self.admin_stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(1)
            self.customer_header.set_current_page('browse')
            self.customer_stack.setCurrentIndex(0)

        self.login_view.clear_fields()

    def on_login_failed(self, error_message):
        """Show login error message."""
        QMessageBox.warning(self, "Login Failed", error_message)

    def on_registration_success(self):
        """Show registration success and switch to login."""
        QMessageBox.information(
            self,
            "Registration Successful",
            "Your account has been created. Please sign in."
        )
        self.login_view.switch_tab(0)

    def on_registration_failed(self, error_message):
        """Show registration error."""
        QMessageBox.warning(self, "Registration Failed", error_message)

    def on_register_requested(self, email, password, confirm, first_name, last_name, phone):
        """Pass registration to auth controller."""
        self.auth_controller.register(email, password, confirm, first_name, last_name, phone)

    def on_admin_login_clicked(self):
        """Fill admin credentials for quick login."""
        self.login_view.email_input.setText("admin@imperialheights.com")
        self.login_view.password_input.setText("admin123")

    def on_logout(self):
        """Handle logout - return to login view."""
        self.stack.setCurrentIndex(0)
        self.customer_stack.setCurrentIndex(0)
        self.admin_stack.setCurrentIndex(0)

    # ============================================================================
    # Navigation Handlers - switch between pages
    # ============================================================================

    def on_customer_navigate(self, page):
        """Handle customer page navigation."""
        page_indices = {'browse': 0, 'bookings': 1, 'profile': 2}

        if page == 'bookings':
            self.load_user_bookings()

        self.customer_stack.setCurrentIndex(page_indices.get(page, 0))

    def on_admin_navigate(self, page):
        """Handle admin page navigation."""
        page_indices = {'dashboard': 0, 'rooms': 1, 'bookings': 2, 'guests': 3}

        if page == 'dashboard':
            self.refresh_dashboard()
        elif page == 'rooms':
            rooms = self.booking_controller.get_all_rooms()
            self.admin_rooms_view.set_rooms(rooms)
        elif page == 'bookings':
            bookings = self.booking_controller.get_all_bookings()
            self.admin_bookings_view.set_bookings(bookings)
        elif page == 'guests':
            guests = self.booking_controller.get_all_guests()
            self.admin_guests_view.set_guests(guests)

        self.admin_stack.setCurrentIndex(page_indices.get(page, 0))

    def switch_to_admin(self):
        """Switch from customer to admin view."""
        self.stack.setCurrentIndex(2)
        self.refresh_dashboard()

    def switch_to_customer(self):
        """Switch from admin to customer view."""
        self.stack.setCurrentIndex(1)
        self.refresh_data()

    # ============================================================================
    # Data Loading - refresh views with current data
    # ============================================================================

    def refresh_data(self):
        """Refresh all customer view data."""
        rooms = self.booking_controller.get_all_rooms()
        self.room_browse_view.set_rooms(rooms)

    def refresh_dashboard(self):
        """Refresh admin dashboard data."""
        stats = self.booking_controller.get_dashboard_stats()
        self.admin_dashboard_view.set_stats(stats)
        activities = self.booking_controller.get_recent_activities(5)
        self.admin_dashboard_view.set_activities(activities)
        checkins = self.booking_controller.get_today_checkins()
        self.admin_dashboard_view.set_checkins(checkins)

    def load_user_bookings(self):
        """Load current user's bookings into my bookings view."""
        bookings = self.booking_controller.get_user_bookings(
            self.auth_controller.current_user.id
        )
        bookings_dict = []
        for b in bookings:
            room = self.booking_controller.get_room_by_id(b.room_id)
            bookings_dict.append({
                'id': b.id,
                'room_number': room.room_number if room else 'N/A',
                'guest_name': b.guest_name,
                'check_in_date': b.check_in_date,
                'check_out_date': b.check_out_date,
                'num_guests': b.num_guests,
                'total_price': b.total_price,
                'status': b.status
            })
        self.my_bookings_view.set_bookings(bookings_dict)

    # ============================================================================
    # Booking Handlers - create, cancel, checkin, checkout
    # ============================================================================

    def on_book_room(self, room_id, booking_data):
        """Handle book room request from customer."""
        user_id = self.auth_controller.current_user.id
        booking_id = self.booking_controller.create_booking(
            user_id=user_id, room_id=room_id,
            check_in_date=booking_data['check_in'],
            check_out_date=booking_data['check_out'],
            guest_name=booking_data['guest_name'],
            guest_email=booking_data['guest_email'],
            guest_phone=booking_data['guest_phone'],
            num_guests=booking_data['num_guests']
        )
        if booking_id:
            QMessageBox.information(
                self, "Booking Confirmed",
                f"Your booking has been confirmed! Booking reference: #{booking_id}"
            )
            self.refresh_data()

    def on_cancel_booking(self, booking_id):
        """Handle booking cancellation."""
        success = self.booking_controller.cancel_booking(booking_id)
        if success:
            QMessageBox.information(self, "Booking Cancelled", "The booking has been cancelled.")
            if self.stack.currentIndex() == 1:
                self.load_user_bookings()
            else:
                bookings = self.booking_controller.get_all_bookings()
                self.admin_bookings_view.set_bookings(bookings)

    def on_booking_created(self, booking_id):
        """Handle booking created signal."""
        self.refresh_data()

    def on_booking_cancelled(self, booking_id):
        """Handle booking cancelled signal."""
        self.refresh_data()

    def on_booking_error(self, error_message):
        """Show booking error message."""
        QMessageBox.warning(self, "Booking Error", error_message)

    # ============================================================================
    # Profile Handlers - update profile, change password
    # ============================================================================

    def on_update_profile(self, profile_data):
        """Handle profile update."""
        self.auth_controller.update_profile(**profile_data)

    def on_change_password(self, old_password, new_password):
        """Handle password change with bcrypt verification."""
        success, message = self.auth_controller.change_password(old_password, new_password)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    # ============================================================================
    # Admin Handlers - checkin, checkout, confirm, add room
    # ============================================================================

    def on_admin_checkin(self, booking_id):
        """Handle admin check-in."""
        success = self.booking_controller.check_in(booking_id)
        if success:
            QMessageBox.information(self, "Success", "Guest checked in successfully!")
            self.refresh_dashboard()
            bookings = self.booking_controller.get_all_bookings()
            self.admin_bookings_view.set_bookings(bookings)

    def on_admin_checkout(self, booking_id):
        """Handle admin check-out."""
        success = self.booking_controller.check_out(booking_id)
        if success:
            QMessageBox.information(self, "Success", "Guest checked out successfully!")
            self.refresh_dashboard()
            bookings = self.booking_controller.get_all_bookings()
            self.admin_bookings_view.set_bookings(bookings)

    def on_confirm_booking(self, booking_id):
        """Handle booking confirmation."""
        success = self.booking_controller.confirm_booking(booking_id)
        if success:
            QMessageBox.information(self, "Success", "Booking confirmed!")
            bookings = self.booking_controller.get_all_bookings()
            self.admin_bookings_view.set_bookings(bookings)

    def on_add_room(self, room_data):
        """Handle add room."""
        room_id = self.booking_controller.create_room(**room_data)
        if room_id:
            QMessageBox.information(self, "Success", f"Room added successfully!")
            rooms = self.booking_controller.get_all_rooms()
            self.admin_rooms_view.set_rooms(rooms)

    def on_update_room_status(self, room_id, status):
        """Handle room status update."""
        success = self.booking_controller.update_room_status(room_id, status)
        if success:
            rooms = self.booking_controller.get_all_rooms()
            self.admin_rooms_view.set_rooms(rooms)

    def on_view_guest_bookings(self, user_id):
        """View a specific guest's bookings."""
        bookings = self.booking_controller.get_user_bookings(user_id)
        self.admin_bookings_view.set_bookings(bookings)
        self.admin_header.set_current_page('bookings')
        self.admin_stack.setCurrentIndex(2)

    # ============================================================================
    # Export Handler - admin only data export
    # ============================================================================

    def on_export_data(self):
        """
        Handle data export request.
        Only admins can export data - enforced by UI (no export button for customers).
        Supports date range selection for bookings.
        """
        dialog = ExportDialog(self)
        if dialog.exec() == ExportDialog.DialogCode.Accepted:
            params = dialog.get_export_params()
            success = False

            if params['type'] == 'bookings':
                success = self.booking_controller.export_bookings_to_csv(
                    params['start_date'], params['end_date'], params['file_path']
                )
            elif params['type'] == 'rooms':
                success = self.booking_controller.export_rooms_to_csv(params['file_path'])
            elif params['type'] == 'guests':
                success = self.booking_controller.export_guests_to_csv(params['file_path'])

            if success:
                QMessageBox.information(self, "Export Complete",
                    f"Data exported successfully to:\n{params['file_path']}")
            else:
                QMessageBox.warning(self, "Export Failed",
                    "No data found for the selected criteria.")


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
