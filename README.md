---

# Django Property Rewriter and Summarizer

## Overview

This Django application provides a CLI command to rewrite property titles and descriptions and generate summaries using the Ollama API. It leverages Django ORM for database interactions and PostgreSQL for data storage.

## Prerequisites

- Python 3.x
- Django 4.x
- PostgreSQL
- Ollama API access
- `requests` library for API calls

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/noman1811048/django-ollama-rewriter.git
   cd django-ollama-rewriter
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**

   Ensure PostgreSQL is running and create a database named `properties` (or your preferred name).

5. **Update Django Settings**

   Edit `cliApplication/settings.py` to configure your PostgreSQL database:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'LLM_DBNAME',
           'USER': 'DB_USERNAME',
           'PASSWORD': 'DB_PASSWORD',
           'HOST': 'DB_HOST',
           'PORT': 'DB_PORT',
       },
       'django_db': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'DJANGO_DBNAME',
           'USER': 'DB_USERNAME',
           'PASSWORD': 'DB_PASSWORD',
           'HOST': 'DB_HOST',
           'PORT': 'DB_PORT',
       }
   }
   ```

6. **Set Up Ollama API**

   Obtain your Ollama API key and update the `your_app/management/commands/sync_database_properties.py` file with your API key:

   ```python
   OLLAMA_API_KEY = 'your_ollama_api_key'
   ```

## Usage

1. **Apply Migrations**

   Apply the initial migrations to set up the database schema:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Run the CLI Command**

   To rewrite property titles and descriptions and generate summaries, run:

   ```bash
   python manage.py sync_database_properties
   ```

   This command will:
   - Rewrite the title and description of each property using the Ollama API.
   - Update the `Property` table with the rewritten information.
   - Generate a summary for each property and save it in the `PropertySummary` table.

## Code Structure

- **`your_app/models.py`**: Contains the Django models for `Property` and `PropertySummary`.
- **`your_app/management/commands/sync_database_properties.py`**: Contains the custom Django management command for rewriting and summarizing property information.
- **`requirements.txt`**: Lists the Python packages required for the project.

## Requirements

Add the following to your `requirements.txt`:

```plaintext
Django>=4.0
psycopg2-binary
requests
```

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that your code adheres to the existing coding standards and includes tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
---
