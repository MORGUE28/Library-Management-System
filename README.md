# Library Management System (LMS) FastAPI Application

## Introduction
This FastAPI application, named LMSAPI, serves as a simple Library Management System. It allows users to perform various operations such as adding books, adding users, checking out books, viewing borrowed books by a user, and more. The application uses SQLAlchemy for database management, FastAPI for creating APIs, and Pandas for handling CSV data.

## Project Structure
- **LMSAPI.py:** Main Python script containing the FastAPI application, database models, and API endpoints.
- **Dockerfile:** Docker configuration file to containerize the application.
- **requirements.txt:** List of Python packages required for the application.
- **library.db:** SQLite database file.
- **library.csv:** CSV file to store library data.

## Getting Started

### Prerequisites
- Docker installed on your machine
- Python 3.11 or higher

### Setup
1. Clone the repository: `git clone https://github.com/your_username/LMSAPI.git`
2. Navigate to the project directory: `cd LMSAPI`

### Running the Application
#### Using Docker
```bash
docker build -t lmsapi .
docker run -p 80:80 lmsapi
```
The application will be accessible at [http://localhost:80](http://localhost:80).

### Docker Image link : `https://hub.docker.com/r/morgue28/lmsimage`
## API Endpoints
### 1. Create a Book
- **Endpoint:** `/books/` (POST)
- **Parameters:**
  - `title` (str): Title of the book.
  - `author` (str): Author of the book.

### 2. Create a User
- **Endpoint:** `/users/` (POST)
- **Parameters:**
  - `name` (str): Name of the user.

### 3. Remove a Book
- **Endpoint:** `/books/{book_id}` (DELETE)
- **Path Parameters:**
  - `book_id` (int): ID of the book to be deleted.

### 4. Modify Book Details
- **Endpoint:** `/books/{book_id}` (PUT)
- **Path Parameters:**
  - `book_id` (int): ID of the book to be modified.
- **Parameters:**
  - `title` (str, optional): New title of the book.
  - `author` (str, optional): New author of the book.

### 5. View All Books
- **Endpoint:** `/books/` (GET)

### 6. Check Out a Book
- **Endpoint:** `/books/{book_id}/checkout/{user_id}` (POST)
- **Path Parameters:**
  - `book_id` (int): ID of the book to be checked out.
  - `user_id` (int): ID of the user checking out the book.

### 7. Get Checked Out Users
- **Endpoint:** `/checked-out-users/` (GET)

### 8. Get Borrowed Books by User
- **Endpoint:** `/users/{user_id}/borrowed-books/` (GET)
- **Path Parameters:**
  - `user_id` (int): ID of the user.

## Additional Information
- The SQLite database file (`library.db`) stores book and user information.
- Book data is also saved to a CSV file (`library.csv`) for backup and easy retrieval.
- The application provides Swagger documentation at the root URL [http://localhost:80/](http://localhost:80/).

Feel free to explore the API endpoints and customize the application according to your requirements.

#Screenshots:
