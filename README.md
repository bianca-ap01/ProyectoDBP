Competitive Programming Club Application - 2023-1
Team Members
Bladimir Alferez
Bianca Aguinaga
Alvaro García
Mateo Llallire
Project Description
This project is a web application aimed at managing the data related to the Competitive Programming Club at our University. This includes registration of interested users, existing members, and club-related information.

Key Objectives
Public User Login: Develop a login mechanism for users who are neither club members nor part of the administrative team. This section will display information about getting started with competitive programming.

Club Member Login: Create a unique login for registered club members.

Admin Login: Establish an administrator login for club members who are part of the club administration. The administrative interface will provide functionalities like activating, deactivating, and deleting members, teams, and other resources.

Mission
To create an interactive web application that facilitates user registration, team creation, and contest management for the Competitive Programming Club.

Vision
This project is intended to serve as a beta version of a more comprehensive web application that will be developed for the Competitive Programming Club in the near future.

Additional Resources Used (Front-End, Back-End, Database)
Flask-Admin: Utilized for the creation and management of administrative interfaces.

Flask-Login: Used for handling user sessions. Includes functions that define accessible routes for users.

Werkzeug: Used for password encryption.

Execution (Script, Host, etc.)
Database:

Management System: PostgreSQL

sql
Copy code
    psql
    > CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    > create database "dbCPC";
    > \c dbCPC
Script:

Clone the Repository:

SSH: git clone git@github.com:bianca-ap01/ProyectoDBP.git
HTTPS: git clone https://github.com/bianca-ap01/ProyectoDBP.git
Create and Activate a Virtual Environment

bash
Copy code
    python -m venv env
    source env/bin/activate
Install Dependencies in the Virtual Environment
markdown
Copy code
    pip install -r requirements.txt
Run the Application
markdown
Copy code
    python server.py
Creating Tables

bash
Copy code
    export FLASK_APP=server.py
    flask shell
    > db.create_all()
    > db.session.commit()
    > exit
API, Requests, and Responses
The application uses HTTP requests to retrieve information submitted in forms.

Upcoming Implementation:

Codeforces API: Codeforces is one of the largest competitive programming platforms with a comprehensive API. This API can be used to validate user information, connect to existing problems, etc.

Error Handling
Successful and error cases are handled as follows:

200: Success
400: Form submission error
401: Incorrect password
404: Not Found
500: Server Error
Additional Notes
Feel free to contribute or report any issues you encounter while using this application. Your feedback is greatly appreciated.
