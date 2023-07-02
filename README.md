# Quizzie

Quizzie is a web application that provides trivia questions in the subjects of maths, English, and science. It offers questions of varying difficulty levels, including easy, intermediate, and hard. The application is built using HTML, CSS (Bootstrap), JavaScript (jQuery), MySQL, and Python (Flask).

## Features

- User registration and login: Users can create an account and log in to access the quiz.
- Session management: The application manages user sessions to keep track of logged-in users.
- Database integration: The application uses a MySQL database to store user information and quiz scores.
- Subject-specific routes: There are separate routes for each subject and difficulty level to provide a seamless experience.
- Score tracking: The application allows users to submit and reset their scores for each quiz.
- User-friendly interface: The application utilizes Bootstrap CSS framework and jQuery to create an intuitive and visually appealing user interface.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/quizzie.git
   ```

2. Navigate to the project directory:

   ```bash
   cd quizzie
   ```

3. Install the required dependencies. It is recommended to use a virtual environment:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:

   - Create a new database named `users` (or choose an existing one).
   - Update the database configuration in the `app.py` file:

     ```python
     app.config["MYSQL_HOST"] = "localhost"
     app.config["MYSQL_USER"] = "root"
     app.config["MYSQL_PASSWORD"] = ""
     app.config["MYSQL_DB"] = "users"
     ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

- Open your web browser and go to `http://localhost:5000`.
- If you don't have an account, click on the "Register" link to create one. Fill in the required information and submit the form.
- If you already have an account, click on the "Login" link and enter your username and password.
- Once logged in, you will be redirected to the home page where you can choose the subject and difficulty level of the quiz you want to attempt.
- After completing a quiz, your score will be recorded and displayed on the scores page.
- You can reset your scores on the scores page if needed.
- To log out, click on the "Logout" link.

## Contributing

Contributions to Quizzie are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request. Please follow the existing code style and guidelines.

## License

This project is licensed under the [MIT License](LICENSE).