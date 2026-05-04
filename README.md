# Learn Backend Course - Social Media API

A comprehensive FastAPI-based backend application demonstrating modern web development practices including RESTful API design, authentication, database management, and deployment.

## 🚀 Deployed API

The API is live and available at:
**https://backend-tutorial-sahil-ab3c3398e7b9.herokuapp.com/**

## 📋 Project Overview

This is a full-featured social media backend API built with FastAPI that includes:
- User authentication and authorization
- Post creation, management, and voting system
- Database migrations with Alembic
- Secure password hashing
- JWT-based authentication
- PostgreSQL database integration
- CORS support for frontend integration

## 🛠️ Technology Stack

### Core Framework
- **FastAPI 0.135.1** - Modern, fast web framework for building APIs
- **Uvicorn 0.41.0** - ASGI server for running FastAPI applications

### Database & ORM
- **SQLAlchemy 2.0.48** - SQL toolkit and ORM
- **Alembic 1.18.4** - Database migration tool
- **psycopg2-binary 2.9.11** - PostgreSQL adapter for Python

### Authentication & Security
- **python-jose 3.3.0** - JWT token handling
- **passlib 1.7.4** - Password hashing utilities
- **bcrypt 4.1.2** - Password hashing algorithm
- **python-multipart 0.0.22** - Form data parsing

### Data Validation & Configuration
- **Pydantic 2.12.5** - Data validation using Python type annotations
- **pydantic-settings 2.13.1** - Settings management
- **email-validator 2.3.0** - Email validation
- **python-dotenv 1.2.2** - Environment variable management

### HTTP Client
- **httpx 0.28.1** - Async HTTP client for testing

## 📁 Project Structure

```
learn-backend-course/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application settings
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── oauth2.py            # JWT authentication logic
│   ├── utils.py             # Utility functions
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       ├── post.py          # Post management endpoints
│       ├── user.py          # User management endpoints
│       └── vote.py          # Voting system endpoints
├── alembic/                 # Database migrations
├── .env                     # Environment variables
├── alembic.ini              # Alembic configuration
├── pyproject.toml           # Project dependencies
├── requirements.txt         # Compatibility requirements file
└── Procfile                 # Heroku deployment configuration
```

## 🗄️ Database Models

### Users
- **id**: Primary key
- **email**: Unique email address
- **password**: Hashed password
- **created_at**: Account creation timestamp
- **mobile_no**: Optional mobile number

### Posts
- **id**: Primary key
- **title**: Post title
- **content**: Post content
- **published**: Publication status
- **created_at**: Creation timestamp
- **owner_id**: Foreign key to users table

### Votes
- **user_id**: Foreign key to users (composite primary key)
- **post_id**: Foreign key to posts (composite primary key)

## 🔐 Authentication System

The API uses JWT (JSON Web Tokens) for authentication:
- Passwords are hashed using bcrypt
- JWT tokens expire based on configuration
- Protected routes require valid bearer tokens
- User context is automatically injected into protected endpoints

## 📡 API Endpoints

### Authentication (`/auth`)
- **POST /login** - User login and token generation

### Users (`/users`)
- **POST /** - Create new user
- **GET /{id}** - Get user by ID

### Posts (`/posts`)
- **GET /** - Get all posts (with pagination and search)
- **POST /** - Create new post (authenticated)
- **GET /{id}** - Get specific post with vote count
- **PUT /{id}** - Update post (owner only)
- **DELETE /{id}** - Delete post (owner only)

### Votes (`/vote`)
- **POST /** - Vote/unvote on a post (authenticated)

### Root
- **GET /** - Health check endpoint

## 🔧 Features

### Post Management
- Create, read, update, delete posts
- Pagination support (limit, skip)
- Search functionality by title
- Vote count aggregation
- Owner-based permissions

### User System
- Secure user registration
- Email validation
- Password hashing
- User profile retrieval

### Voting System
- Upvote/downvote functionality
- Prevent duplicate voting
- Real-time vote counting
- Cascade deletion on post/user removal

### Security
- JWT-based authentication
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention through ORM
- Authorization checks for resource ownership

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Environment variables configured

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd learn-backend-course
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables in `.env`:
```env
DATABASE_hostname=localhost
DATABASE_port=5432
DATABASE_name=your_db_name
DATABASE_user=your_db_user
DATABASE_password=your_db_password
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=30
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload
```

## 🧪 Testing

The API can be tested using:
- FastAPI's automatic documentation at `/docs`
- HTTP clients like Postman or curl
- The provided httpx client for integration tests

## 📊 API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🚀 Deployment

The application is configured for deployment on Heroku:
- Uses Gunicorn through Procfile
- Environment variables configured through Heroku config vars
- PostgreSQL database through Heroku Postgres

## 🔄 Database Migrations

Alembic is used for database version control:
- Create new migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Downgrade: `alembic downgrade -1`

## 🚀 CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline using GitHub Actions that automates testing and deployment to Heroku.

### Pipeline Features

#### CI Pipeline (`.github/workflows/ci.yml`)
- **Code Quality**: Black formatting, isort import sorting, flake8 linting
- **Security**: Bandit security scanning, Safety dependency checks
- **Testing**: Automated test execution with PostgreSQL
- **API Health Checks**: Endpoint validation

#### Deployment Pipeline (`.github/workflows/deploy.yml`)
- **Automated Testing**: Runs tests before deployment
- **Alembic Migration Detection**: Automatically detects model/migration changes
- **Smart Migration Execution**: Only runs migrations when changes are detected
- **Heroku Deployment**: Automatic deployment to Heroku on main branch pushes

### Setup Instructions

#### 1. GitHub Secrets
Add these secrets to your GitHub repository:

```
HEROKU_API_KEY=your_heroku_api_key
HEROKU_APP_NAME=backend-tutorial-sahil-ab3c3398e7b9
HEROKU_EMAIL=your_heroku_email
```

#### 2. Get Heroku API Key
```bash
heroku login
heroku auth:token
```

#### 3. Pipeline Triggers
- **Push to main**: Full CI + deployment to Heroku
- **Pull requests**: CI testing only
- **Push to develop**: CI testing only

#### 4. Alembic Migration Automation
The pipeline automatically:
- Detects changes in `alembic/versions/` or `app/models.py`
- Runs `alembic upgrade head` on Heroku if migrations are found
- Skips migration step if no changes detected

### Development Workflow

1. **Create Feature Branch**
```bash
git checkout -b feature/new-feature
```

2. **Make Changes** (including models if needed)
```bash
# If you changed models:
alembic revision --autogenerate -m "Add new feature"
```

3. **Test Locally**
```bash
alembic upgrade head
uvicorn app.main:app --reload
```

4. **Push and Deploy**
```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
# Create pull request
# After merge, automatic deployment to Heroku
```

### Pipeline Monitoring

- **GitHub Actions**: Check Actions tab in GitHub repository
- **Deployment Status**: Automatic notifications on success/failure
- **Migration Logs**: Available in GitHub Actions run logs

### Local Development Dependencies

Install development dependencies for local testing:
```bash
pip install -r requirements-dev.txt
```

This includes:
- `black` - Code formatting
- `isort` - Import sorting  
- `flake8` - Linting
- `bandit` - Security scanning
- `safety` - Dependency security
- `pytest` - Testing framework

## 🤝 Contributing

This project serves as a learning resource for backend development concepts including:
- RESTful API design
- Database modeling and relationships
- Authentication and authorization
- Modern Python web development
- Deployment strategies

## 📝 License

This project is licensed under the MIT License.
