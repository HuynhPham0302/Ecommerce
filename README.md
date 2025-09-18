# E-commerce API Project

## Project Overview

This is a comprehensive Flask-based REST API for an e-commerce platform. The application provides a complete backend solution for managing users, products, orders, payments, and addresses in an online shopping environment.

### Key Features

- 👥 User authentication and management (Customer/Admin roles)
- 📦 Product catalog with categories and inventory tracking
- 🛒 Shopping cart and order processing
- 💳 Payment tracking and management
- 📍 Multiple address management per user
- 🔐 Role-based access control
- 🌱 Database seeding for development
- 📊 Standardized API response format

## Tech Stack

- **Backend Framework**: Flask (Python)
- **Database**: MySQL with SQLAlchemy ORM
- **Environment Management**: python-dotenv for configuration
- **Database Migration**: Flask-SQLAlchemy
- **Development Tools**: Make for task automation
- **Password Security**: Bcrypt hashing (recommended)
- **API Standards**: RESTful design with JSON responses

## Project Structure

```
Ecommerce/
├── application.py          # Application entry point
├── schema.sql             # Database schema definition
├── seed_db.py            # Database seeding script
├── Makefile              # Development commands
├── LICENSE               # Project license
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
│
├── app/                  # Main application package
│   ├── __init__.py      # App factory
│   ├── config.py        # Configuration settings
│   ├── extensions.py    # Flask extensions
│   │
│   ├── models/          # Data models (SQLAlchemy)
│   │   ├── user.py      # User model with roles
│   │   ├── product.py   # Product catalog model
│   │   ├── category.py  # Product categories
│   │   ├── address.py   # User addresses
│   │   ├── order.py     # Order management
│   │   ├── order_item.py # Order line items
│   │   └── payment.py   # Payment transactions
│   │
│   ├── api/             # REST API endpoints
│   │   ├── users.py     # User management endpoints
│   │   ├── products.py  # Product CRUD operations
│   │   ├── categories.py # Category management
│   │   ├── addresses.py # Address management
│   │   ├── orders.py    # Order processing
│   │   ├── order_items.py # Order item management
│   │   ├── payments.py  # Payment handling
│   │   └── auth.py      # Authentication endpoints
│   │
│   ├── utils/           # Utility functions
│   │   └── api_helpers.py # Standardized API responses
│   │
│   └── serializers/     # Data serialization (if used)
```

## Data Model

### Core Entities

#### Users
- **Fields**: id, first_name, last_name, email, password_hash, phone_number, role
- **Roles**: CUSTOMER, ADMIN  
- **Relationships**: One-to-many with addresses and orders

#### Products
- **Fields**: id, category_id, name, description, price, sku, stock_quantity, image_url
- **Relationships**: Belongs to category, appears in order items

#### Categories
- **Fields**: id, name, description
- **Purpose**: Organize products for better navigation

#### Addresses  
- **Fields**: id, user_id, address_line1, address_line2, city, state_province_region, postal_code, country
- **Purpose**: Multiple shipping/billing addresses per user

#### Orders
- **Fields**: id, user_id, shipping_address_id, order_date, status, total_amount, shipping_method
- **Status**: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED
- **Relationships**: Belongs to user and address, has many order items and payments

#### Order Items
- **Fields**: id, order_id, product_id, quantity, price_per_unit
- **Purpose**: Junction table for products in orders (captures price at purchase time)

#### Payments
- **Fields**: id, order_id, payment_method, transaction_id, amount, status, payment_date
- **Status**: PENDING, COMPLETED, FAILED, REFUNDED

### Entity Relationship Diagram

```
Users (1) ←→ (N) Addresses
Users (1) ←→ (N) Orders
Categories (1) ←→ (N) Products
Products (1) ←→ (N) Order_Items
Orders (1) ←→ (N) Order_Items
Orders (1) ←→ (N) Payments
Addresses (1) ←→ (N) Orders
```

## API Endpoint Design

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints
```
POST /api/auth/login       # User login
POST /api/auth/register    # User registration
POST /api/auth/logout      # User logout
```

### User Management
```
GET    /api/users          # Get all users (Admin)
GET    /api/users/{id}     # Get user by ID
POST   /api/users          # Create new user
PUT    /api/users/{id}     # Update user
DELETE /api/users/{id}     # Delete user
```

### Product Management
```
GET    /api/products       # Get all products
GET    /api/products/{id}  # Get product by ID  
POST   /api/products       # Create product (Admin)
PUT    /api/products/{id}  # Update product (Admin)
DELETE /api/products/{id}  # Delete product (Admin)
```

### Category Management
```
GET    /api/categories     # Get all categories
GET    /api/categories/{id} # Get category by ID
POST   /api/categories     # Create category (Admin)
PUT    /api/categories/{id} # Update category (Admin)
DELETE /api/categories/{id} # Delete category (Admin)
```

### Address Management
```
GET    /api/addresses      # Get user addresses
POST   /api/addresses      # Add new address
PUT    /api/addresses/{id} # Update address
DELETE /api/addresses/{id} # Delete address
```

### Order Management
```
GET    /api/orders         # Get user orders
GET    /api/orders/{id}    # Get order details
POST   /api/orders         # Create new order
PUT    /api/orders/{id}    # Update order status
DELETE /api/orders/{id}    # Cancel order
```

### Order Items Management
```
GET    /api/order-items     # Get order items for an order
POST   /api/order-items     # Add item to order
PUT    /api/order-items/{id} # Update order item
DELETE /api/order-items/{id} # Remove item from order
```

### Payment Management
```
GET    /api/payments        # Get payments for user/order
POST   /api/payments        # Process payment
PUT    /api/payments/{id}   # Update payment status
```

### Standard API Response Format

#### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "timestamp": "2025-09-17T10:30:00.000Z"
}
```

#### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error_code": 404,
  "timestamp": "2025-09-17T10:30:00.000Z"
}
```

## Business Flow for Frontend

### User Registration & Authentication Flow
1. **User Registration**: POST `/api/auth/register` → Create user account
2. **User Login**: POST `/api/auth/login` → Authenticate and get token
3. **Profile Management**: GET/PUT `/api/users/{id}` → View/update profile

### Shopping Flow
1. **Browse Categories**: GET `/api/categories` → Display product categories
2. **View Products**: GET `/api/products` → Show product catalog
3. **Product Details**: GET `/api/products/{id}` → Show detailed product info
4. **Add to Cart**: Frontend state management for cart items
5. **Address Selection**: GET `/api/addresses` → Choose shipping address
6. **Create Order**: POST `/api/orders` → Convert cart to order
7. **Add Order Items**: POST `/api/order-items` → Add products to order
8. **Process Payment**: POST `/api/payments` → Handle payment

### Order Management Flow
1. **View Orders**: GET `/api/orders` → Display user's order history
2. **Order Details**: GET `/api/orders/{id}` → Show specific order details
3. **Track Order**: GET `/api/orders/{id}` → Check order status
4. **Cancel Order**: PUT `/api/orders/{id}` → Update status to cancelled

### Admin Management Flow
1. **Product Management**: CRUD operations on `/api/products`
2. **Category Management**: CRUD operations on `/api/categories`
3. **Order Management**: View and update all orders
4. **User Management**: View and manage all users

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ecommerce
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy python-dotenv bcrypt
   # Add other dependencies as needed
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=mysql://username:password@localhost/ecommerce_db
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Database Setup**
   ```bash
   # Create database using schema.sql
   mysql -u username -p < schema.sql
   
   # Seed database with sample data
   make seed
   # or
   python3 seed_db.py
   ```

### Running the Application

1. **Start the development server**
   ```bash
   make run
   # or
   python3 application.py
   ```

2. **Access the API**
   - Base URL: `http://localhost:5000`
   - API endpoints: `http://localhost:5000/api/*`

### Available Make Commands

```bash
make run    # Start the development server
make seed   # Seed database with sample data
```

## Development Guidelines

### Adding New Endpoints
1. Create endpoint functions in appropriate API module (`app/api/`)
2. Register blueprint in `app/api/__init__.py`
3. Use `APIResponse` class for consistent response formatting
4. Add proper error handling and validation

### Database Changes
1. Update model classes in `app/models/`
2. Update `schema.sql` file
3. Update `seed_db.py` if sample data is needed
4. Test migrations thoroughly

### Code Standards
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings for complex functions
- Include error handling for all API endpoints
- Use proper HTTP status codes

## Testing

### Manual Testing
Use tools like Postman, curl, or HTTPie to test API endpoints:

```bash
# Get all products
curl -X GET http://localhost:5000/api/products

# Create a new user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"password123"}'
```

### Database Testing
```bash
# Seed fresh data
make seed

# Verify data in MySQL
mysql -u username -p ecommerce_db
SELECT * FROM users LIMIT 5;
```

## Security Considerations

- ⚠️ **Authentication**: Currently, auth endpoints exist but may need JWT implementation
- ⚠️ **Authorization**: Admin-only routes are commented out - implement role checking
- ⚠️ **Password Security**: Use bcrypt for password hashing
- ⚠️ **Input Validation**: Add proper request validation
- ⚠️ **SQL Injection**: Using SQLAlchemy ORM helps prevent this
- ⚠️ **Environment Variables**: Never commit `.env` file to version control

## Deployment Considerations

### Production Environment
- Use a production WSGI server (Gunicorn, uWSGI)
- Set up proper logging
- Use environment-specific configuration
- Set up database connection pooling
- Implement rate limiting
- Add request/response logging

### Environment Variables for Production
```env
DATABASE_URL=mysql://user:pass@production-host/ecommerce_db
SECRET_KEY=production-secret-key-very-secure
DEBUG=False
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For questions or issues, please:
1. Check existing documentation
2. Review API endpoint implementations
3. Examine database schema and models
4. Test with sample data using `make seed`

---

*Generated on September 17, 2025 - This documentation reflects the current state of the E-commerce API project.*  