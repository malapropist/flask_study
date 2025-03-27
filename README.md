
# Bible Study Note Taking Web App

This is a Flask web application that allows users to take and organize notes while studying the Bible. Users can create accounts, log in securely, and maintain their personal collection of Bible study notes with verse references.

## Features

- User authentication (signup, login, logout)
- Create, view and delete notes
- Associate notes with specific Bible verses
- Secure password hashing
- Personal note dashboard for each user

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   ```python
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
   ```
   .\venv\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source venv/bin/activate
   ```
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```
5. Initialize the database:
   ```
   python init_db.py
   ```
6. Run the application:
   ```
   python main.py
   ```
7. Open a web browser and navigate to `http://localhost:5000`


