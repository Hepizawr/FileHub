# FileHub

**FileHub** is a file management web application that allows users to store, manage, and retrieve files securely. The application includes an admin dashboard, user roles, and an intuitive interface for browsing and downloading files. Built with Flask, SQLAlchemy, and SQLite, FileHub is designed for scalability and easy deployment.

## Features

- **User Registration and Authentication**: Users can sign up, log in, and reset their passwords securely.
- **Admin Management**: Admin users have elevated privileges, allowing them to manage user accounts, view all uploaded files, and delete files if necessary.
- **File Upload and Download**: Users can upload files, organize them, and download files on demand.
- **Search and Filter**: Search files by name and format for quick and easy access.
- **Download Tracking**: Tracks file download counts to keep a record of file popularity.
- **Pagination**: Paginated file lists for efficient browsing, especially for large datasets.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Hepizawr/FileHub.git
    cd FileHub
    ```

2. **Set up a virtual environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

1. **Initialize the database**:

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

2. **Create a superuser**:

    To create an admin user with elevated privileges, run:

    ```bash
    flask admin createsuperuser
    ```

    You will be prompted to enter a username and password for the superuser account.

## Running the Application

To start the development server:

```bash
flask run

Open a web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the application.
