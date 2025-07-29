Django Todo App - Dockerized with Celery & SMTP4Dev
This project is a Django application that is containerized using Docker and uses Celery for asynchronous/background task processing and SMTP4Dev for testing email functionality.
📦 Tech Stack

Python 3.12
Django
Celery
Docker
SMTP4Dev
pipenv

🚀 Getting Started
Prerequisites
Make sure you have the following installed:

Docker
Docker Compose

Installation

Clone the Repository
git clone https://github.com/your-username/django-todo-app.git
cd django-todo-app


Set Up Environment Variables
Create a .env file in the project root and configure the following variables:
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://redis:6379/0
EMAIL_HOST=smtp
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False

Replace your-secret-key with a secure Django secret key. For production, ensure DEBUG=False and use a proper database URL (e.g., for PostgreSQL).

Run the Application
Build and start the Docker containers:
docker-compose up --build

This command will:

Build the Django application container.
Start the Django development server on port 8000.
Start the Celery worker and beat services.
Start the SMTP4Dev service for email testing, accessible at http://localhost:8025.


Access the Application

Web Application: Open http://localhost:8000 in your browser.
SMTP4Dev Web UI: Open http://localhost:8025 to view emails sent during testing.


Apply Database Migrations
If your Django app requires migrations, run:
docker-compose exec app python manage.py migrate


Create a Superuser (Optional)
To access the Django admin interface, create a superuser:
docker-compose exec app python manage.py createsuperuser



🛠️ Project Structure

Dockerfile: Defines the Docker image for the Django application.
docker-compose.yml: Configures the services (Django app, Celery worker, Celery beat, SMTP4Dev).
Pipfile & Pipfile.lock: Manage Python dependencies using pipenv.
manage.py: Django's command-line utility for administrative tasks.
todo_app/: Your Django project directory (replace todo_app with your actual project name).

⚙️ Services

app: Runs the Django development server.
celery-worker: Handles asynchronous tasks using Celery.
celery-beat: Schedules periodic tasks using Celery Beat.
smtp: Runs SMTP4Dev for capturing and inspecting emails during development.

📧 Email Testing with SMTP4Dev
SMTP4Dev is a dummy SMTP server for testing email functionality. It captures emails sent by the application without delivering them to real recipients. Access the SMTP4Dev web interface at http://localhost:8025 to view captured emails.
🛑 Stopping the Application
To stop the running containers:
docker-compose down

To stop and remove containers, networks, and volumes:
docker-compose down -v

🧪 Running Tests
To run your Django app's tests:
docker-compose exec app python manage.py test

🔧 Troubleshooting

Container Fails to Start: Check logs with docker-compose logs <service> (e.g., app, celery-worker, smtp).
Port Conflicts: Ensure ports 8000, 8025, and 1025 are free.
Celery Tasks Not Running: Verify CELERY_BROKER_URL in the .env file and ensure Redis is running (if used as the broker).
Email Issues:  Confirm the SMTP settings in the .env file and check the SMTP4Dev web UI. Also, ensure that the EMAIL_HOST variable is set to the name of the SMTP4Dev container (typically smtp).


📄 License
This project is licensed under the MIT License. See the LICENSE file for details.