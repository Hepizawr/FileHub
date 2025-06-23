# FileHub

**FileHub** is a file-sharing web application designed to facilitate secure file management and access. The system includes two types of users: regular users and administrators, each with different access levels and functionalities. 

## Features

- **User Registration and Authentication**: Users can sign up and log in securely, with hashed passwords ensuring data protection.
- **Admin Management**: Admin users have elevated privileges, allowing them to manage user accounts, view all uploaded files, and delete files if necessary.
- **File Upload and Download**: Admins can upload files, organize them, and download files on demand.
- **Search and Filter**: Search files by name and format for quick and easy access.
- **Download Tracking**: Tracks file download counts to keep a record of file popularity.
- **File Download Logging**: Each download by a user is logged, recording the user’s name, file, and download timestamp.
- **User Activity Statistics**: Admins can monitor each user's file download statistics, via the admin dashboard.
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
    flask --app "app:create_app()" admin createsuperuser
    ```

    You will be prompted to enter a username and password for the superuser account.

## Running the Application

To start the development server:

```bash
flask run
```

Open a web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the application.
