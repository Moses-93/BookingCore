# BookingCore – Backend for the Booking System

## 📌 Project Description  
**BookingCore** is a backend server built with FastAPI, responsible for managing bookings, payments, and users in the **BookEasy** SaaS solution.

## ⚙️ Architecture  
The server follows **clean architecture** and **REST API** principles.  
Asynchronous processes handle business logic, while Redis and Celery ensure background task execution.

## 🔹 Key Features  
✅ Booking management and scheduling.  
✅ Payment and subscription processing.  
✅ Request caching for performance optimization.  
✅ Background tasks (reminders, booking deactivation, etc.).  

## 🛠️ Tech Stack  
- **FastAPI** – asynchronous backend framework.  
- **PostgreSQL** – database.  
- **Redis** – caching and message broker for Celery.  
- **Celery** – background task processing.  
- **boto3** – integration with AWS Secrets Manager.  
- **cryptography** – encryption of personal data.  
- **SQLAlchemy & Alembic** – ORM and database migrations.  

## 📢 Contact  
📩 If you have any questions, feel free to reach out via **Telegram** or email.  
