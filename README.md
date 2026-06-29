# 🎟️ Event Exhibition Badge Management System

A Django-based web application for managing exhibitor badges, visitor registrations, invitations, and bulk attendee uploads for exhibitions and events.

## 🚀 Features

### 👤 Exhibitor Authentication
- Secure exhibitor login
- Session-based authentication
- Dashboard access for authorized exhibitors

### 🎫 Badge Management
- Create badges
- Edit badge details
- Delete badges
- Badge ID generation
- Badge allocation tracking

### 📧 Invitation Management
- Send visitor invitations
- Generate unique invitation links
- Visitor registration through invitation links
- Invitation status tracking (Pending / Confirmed)

### 📊 Dashboard
- Total allocated badges
- Invited visitors count
- Confirmed registrations
- Available badge balance
- Ticket-wise summary

### 📁 Bulk Upload
- Upload attendee data using Excel
- Excel validation
- Invalid row detection
- Column mapping
- Preview uploaded data
- Bulk delete uploaded records
- Exhibitor-specific uploaded records

### 👥 Visitor Registration
- Register through invitation links
- Automatic badge assignment
- Badge ID generation
- Terms acceptance

### 🛠️ Admin Panel
- Manage exhibitors
- Manage badges
- Manage invitations
- Manage uploaded records
- Allocate badges to exhibitors

---

# 🛠 Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript
- jQuery
- Axios

### Database
- SQLite

### Deployment
- PythonAnywhere

---

# 📂 Project Structure

```
Event_Exhibition/
│
├── Event_Exhibition/
│
├── Event_Exhibition_App/
│
├── templates/
│
├── img/
│
├── staticfiles/
│
├── manage.py
│
└── requirements.txt
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/nidheesh146/Event-Exhibitor-System.git

cd Event-Exhibitor-System
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Run Server

```bash
python manage.py runserver
```

---

# 🌐 Application URLs

| URL | Description |
|------|-------------|
| `/admin/` | Django Admin |
| `/exhibitor-login-page/` | Exhibitor Login |
| `/register/<token>/` | Visitor Registration |
| `/dashboard/` | Dashboard API |

---

# 📈 Workflow

### Invitation Flow

```
Admin
     ↓
Create Exhibitor
     ↓
Exhibitor Login
     ↓
Send Invitation
     ↓
Visitor Opens Link
     ↓
Visitor Registers
     ↓
Badge Created
     ↓
Dashboard Updated
```

### Bulk Upload Flow

```
Login
   ↓
Upload Excel
   ↓
Validate Records
   ↓
Column Mapping
   ↓
Preview Data
   ↓
Save Records
   ↓
Dashboard Updated
```

---

# 🔐 Authentication

- Django Authentication
- Session Authentication
- CSRF Protection

---

# 📊 Dashboard Metrics

- Allocated Badges
- Invited Visitors
- Confirmed Registrations
- Available Badge Balance
- Ticket Summary

---

# 🚀 Deployment

The application is deployed on **PythonAnywhere**.

---

# 📌 Future Improvements

- Email Integration
- QR Code Badge Generation
- PDF Badge Printing
- Excel Export
- Analytics Dashboard
- Role-Based Access Control
- PostgreSQL Support

---


Python | Django | REST API Developer

GitHub: https://github.com/nidheesh146
