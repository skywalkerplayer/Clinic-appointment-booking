# AI Appointment Assistant

A lightweight AI-powered appointment assistant built with **Python, NiceGUI, and LLMs**.

The application provides a conversational interface for patients to make and manage appointments, with a separate admin interface for managing scheduled appointments.

## Demo

https://github.com/user-attachments/assets/ab0ea7b1-08e2-4542-891d-42382539d3dc



The demo shows:

* Conversational appointment booking
* Appointment confirmation
* Appointment management
* Admin interface
* Rescheduling and deleting appointments

## Features

### Patient Interface

* Chat-based appointment booking
* Natural-language interaction with the AI assistant
* Appointment availability checking
* Appointment confirmation

### Admin Interface

* View existing appointments
* Filter appointments by doctor or status
* Reschedule appointments
* Delete appointments

## Architecture

```text
┌─────────────────────┐
│      NiceGUI        │
│    Web Interface    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Python Backend    │
│                     │
│ Appointment Logic   │
│ LLM Integration     │
└──────────┬──────────┘
           │
           ├──────────────► LLM
           │
           ▼
┌─────────────────────┐
│       SQLite        │
│    Appointments     │
└─────────────────────┘
```

## Tech Stack

* **Python**
* **NiceGUI**
* **SQLite**
* **LLM / LLM API**
* **HTML / CSS / Tailwind CSS**

## Getting Started

### Requirements

* Python 3.10+
* An LLM service/API

### Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your LLM settings as required by the project.

Start the application:

```bash
python main.py
```

The application will be available at:

```text
http://localhost:8080
```

To make the application accessible from other devices on the local network:

```python
ui.run(host="0.0.0.0", port=8080)
```

## Project Structure

```text
.
├── main.py
├── database.py
├── llm_service.py
├── config_manager.py
├── requirements.txt
└── README.md
```

## Why I Built This

This project explores how an LLM can be integrated with a traditional transactional application.

Instead of allowing the LLM to directly modify the database, the assistant interprets the user's request and invokes application-level appointment operations. This keeps business logic and data access under the control of the backend.

## Future Improvements

* Authentication and role-based access control
* Doctor availability management
* Appointment conflict detection
* Persistent conversation history
* Streaming LLM responses
* Email/SMS appointment notifications
* Production deployment with HTTPS
