# Food Booking System

A console-based Food Booking System developed using Python and MySQL. The application allows users to register, browse restaurants and menu items, place food orders, and manage account details. It also includes an administrator interface for managing restaurants, menu items, and orders.

## Features

### User Features

- User Registration and Login
- View Available Restaurants
- View Restaurant Menus
- Place Food Orders
- Update Username and Password
- Logout Functionality

### Admin Features

- Add Restaurants
- Add Menu Items
- View Restaurants and Menus
- Update Restaurant Details
- Update Menu Items
- Delete Restaurants
- Delete Menu Items
- View Customer Orders

## Technologies Used

- Python
- MySQL
- mysql-connector-python

## Database Schema

The application uses the following tables:

- users
- restaurants
- menu_items
- orders

Relationships are managed using primary keys and foreign key constraints.

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MySQL

Ensure MySQL is installed and running.

Update the database connection credentials in the Python file:

```python
host="localhost"
user="root"
password="your_password"
```

### 3. Run the Application

```bash
python OnlineFoodBooking.py
```

## Learning Outcomes

- Python Programming
- MySQL Database Management
- CRUD Operations
- Relational Database Design
- User Authentication
- Database Connectivity using Python

## Future Improvements

- Graphical User Interface (GUI)
- Web-based Frontend
- Password Encryption
- Online Payment Integration
- Order Tracking System

## Author

Neha
B.Tech Computer Science and Engineering
