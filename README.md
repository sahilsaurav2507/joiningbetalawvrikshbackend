# LawVriksh Backend API

A production-ready FastAPI backend for the LawVriksh website, providing APIs for waiting list management, feedback collection, and admin operations.

## 🚀 Features

- **User Management**: Registration for users and creators on waiting lists
- **Feedback System**: Multi-step feedback collection with ratings and suggestions
- **Admin Dashboard**: Secure admin interface for data management
- **Authentication**: JWT-based authentication for admin access
- **Data Export**: Excel/CSV export functionality
- **Rate Limiting**: Built-in rate limiting for API protection
- **CORS Support**: Configured for frontend integration
- **Database**: MySQL with SQLAlchemy ORM
- **Validation**: Comprehensive input validation with Pydantic
- **Logging**: Structured logging for monitoring and debugging

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- Redis (optional, for session storage)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd joiningbetalawvrikshbackend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the environment template and configure your settings:

```bash
cp env.example .env
```

Edit `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost/lawvriksh_db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
CORS_ORIGINS=https://lawvriksh.com,https://www.lawvriksh.com
CORS_ALLOW_CREDENTIALS=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
ADMIN_RATE_LIMIT_PER_MINUTE=100

# Environment
ENVIRONMENT=development
DEBUG=true
```

### 5. Database Setup

Create the MySQL database:

```sql
CREATE DATABASE lawvriksh_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Initialize Database

```bash
python -c "from app.database import init_db; init_db()"
```

## 🚀 Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Docs**: http://localhost:8000/api/docs
- **ReDoc Documentation**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## 🔐 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/auth/refresh` - Refresh token

### User Management
- `POST /api/v1/users/register` - Register user for waiting list
- `GET /api/v1/admin/users` - Get all users (admin only)

### Creator Management
- `POST /api/v1/creators/register` - Register creator for waiting list
- `GET /api/v1/admin/creators` - Get all creators (admin only)

### Not Interested
- `POST /api/v1/not-interested` - Submit not interested data
- `GET /api/v1/admin/not-interested` - Get not interested users (admin only)

### Feedback System
- `POST /api/v1/feedback/start` - Start feedback session
- `POST /api/v1/feedback/ui-ratings` - Submit UI ratings
- `POST /api/v1/feedback/ux-ratings` - Submit UX ratings
- `POST /api/v1/feedback/suggestions` - Submit suggestions
- `GET /api/v1/feedback/{session_id}` - Get feedback by session
- `GET /api/v1/admin/feedback` - Get all feedback (admin only)

### Admin Operations
- `POST /api/v1/admin/export` - Export data to Excel/CSV
- `GET /api/v1/admin/dashboard` - Dashboard statistics

## 🏗️ Project Structure

```
joiningbetalawvrikshbackend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── repositories/          # Data access layer
│   ├── services/              # Business logic
│   ├── routes/                # API endpoints
│   └── utils/                 # Utility functions
├── tests/                     # Test suite
├── logs/                      # Application logs
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .env                       # Environment variables
├── env.example               # Environment template
├── wsgi.py                   # WSGI entry point
└── README.md                 # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Run tests with verbose output
pytest -v
```

## 🚀 Deployment

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t lawvriksh-backend .
```

2. Run the container:

```bash
docker run -d -p 8000:8000 --env-file .env lawvriksh-backend
```

### Production Deployment

1. Set up a production server (Ubuntu recommended)
2. Install Python, MySQL, and Nginx
3. Configure environment variables for production
4. Set up SSL certificates
5. Configure Nginx as reverse proxy
6. Use systemd for process management

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name api.lawvriksh.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.lawvriksh.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- Rate limiting
- SQL injection prevention
- XSS protection

## 📊 Monitoring

The application includes:

- Request/response logging
- Error tracking
- Performance monitoring
- Health check endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the API documentation

## 🔄 Updates

To update the application:

1. Pull the latest changes
2. Update dependencies: `pip install -r requirements.txt`
3. Run database migrations (if any)
4. Restart the application

---

**LawVriksh Backend API** - Built with FastAPI and MySQL 