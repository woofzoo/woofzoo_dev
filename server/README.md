# 🐕 WoofZoo - Pet Management System

A comprehensive FastAPI-based pet management system with authentication, family management, photo storage, and more.

## 🚀 Features

### ✅ **Phase 1: Pet Profile System**
- **Pet Management**: Complete CRUD operations for pets
- **Owner Management**: Pet owner registration and management
- **Pet Types & Breeds**: Predefined lists with search functionality
- **Data Validation**: Comprehensive input validation and error handling

### ✅ **Phase 2: Family Management System**
- **Family Creation**: Create and manage pet families
- **Family Members**: Add and manage family members with access levels
- **Family Invitations**: Send and manage invitations with expiration
- **Role-Based Access**: Different access levels for family members

### ✅ **Phase 3: Photo Management & Storage System**
- **Photo Upload**: Secure file upload with AWS S3 integration
- **Image Processing**: Automatic image optimization and resizing
- **Pre-signed URLs**: Secure file access with temporary URLs
- **Primary Photo Management**: Set and manage primary pet photos

### ✅ **Phase 4: Authentication & Authorization System**
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Flexible permission system
- **Password Management**: Secure password hashing and reset
- **Email Verification**: Complete email verification workflow

### ✅ **Phase 5: Integration & Final Testing**
- **Protected Routes**: All endpoints secured with authentication
- **Cross-System Integration**: Complete system integration
- **Comprehensive Testing**: 200+ test cases covering all functionality
- **Error Handling**: Robust error handling and validation

## 🏗️ Architecture

### **Clean Architecture Pattern**
```
Routes → Controllers → Services → Repositories → Models
```

### **Technology Stack**
- **Framework**: FastAPI (Python 3.13+)
- **Database**: PostgreSQL (with SQLite for testing)
- **ORM**: SQLAlchemy (synchronous)
- **Authentication**: JWT with bcrypt password hashing
- **File Storage**: AWS S3 with pre-signed URLs
- **Image Processing**: Pillow (PIL)
- **Testing**: pytest with comprehensive test suite

### **Key Components**
- **Models**: SQLAlchemy ORM models with proper relationships
- **Schemas**: Pydantic models for request/response validation
- **Repositories**: Data access layer with database operations
- **Services**: Business logic layer with complex operations
- **Controllers**: HTTP request/response handling
- **Routes**: API endpoint definitions with dependency injection
- **Middleware**: Authentication and authorization middleware

## 📋 API Endpoints

### **Authentication** (`/api/auth/`)
- `POST /register` - User registration
- `POST /login` - User authentication
- `POST /refresh` - Token refresh
- `POST /logout` - User logout
- `GET /me` - Get current user
- `POST /password-reset-request` - Request password reset
- `POST /password-reset` - Reset password
- `POST /change-password` - Change password
- `POST /verify-email` - Verify email
- `POST /send-verification-email` - Send verification email

### **Pet Types** (`/api/pet-types/`)
- `GET /` - Get all pet types
- `GET /{type}/breeds` - Get breeds for pet type
- `GET /search/breeds` - Search breeds

### **Owners** (`/api/owners/`)
- `POST /` - Create owner
- `GET /` - Get all owners (paginated)
- `GET /{id}` - Get owner by ID
- `PUT /{id}` - Update owner
- `DELETE /{id}` - Delete owner

### **Pets** (`/api/pets/`)
- `POST /` - Create pet
- `GET /` - Get all pets (paginated)
- `GET /{id}` - Get pet by ID
- `PUT /{id}` - Update pet
- `DELETE /{id}` - Delete pet
- `GET /owner/{owner_id}` - Get pets by owner
- `GET /search/` - Search pets
- `POST /lookup` - Lookup pet by ID

### **Families** (`/api/families/`)
- `POST /` - Create family
- `GET /` - Get families by owner
- `GET /{id}` - Get family by ID
- `PUT /{id}` - Update family
- `DELETE /{id}` - Delete family
- `GET /search/` - Search families

### **Family Members** (`/api/family-members/`)
- `POST /` - Add family member
- `GET /` - Get family members
- `GET /{id}` - Get family member by ID
- `PUT /{id}` - Update family member
- `DELETE /{id}` - Remove family member

### **Family Invitations** (`/api/family-invitations/`)
- `POST /` - Create invitation
- `GET /` - Get invitations
- `GET /{id}` - Get invitation by ID
- `PUT /{id}` - Update invitation
- `DELETE /{id}` - Delete invitation
- `POST /{id}/accept` - Accept invitation
- `POST /{id}/decline` - Decline invitation

### **Photos** (`/api/photos/`)
- `POST /upload-request` - Create upload request
- `POST /` - Create photo record
- `GET /` - Get photos by pet
- `GET /{id}` - Get photo by ID
- `PUT /{id}` - Update photo
- `DELETE /{id}` - Delete photo
- `POST /{id}/hard-delete` - Hard delete photo
- `GET /{id}/download-url` - Get download URL
- `GET /pet/{pet_id}/primary` - Get primary photo
- `POST /pet/{pet_id}/primary/{photo_id}` - Set primary photo
- `GET /uploader/{uploaded_by}` - Get photos by uploader

## 🔧 Installation & Setup

### **Prerequisites**
- Python 3.13+
- PostgreSQL (or SQLite for development)
- AWS S3 account (for photo storage)
- Conda environment manager

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd woofzoo_dev/server
```

### **2. Set Up Environment**
```bash
# Create conda environment
conda create -n woofzoo python=3.13
conda activate woofzoo

# Install dependencies
pip install -r requirements.txt
```

### **3. Environment Configuration**
Create a `.env` file with the following variables:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost/woofzoo
TEST_DATABASE_URL=sqlite:///./test.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS S3
S3_BUCKET_NAME=your-bucket-name
S3_REGION=us-east-1
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS (optional)
MSG91_API_KEY=your-api-key
MSG91_TEMPLATE_ID=your-template-id
MSG91_SENDER_ID=your-sender-id

# Application Settings
PET_PHOTO_MAX_SIZE_MB=10
PET_PHOTO_ALLOWED_TYPES=["image/jpeg", "image/png", "image/webp"]
FAMILY_INVITATION_EXPIRE_DAYS=10
OTP_EXPIRE_MINUTES=10
OTP_MAX_ATTEMPTS=3
```

### **4. Database Setup**
```bash
# Run database migrations
alembic upgrade head

# For development (SQLite)
alembic upgrade head
```

### **5. Run the Application**
```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Testing

### **Run All Tests**
```bash
pytest
```

### **Run Specific Test Categories**
```bash
# Authentication tests
pytest tests/test_auth_system.py

# Pet management tests
pytest tests/test_pet_api.py

# Family management tests
pytest tests/test_family_api.py

# Photo management tests
pytest tests/test_photo_api.py

# Integration tests
pytest tests/test_integration.py

# Full system tests
pytest tests/test_full_system.py
```

### **Test Coverage**
- **Phase 1**: 61 tests ✅ (Pet Profile System)
- **Phase 2**: 48 tests ✅ (Family Management System)
- **Phase 3**: 25 tests ✅ (Photo Management & Storage System)
- **Phase 4**: 32 tests ✅ (Authentication & Authorization System)
- **Phase 5**: 20+ tests ✅ (Integration & Final Testing)
- **Total**: 200+ tests ✅

## 🔐 Security Features

### **Authentication & Authorization**
- JWT-based authentication with access and refresh tokens
- Role-based access control (RBAC)
- Secure password hashing with bcrypt
- Token expiration and validation
- Protected route middleware

### **Data Security**
- Input validation and sanitization
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CSRF protection
- Secure file upload validation

### **File Security**
- Pre-signed URLs for secure file access
- File type and size validation
- Image processing and optimization
- Secure S3 integration

## 📊 Database Schema

### **Core Tables**
- `users` - User accounts and authentication
- `owners` - Pet owners
- `pets` - Pet information
- `families` - Pet families
- `family_members` - Family member relationships
- `family_invitations` - Family invitations
- `photos` - Pet photos and metadata
- `otps` - One-time passwords for verification

### **Key Relationships**
- Users can have multiple owners
- Owners can have multiple pets
- Pets can belong to multiple families
- Families can have multiple members
- Photos are linked to pets and uploaders

## 🚀 Deployment

### **Docker Deployment**
```bash
# Build Docker image
docker build -t woofzoo .

# Run container
docker run -p 8000:8000 woofzoo
```

### **Production Considerations**
- Use PostgreSQL for production database
- Configure proper CORS settings
- Set up HTTPS with SSL certificates
- Configure AWS S3 for file storage
- Set up monitoring and logging
- Use environment variables for configuration
- Implement rate limiting
- Set up backup strategies

## 📝 API Documentation

Once the application is running, you can access:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the test cases for usage examples

## 🎯 Roadmap

### **Future Enhancements**
- [ ] Real-time notifications
- [ ] Mobile app integration
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Advanced search and filtering
- [ ] Social features and sharing
- [ ] Veterinary integration
- [ ] Pet health tracking
- [ ] Appointment scheduling
- [ ] Payment processing

---

**WoofZoo** - Making pet management simple and secure! 🐕✨
