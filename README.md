# Flask User Authentication App

This Flask web application serves as a template for creating web applications with already implemented login, signup, and logout functionality. It utilizes Flask for the web framework, MongoDB for database management, and Flask-Login for user authentication.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features

-   User signup with email, username, and password
-   User login with username and password
-   User logout
-   Session management with Flask-Login
-   Passwords hashed using bcrypt for security
-   MongoDB integration for user data storage
-   Simple template structure for easy customization

## Installation

1.  **Clone the repository:**
    
    
    `git clone https://github.com/yourusername/your-repository.git` 
    
2.  **Install dependencies:**
    
    
    `pip install -r requirements.txt` 
    
3.  **Set up MongoDB:**
    
    -   Install MongoDB on your system if not already installed.
    -   Create a MongoDB database and update the `MONGO_URI` in `config.py` with your database URI.

## Usage

1.  **Run the Flask app:**
        
    `python app.py` 
    
    The app will be running at `http://localhost:5000`.
    
2.  **Access the following routes:**
    
    -   `/`: Home page
    -   `/signup`: User signup page
    -   `/login`: User login page
    -   `/account`: Account page (accessible only to logged-in users)
    -   `/logout`: Log out the current user
