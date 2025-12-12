# 🏥 COM7033 — Patient Management System


A comprehensive **Flask-based Patient Management System** developed for the COM7033 assignment at Leeds Trinity University. This application enables healthcare professionals to manage patient records, track allergies, and conduct health assessments with role-based access control. 

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [User Roles & Permissions](#-user-roles--permissions)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- **User Authentication** — Secure login and registration system with password validation
- **Patient Management** — Full CRUD operations for patient records
- **Allergy Tracking** — Record and manage patient allergies with severity levels
- **Health Assessments** — Comprehensive health assessment tracking including: 
  - Hypertension status
  - Marital status
  - Work type classification
  - Residence type
  - Average glucose levels
  - BMI tracking
  - Smoking status
  - Stroke risk assessment

### Security Features
- CSRF protection using Flask-WTF
- Password strength validation (8+ characters with uppercase, lowercase, digit, and special character)
- Session-based authentication
- Role-based access control (RBAC)

### User Interface
- Responsive HTML templates
- Flash messaging for user feedback
- Custom 404 error page
- Clean navigation with base template inheritance

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Backend Framework** | Flask 3.1.2 |
| **Relational Database** | SQLite / SQLAlchemy 2.0.44 |
| **NoSQL Database** | MongoDB (PyMongo 4.10.1) |
| **Template Engine** | Jinja2 3.1.6 |
| **Form Handling** | Flask-WTF 1.2.2, WTForms 3.2.1 |
| **Authentication** | PyJWT 2.10.1, PyOTP 2.9.0 |
| **Security** | Werkzeug 3.1.4 |
| **Environment** | python-dotenv 1.2.1 |

---

## 📁 Project Structure

```
com7033-assignment-surajyawnumah/
├── app.py                    # Main Flask application entry point
├── config.py                 # Application configuration settings
├── init_db.py                # Database initialization script
├── seed_db.py                # Database seeding utility
├── seeded_dataset.csv        # Sample dataset for seeding
├── requirements.txt          # Python dependencies
├── test. py                   # Test suite
├── models/                   # Data models
│   ├── user.py               # User model (SQLAlchemy)
│   ├── patient.py            # Patient model (SQLAlchemy)
│   └── mongo/                # MongoDB models
│       ├── allergy_model.py  # Allergy model
│       └── assessment_model.py # Assessment model
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base template with common layout
│   ├── home.html             # Landing page
│   ├── about.html            # About page
│   ├── login.html            # User login form
│   ├── register.html         # User registration form
│   ├── patient_management.html # Patient dashboard
│   ├── edit_patient.html     # Patient edit view with allergies/assessments
│   ├── flash. html            # Flash message component
│   └── 404.html              # Custom error page
└── utils/                    # Utility modules
    ├── decorators.py         # Auth decorators (@auth_required, @admin_required, @doctor_required)
    ├── patient_utils.py      # Patient validation helpers
    └── mongo_validation.py   # MongoDB data validation
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed: 

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **pip** — Python package manager (included with Python)
- **MongoDB** — [Download MongoDB](https://www.mongodb.com/try/download/community) (for allergy and assessment data)
- **Git** — [Download Git](https://git-scm. com/downloads)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/CS-LTU/com7033-assignment-surajyawnumah. git
cd com7033-assignment-surajyawnumah
```

### 2. Create a Virtual Environment

**macOS / Linux:**
```bash
python -m venv . venv
source . venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
. \. venv\Scripts\Activate. ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate. bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (recommended for secrets):

```env
SECRET_KEY=your-super-secret-key-here
MONGO_URI=mongodb://localhost:27017/patient_management
DATABASE_URL=sqlite: ///patients.db
DEBUG=True
```

### Configuration File

Review and modify `config.py` as needed:

```python
class Config:
    SECRET_KEY = os. environ.get('SECRET_KEY') or 'your-fallback-secret-key'
    MONGO_URI = os. environ.get('MONGO_URI') or 'mongodb://localhost:27017/patient_db'
    # Additional configuration options...
```

> ⚠️ **Security Note:** Never commit secrets to version control.  Use environment variables for sensitive data.

---

## 🗄 Database Setup

### 1. Start MongoDB

Ensure MongoDB is running on your system:

```bash
# macOS (Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows
net start MongoDB
```

### 2. Initialize the Relational Database

```bash
python init_db.py
```

This creates the SQLite database schema with the required tables for users and patients.

### 3. Seed the Database (Optional)

Populate the database with sample data from `seeded_dataset.csv`:

```bash
python seed_db. py
```

---

## ▶️ Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at:  **http://127.0.0.1:8080**

### Production Deployment

For production, use a WSGI server like Gunicorn: 

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

---

## 🔌 API Endpoints

### Public Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page |
| `GET` | `/about` | About page |
| `GET/POST` | `/login` | User login |
| `GET/POST` | `/register` | User registration |
| `GET` | `/logout` | User logout |

### Protected Routes (Authentication Required)

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| `GET` | `/patient-management` | Patient dashboard | Any authenticated user |
| `POST` | `/add-patient` | Add new patient | Admin |
| `GET` | `/edit-patient/<id>` | View/edit patient details | Doctor |
| `POST` | `/update-patient/<id>` | Update patient info | Doctor |
| `POST` | `/delete-patient/<id>` | Delete patient | Admin |
| `POST` | `/add-allergy/<patient_id>` | Add patient allergy | Doctor |
| `POST` | `/update-allergy/<patient_id>/<allergy_id>` | Update allergy | Doctor |
| `POST` | `/delete-allergy/<patient_id>/<allergy_id>` | Delete allergy | Doctor |
| `POST` | `/add-assessment/<patient_id>` | Add health assessment | Doctor |

### Example API Calls

**Login:**
```bash
curl -i -c cookies.txt -X POST http://127.0.0.1:8080/login \
  -d "email=doctor@example.com" \
  -d "password=SecurePass123!"
```

**Register a New User:**
```bash
curl -i -X POST http://127.0.0.1:8080/register \
  -d "first_name=John" \
  -d "last_name=Doe" \
  -d "email=john.doe@example.com" \
  -d "password=SecurePass123!" \
  -d "confirm_password=SecurePass123!" \
  -d "role=doctor"
```

**Access Protected Route (with session cookie):**
```bash
curl -i -b cookies.txt http://127.0.0.1:8080/patient-management
```

---

## 👥 User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Admin** | Full access:  Add, edit, delete patients; manage all records |
| **Doctor** | View patients; edit patient details; manage allergies and assessments |
| **User** | View patient management dashboard |

### Role Decorators

The application uses custom decorators for access control:

- `@auth_required` — Requires any authenticated user
- `@admin_required` — Requires admin role
- `@doctor_required` — Requires doctor role

---

## 🧪 Testing

Run the test suite: 

```bash
python test.py
```

For more comprehensive testing with pytest:

```bash
pip install pytest pytest-cov
pytest test. py -v --cov=. 
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Database Connection Errors**
```bash
# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Check SQLite file permissions
ls -la *.db
```

**2. Module Not Found Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**3. Port Already in Use**
```bash
# Use a different port
python app.py  # Modify port in app.py, or: 
flask run --port 5001
```

**4. Virtual Environment Issues**
```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # or Windows equivalent
pip install -r requirements. txt
```


---

## 👤 Author

**Suraj Yawnumah**
- GitHub:  [@surajyawnumah](https://github.com/surajyawnumah)

---


## 🙏 Acknowledgments

- Leeds Trinity University — COM7033 Module
- Flask Documentation
- MongoDB Documentation
- SQLAlchemy Documentation

---


