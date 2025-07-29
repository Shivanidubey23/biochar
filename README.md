# Biochar Carbon Credits API

A Django REST API for handling contact form submissions for a biochar carbon credits platform.

## Features

- **POST API**: Submit contact form data (name, email, interests, message)
- **GET API**: Retrieve all contact form submissions
- PostgreSQL database for data storage
- Django admin interface for data management
- Input validation and exception handling

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Setup Instructions

### 1. Install PostgreSQL

**Windows**: Download from https://www.postgresql.org/download/windows/
**macOS**: `brew install postgresql`
**Ubuntu**: `sudo apt install postgresql postgresql-contrib`

### 2. Create Database and User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE biochar_db;
CREATE USER biochar_user WITH PASSWORD 'biochar123';
GRANT ALL PRIVILEGES ON DATABASE biochar_db TO biochar_user;
GRANT USAGE ON SCHEMA public TO biochar_user;
GRANT CREATE ON SCHEMA public TO biochar_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO biochar_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO biochar_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO biochar_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO biochar_user;

\q
```

### 3. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd biochar

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=biochar_db
DB_USER=biochar_user
DB_PASSWORD=biochar123
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Migration

```bash
# Create migrations
python manage.py makemigrations carbon_api

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Submit Contact Form
- **URL**: `POST /api/submit-contact/`
- **Description**: Submit a contact form
- **Payload**:
```json
{
    "full_name": "John Doe",
    "email": "john@example.com",
    "interests": ["Offset Emissions", "Explore Partnership"],
    "inquiry_message": "I want to offset my carbon footprint"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "Contact form submitted successfully!",
    "data": {
        "id": "uuid-here",
        "full_name": "John Doe",
        "email": "john@example.com",
        "interests": ["Offset Emissions", "Explore Partnership"],
        "inquiry_message": "I want to offset my carbon footprint",
        "created_at": "2025-01-01T10:00:00Z"
    }
}
```

### Get Contact Forms
- **URL**: `GET /api/contacts/`
- **Description**: Retrieve all contact form submissions
- **Response**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "uuid-here",
            "full_name": "John Doe",
            "email": "john@example.com",
            "interests": ["Offset Emissions"],
            "inquiry_message": "Test message",
            "created_at": "2025-01-01T10:00:00Z"
        }
    ]
}
```

## Testing the APIs

### Using curl

**Test POST API:**
```bash
curl -X POST http://127.0.0.1:8000/api/submit-contact/ \
-H "Content-Type: application/json" \
-d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "interests": ["Offset Emissions"],
    "inquiry_message": "Test message"
}'
```

**Test GET API:**
```bash
curl http://127.0.0.1:8000/api/contacts/
```

### Using Django Admin

1. Visit: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Go to "Contact forms" to see submitted data
4. You can manually add/edit contact forms here

## Valid Interest Options

The frontend should use these exact values for the interests field:
- "Offset Emissions"
- "Explore Partnership" 
- "Support Farmers"
- "Join as a Volunteer"
- "Other"

## Field Validation

- **full_name**: Required, minimum 2 characters, letters/spaces/hyphens/apostrophes only
- **email**: Required, valid email format
- **interests**: Required, must be array with at least 1 interest, maximum 5 interests
- **inquiry_message**: Optional, maximum 2000 characters

## Project Structure

```
biochar/
├── biochar_project/          # Django project settings
│   ├── settings.py          # Database and app configuration
│   └── urls.py              # Main URL routing
├── apps/
│   └── carbon_api/          # Main API app
│       ├── models.py        # Database models
│       ├── serializers.py   # Data validation
│       ├── views.py         # API endpoints
│       ├── urls.py          # API URL routing
│       └── admin.py         # Admin interface
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── manage.py               # Django management
```

## Dependencies

```txt
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.7
python-decouple==3.8
django-cors-headers==4.3.1
whitenoise==6.6.0
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in `.env` file
- Check if user has proper permissions

### Migration Issues
```bash
# Reset migrations if needed
python manage.py migrate carbon_api zero
python manage.py makemigrations carbon_api
python manage.py migrate
```

### Permission Errors
Make sure PostgreSQL user has all necessary permissions as shown in setup step 2.
