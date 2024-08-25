# Django Ollama Property Rewriter

A Django CLI application that rewrites property information using Ollama, an open-source large language model.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Database Schema](#database-schema)
9. [Contributing](#contributing)
10. [License](#license)

## Project Overview

This Django CLI application is designed to rewrite property information stored in a database using Ollama. It reads property titles and descriptions, uses Ollama to generate improved versions, and stores the results back in the database. Additionally, it generates and stores summaries for each property.

## Features

- Rewrite property titles and descriptions using Ollama
- Generate property summaries
- Store updated information and summaries in PostgreSQL database
- Django CLI command for easy execution

## Prerequisites

- Python 3.x
- PostgreSQL
- Django
- Ollama (installed and running on your system)
- Django_assignment project set up and running

## Project Structure

```
root/
├── django-ollama-rewriter/
│   ├── cliApplication/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── llmApp/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── rewrite_property_info.py
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── .gitignore
│   ├── config.py
│   ├── manage.py
│   ├── README.md
│   └── requirements.txt
└── djangoAssignment/
```

## Installation

Before proceeding with the installation of this project, please make sure you have already set up and run the `Django_assignment` project.
GitHub repository: https://github.com/noman1811048/djangoAssignment.git

1. Clone the repository:
   ```
   git clone https://github.com/noman1811048/django-ollama-rewriter.git
   cd django-ollama-rewriter
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database and update the `config.py` file with your database credentials.

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Install and start Ollama:
   - Follow the instructions at [Ollama's official website](https://ollama.ai/download) to install Ollama on your system.

7. Pull the required model (e.g., gemma2:2b):
   ```
   ollama pull gemma2:2b
   ```

## Configuration

1. Create a `config.py` file in the root directory with the following content:

   ```python
   DB_NAME = 'your_database_name'  # This should refer to the database name that was previously configured for the Django project.
   DB_USER = 'your_database_user'
   DB_PASSWORD = 'your_database_password'
   DB_HOST = 'localhost'
   DB_PORT = 'PORT'
   ```

2. Ensure Ollama is installed and running on your system.

## Usage

1. Ensure Ollama is running:
   ```
   ollama run gemma2:2b
   ```

2. Run the property rewriter command:
   ```
   python manage.py rewrite_properties
   ```
   
   This command will:
   * Rewrite the title and description of each property in the database
   * Generate a summary for each property
   * Save the updated information and new summaries to the database

3. Create a superuser (Admin user):
   ```
   python manage.py createsuperuser
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`

6. Access the admin panel at `http://127.0.0.1:8000/admin/`

## Database Schema

The project uses two main models:

1. `Property` model (existing)
   - Fields: id, title, description, etc.

2. `PropertySummary` model (new)
   - Fields:
     - property (ForeignKey to Property)
     - summary (TextField)

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License
Copyright (c) 2024 Asadullah Al Noman