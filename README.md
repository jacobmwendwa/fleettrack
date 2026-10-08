# FleetTrack 🚗

A simple web-based **Fleet Tracking and Monitoring System** built with Django and PostgreSQL.

FleetTrack is a learning and practical project designed to demonstrate how a fleet management system can be developed, deployed, and maintained using modern web technologies.

## 🌐 Live System

**FleetTrack:**
https://fleettrack-e1bn.onrender.com

**Django Administration:**
https://fleettrack-e1bn.onrender.com/admin/

## 📌 Project Overview

FleetTrack provides a simple platform for managing and monitoring fleet-related information.

The system demonstrates basic functionality such as:

* User registration and login
* User authentication
* Fleet dashboard
* Vehicle monitoring
* Vehicle status information
* Alerts and monitoring information
* Task management
* Django administration

The project was intentionally kept simple to make it suitable for learning, testing, and demonstrating the basic concepts of a fleet tracking application.

## 🎯 Project Objectives

The main objectives of FleetTrack are to:

1. Demonstrate development of a Django web application.
2. Implement user authentication and authorization.
3. Create a simple fleet monitoring dashboard.
4. Work with a relational PostgreSQL database.
5. Deploy a Django application to the cloud.
6. Practice Git and GitHub version control.
7. Provide a foundation that can be expanded with additional fleet-management features in the future.

## 🛠️ Technologies Used

| Technology    | Purpose                       |
| ------------- | ----------------------------- |
| Python 3.12.4 | Programming language          |
| Django 5.0.6  | Web framework                 |
| PostgreSQL    | Production database           |
| SQLite        | Local development database    |
| Gunicorn      | Production application server |
| WhiteNoise    | Static file serving           |
| Git           | Version control               |
| GitHub        | Source code repository        |
| Render        | Cloud deployment              |

## 📂 Project Structure

```text
fleettrack/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   └── urls.py
│
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt
├── build.sh
├── .python-version
└── README.md
```

## 🔐 Authentication

FleetTrack uses Django's built-in authentication system.

Users can:

* Register an account
* Log in
* Access authenticated pages
* Log out
* Use the Django administration interface where authorized

The production system also contains a Django superuser for administrative management.

## 📊 Dashboard

The FleetTrack dashboard provides a simple overview of fleet activity.

The dashboard displays information such as:

* Total vehicles
* Active vehicles
* Offline vehicles
* Active alerts

The dashboard is designed to provide a quick overview of the current fleet situation.

## 🚘 Fleet Monitoring

The system provides basic fleet monitoring functionality.

The current version focuses on the essential concepts required for a fleet tracking application rather than implementing advanced GPS or telematics functionality.

Future versions can introduce additional monitoring capabilities as the project develops.

## 🗄️ Database

### Local Development

SQLite is used during local development for simplicity.

### Production

The deployed application uses **PostgreSQL**.

Database configuration is handled through environment variables rather than storing database credentials directly in the source code.

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/jacobmwendwa/fleettrack.git
```

### 2. Enter the project directory

```bash
cd fleettrack
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

On Windows:

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

## ☁️ Deployment

FleetTrack is deployed using **Render**.

The production deployment uses:

* Python 3.12.4
* Django 5.0.6
* PostgreSQL
* Gunicorn
* WhiteNoise

The application is configured to use environment variables for production settings and sensitive configuration.

## 🔑 Environment Variables

Production configuration is stored using environment variables.

Examples include:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
ALLOWED_HOSTS
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
RENDER
```

### Security Notice

**Never commit passwords, secret keys, database credentials, API keys, or other sensitive information to GitHub.**

Sensitive production values are stored in the Render environment rather than in the public repository.

## 🔧 Build Command

The production build uses:

```bash
./build.sh
```

The build process installs dependencies, collects static files, and applies database migrations.

## ▶️ Start Command

The production server runs using Gunicorn:

```bash
gunicorn mysite.wsgi:application
```

## 📈 Future Improvements

FleetTrack Version 1.0 focuses on basic functionality.

Possible future improvements include:

* GPS location tracking
* Interactive maps
* Vehicle trip history
* Driver management
* Maintenance records
* Fuel monitoring
* More detailed alerts
* Reports and analytics
* Customer/CRM functionality
* Improved mobile responsiveness
* Advanced fleet monitoring

These features can be added gradually after the basic system has been fully tested.

## 📚 Learning Purpose

This project was developed as a practical learning project covering:

* Python programming
* Django development
* Database management
* Authentication
* HTML and CSS
* Git and GitHub
* PostgreSQL
* Cloud deployment
* Environment configuration
* Basic production troubleshooting

## 👨‍💻 Author

**Jacob Mwendwa Musyoki**

FleetTrack was developed as a practical learning and portfolio project.

## 📄 License

This project is currently provided for learning and demonstration purposes.

---

### FleetTrack Version 1.0

**Django • PostgreSQL • GitHub • Render**
