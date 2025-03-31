# Quizzie

Quizzie is a web-based quiz application that provides trivia questions in the subjects of Maths, English, and Science. It offers questions of varying difficulty levels: Easy, Intermediate, and Hard. The application is built using Flask, MySQL, HTML, CSS, and JavaScript.

## Features

- **User Registration and Login**: Users can create an account and log in to access the quizzes.
- **Session Management**: User sessions are managed using Flask-Session.
- **Database Integration**: MySQL is used to store user information and quiz scores.
- **Dynamic Quiz Pages**: Separate routes and templates for each subject and difficulty level.
- **Score Tracking**: Users can view and reset their scores for each quiz.
- **Timer Functionality**: Each quiz has a countdown timer based on its difficulty level.
- **Responsive Design**: The application uses Bootstrap for a user-friendly and responsive interface.

## Installation

### Prerequisites

- Python 3.10 or higher
- MySQL server
- A virtual environment (optional but recommended)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/quizzie.git
   cd quizzie
   ```

2. **Install Dependencies**:
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Create a MySQL database named `users` (or any name of your choice).
   - Update the database configuration in `app.py`:
     ```python
     app.config["MYSQL_HOST"] = "localhost"
     app.config["MYSQL_USER"] = "root"
     app.config["MYSQL_PASSWORD"] = ""
     app.config["MYSQL_DB"] = "users"
     ```
   - Run the following SQL command to create the `userr` table:
     ```sql
     CREATE TABLE userr (
         id INT PRIMARY KEY AUTO_INCREMENT,
         username TEXT,
         password TEXT,
         maths_easy INT DEFAULT 0,
         maths_intermediate INT DEFAULT 0,
         maths_hard INT DEFAULT 0,
         english_easy INT DEFAULT 0,
         english_intermediate INT DEFAULT 0,
         english_hard INT DEFAULT 0,
         science_easy INT DEFAULT 0,
         science_intermediate INT DEFAULT 0,
         science_hard INT DEFAULT 0
     );
     ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`.

## Usage

1. Open your browser and navigate to `http://localhost:5000`.
2. Register for an account or log in if you already have one.
3. Choose a subject and difficulty level from the home page.
4. Complete the quiz within the allotted time.
5. View your scores on the "Scores" page.
6. Reset your scores if needed.

## Project Structure

```
Quizzie/
├── app.py                  # Main Flask application
├── templates/              # HTML templates for the app
│   ├── layout.html         # Base layout for all pages
│   ├── index.html          # Home page
│   ├── register.html       # Registration page
│   ├── login.html          # Login page
│   ├── scores.html         # Scores page
│   ├── maths_easy.html     # Easy Maths quiz
│   ├── maths_intermediate.html  # Intermediate Maths quiz
│   ├── maths_hard.html     # Hard Maths quiz
│   ├── english_easy.html   # Easy English quiz
│   ├── english_intermediate.html  # Intermediate English quiz
│   ├── english_hard.html   # Hard English quiz
│   ├── science_easy.html   # Easy Science quiz
│   ├── science_intermediate.html  # Intermediate Science quiz
│   ├── science_hard.html   # Hard Science quiz
├── static/                 # Static files (CSS, JS, images)
│   ├── styles.css          # Custom styles
│   ├── js/
│   │   ├── score.js        # Timer and score submission logic
│   │   ├── reset_scores.js # Reset scores logic
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

## Technologies Used

- **Backend**: Flask, Flask-MySQLdb, Flask-Session
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (jQuery)
- **Database**: MySQL
- **Other Libraries**: NumPy, Pandas

## Future Enhancements

- Add more subjects and quizzes.
- Implement user profile pages.
- Add a leaderboard to compare scores with other users.
- Improve security by hashing passwords before storing them in the database.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
