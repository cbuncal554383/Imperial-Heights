# Imperial-Heights
Imperial Heights - Hotel Management System A PyQt6-based Hotel Management System with MVC architecture, featuring customer and admin views, room booking, and data export functionality.
Features
Customer View
Browse available rooms with filters (All, Single, Double, Suite)
Book rooms with date selection and guest information
View and manage personal bookings
Edit profile information
Change password with visibility toggle
Admin View
Dashboard with statistics (Total Rooms, Guests, Bookings, Revenue)
Recent activities feed
Today's check-ins management
Room management (add rooms, update status)
Booking management (confirm, check-in, check-out, cancel)
Guest management with search
Export data to CSV (admin only)
MVC Architecture
imperial_heights/
├── main.py              # Application entry point
├── models/              # Data access layer
│   ├── __init__.py
│   └── database.py      # SQLite database operations
├── controllers/         # Business logic layer
│   ├── __init__.py
│   ├── auth_controller.py     # Authentication
│   └── booking_controller.py  # Booking operations
├── views/               # UI layer
│   ├── __init__.py
│   ├── styles.py        # Colors, icons, and styling
│   ├── login_view.py    # Login/Register
│   ├── customer_header.py     # Customer navigation
│   ├── admin_header.py        # Admin navigation
│   ├── room_browse_view.py    # Browse rooms
│   ├── my_bookings_view.py    # My bookings
│   ├── profile_view.py        # Profile
│   ├── admin_dashboard_view.py
│   ├── admin_rooms_view.py
│   ├── admin_bookings_view.py
│   ├── admin_guests_view.py
│   └── export_dialog.py
├── database/            # Auto-created SQLite database
├── view_mysql_tables.py # MySQL table viewer
└── requirements.txt
Installation
Install Python 3.8 or higher
Install dependencies:
pip install -r requirements.txt
Running the Application
python main.py
Default Login Credentials
Admin Account
Email: admin@imperialheights.com
Password: admin123
Customer Accounts
Email: juan.delacruz@email.com

Password: password123

Email: maria.clara@email.com

Password: password123

MySQL Table Viewer
To view tables in MySQL:

Update MYSQL_CONFIG in view_mysql_tables.py with your credentials
Run:
python view_mysql_tables.py
This will display all tables and statistics from your MySQL database.

Features Implemented
No unnecessary borders - clean modern UI
High contrast stats colors for visibility
Visible action buttons on all tables (FIXED)
No visible IDs in the interface
Textbox height optimized for 1920x1080 (FIXED)
Fixed alignments throughout (FIXED)
Password toggle on all password fields
No overlapping components (FIXED)
Working authentication with bcrypt (FIXED)
Password encryption (bcrypt with 12 rounds)
FontAwesome icons via qtawesome (no emojis)
No transactions in the model layer
Data export with date range (admin only)
MySQL table viewer included
Comprehensive comments throughout
Only admins can export data
Admin/Customer view switch for admin users
