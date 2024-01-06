Flask Movie Management App
Description

This Flask-based web application is designed for managing a movie collection. It integrates Flask-Bootstrap, Flask-WTF for form handling, and uses SQLite for the database. The app allows users to add, view, and manage movie details.
Features

    Movie Management: Add and view movie details.
    Form Handling: Utilizes Flask-WTF.
    Styling: Integrated with Flask-Bootstrap.

Installation

    Clone the Repository:
        git clone [repository-url]

Install Dependencies:

    pip install -r requirements.txt

    Database Setup:
        The app uses SQLite, managed by Flask-SQLAlchemy.

Usage

To run the application:

python main.py

Access the application at localhost:5000.

Important Note:

    The application includes a function to populate the database with dummy data for demonstration purposes. To use this feature, uncomment the function call in main.py. Remember to comment it back out after the initial data load to prevent duplicate entries.

Technologies Used

    Backend: Flask.
    Database: SQLite with Flask-SQLAlchemy.
    Frontend: Flask-Bootstrap.