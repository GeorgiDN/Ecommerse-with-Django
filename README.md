# Django eCommerce Platform

A full-featured eCommerce platform built with Django that supports product variants, guest checkout, email notifications, and admin management.

## Key Features

### User Features
- ✅ **User authentication** (register/login/logout)
- ✅ **Password management** (reset/change)
- ✅ **Guest checkout** (no account required)
- ✅ **Persistent cart** (saves when logged in/out)
- ✅ **Email notifications** for:
  - Account registration
  - Password resets
  - Order confirmations

### Product Features
- 🛍️ **Product variants/options** (size, color, etc.)
- ⚖️ **Inventory tracking** (optional per product)
- 📊 **Bulk product management** (import/export via Excel)
- 🏷️ **Product categorization**
- 🔍 **Advanced search** (name, SKU, tags, description)

### Admin Features
- 👔 **Staff dashboard** with order management
- 📦 **Product CRUD operations**
- 📁 **Category management**
- 📈 **Bulk operations**:
  - Activate/deactivate products
  - Update availability
  - Category assignments
  - Mass deletion
- 📥📤 **Data import/export** (Excel format)

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or SQLite

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/GeorgiDN/Ecommerse-with-Django.git


### 2. Open the project


### 3. Install dependencies
 
   ```terminal
   
     pip install -r requirements.txt
  
   ```

### 4. Change DB settings in settings.py

  ```py
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "your_db_name",
            "USER": "your_username",
            "PASSWORD": "your_pass",
            "HOST": "your_host",
            "PORT": "your_port",
        }
    }
  ```

### 5. Run the migrations

  ```terminal

    python manage.py migrate

  ```

### 6. Run the project

  ```terminal

    python manage.py runserver

  ```
