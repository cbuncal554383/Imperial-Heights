"""
Authentication Controller for Imperial Heights Hotel Management System
Handles user authentication, registration, and session management
Passwords are encrypted using bcrypt with 12 rounds of hashing
FIXED: Authentication flow works correctly with proper password verification
"""

from typing import Optional, Callable
import bcrypt
from PyQt6.QtCore import QObject, pyqtSignal
from models.database import Database, User


class AuthController(QObject):
    """
    Controller for handling authentication operations.
    Uses bcrypt for secure password hashing with 12 rounds.
    Manages user sessions and login state.
    """

    # Signals for communicating with views - decouples controller from UI
    login_success = pyqtSignal(object)       # Emits User object on successful login
    login_failed = pyqtSignal(str)           # Emits error message on failed login
    logout_success = pyqtSignal()            # Emitted on logout
    registration_success = pyqtSignal()      # Emitted on successful registration
    registration_failed = pyqtSignal(str)    # Emits error message on failed registration

    def __init__(self, database: Database):
        """
        Initialize auth controller with database reference.

        Args:
            database: Database instance for user operations
        """
        super().__init__()
        self.db = database
        self._current_user: Optional[User] = None
        self._on_login_success: Optional[Callable] = None
        self._on_logout: Optional[Callable] = None

    # ============================================================================
    # Properties - provide read-only access to auth state
    # ============================================================================

    @property
    def current_user(self) -> Optional[User]:
        """Get the currently logged in user."""
        return self._current_user

    @property
    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self._current_user is not None

    @property
    def is_admin(self) -> bool:
        """Check if current user has admin privileges."""
        return self._current_user is not None and self._current_user.is_admin

    # ============================================================================
    # Password Hashing - bcrypt with 12 rounds for security
    # ============================================================================

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def _verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password to verify
            hashed: Stored hash to compare against

        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    # ============================================================================
    # Login / Logout - session management
    # ============================================================================

    def login(self, email: str, password: str) -> bool:
        """
        Authenticate user with email and password.
        FIXED: Properly handles both first-time login (HASH_PLACEHOLDER)
        and subsequent logins with bcrypt verification.

        Args:
            email: User's email address
            password: User's password (plain text)

        Returns:
            True if login successful, False otherwise
        """
        # Validate inputs are not empty
        if not email or not password:
            self.login_failed.emit("Please enter both email and password")
            return False

        # Look up user by email
        user = self.db.get_user_by_email(email)
        if user is None:
            self.login_failed.emit("Invalid email or password")
            return False

        # For initial admin setup - check if password is the placeholder
        if user.password == 'HASH_PLACEHOLDER':
            # First login with placeholder - allow default passwords
            default_passwords = {
                'admin@imperialheights.com': 'admin123',
                'juan.delacruz@email.com': 'password123',
                'maria.clara@email.com': 'password123'
            }
            if email in default_passwords and password == default_passwords[email]:
                # Hash the password and update in database
                hashed = self._hash_password(password)
                self.db.update_user(user.id, password=hashed)
                # Reload user with new password
                user = self.db.get_user_by_id(user.id)
            else:
                self.login_failed.emit("Invalid email or password")
                return False
        else:
            # Normal login with bcrypt verification
            if not self._verify_password(password, user.password):
                self.login_failed.emit("Invalid email or password")
                return False

        # Login successful - store user and emit signal
        self._current_user = user
        self.login_success.emit(user)
        if self._on_login_success:
            self._on_login_success(user)
        return True

    def logout(self):
        """Log out the current user and clear session."""
        self._current_user = None
        self.logout_success.emit()
        if self._on_logout:
            self._on_logout()

    # ============================================================================
    # Registration - new user creation with password hashing
    # ============================================================================

    def register(self, email: str, password: str, confirm_password: str,
                 first_name: str, last_name: str, phone: str = "") -> bool:
        """
        Register a new user account with bcrypt password hashing.

        Args:
            email: User's email address
            password: User's password
            confirm_password: Password confirmation
            first_name: User's first name
            last_name: User's last name
            phone: User's phone number (optional)

        Returns:
            True if registration successful, False otherwise
        """
        # Validate required fields
        if not email or not password or not first_name or not last_name:
            self.registration_failed.emit("Please fill in all required fields")
            return False

        # Check passwords match
        if password != confirm_password:
            self.registration_failed.emit("Passwords do not match")
            return False

        # Validate password length
        if len(password) < 6:
            self.registration_failed.emit("Password must be at least 6 characters")
            return False

        # Check if email already exists
        existing_user = self.db.get_user_by_email(email)
        if existing_user:
            self.registration_failed.emit("Email already registered")
            return False

        # Hash password before storing
        hashed_password = self._hash_password(password)

        # Create new user with hashed password
        try:
            user_id = self.db.create_user(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                is_admin=False
            )
            if user_id:
                self.registration_success.emit()
                return True
            else:
                self.registration_failed.emit("Failed to create account")
                return False
        except Exception as e:
            self.registration_failed.emit(f"Registration error: {str(e)}")
            return False

    # ============================================================================
    # Profile Management - update user info
    # ============================================================================

    def update_profile(self, **kwargs) -> bool:
        """
        Update current user's profile information.

        Args:
            **kwargs: Fields to update (email, first_name, last_name, phone)

        Returns:
            True if update successful, False otherwise
        """
        if not self._current_user:
            return False
        success = self.db.update_user(self._current_user.id, **kwargs)
        if success:
            self._current_user = self.db.get_user_by_id(self._current_user.id)
        return success

    def change_password(self, old_password: str, new_password: str) -> tuple:
        """
        Change user password with verification.
        FIXED: Properly verifies old password against bcrypt hash before updating.

        Args:
            old_password: Current password for verification
            new_password: New password to set

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self._current_user:
            return False, "Not logged in"

        # Verify old password
        if self._current_user.password == 'HASH_PLACEHOLDER':
            return False, "Please login first to set your password"

        if not self._verify_password(old_password, self._current_user.password):
            return False, "Current password is incorrect"

        # Hash and update new password
        hashed = self._hash_password(new_password)
        success = self.db.update_user(self._current_user.id, password=hashed)
        if success:
            self._current_user = self.db.get_user_by_id(self._current_user.id)
            return True, "Password changed successfully"
        return False, "Failed to update password"

    # ============================================================================
    # Callbacks - optional external handlers
    # ============================================================================

    def set_login_callback(self, callback: Callable):
        """Set callback for successful login."""
        self._on_login_success = callback

    def set_logout_callback(self, callback: Callable):
        """Set callback for logout."""
        self._on_logout = callback

    def get_user_full_name(self) -> str:
        """Get current user's full name."""
        if self._current_user:
            return f"{self._current_user.first_name} {self._current_user.last_name}"
        return "Guest"
