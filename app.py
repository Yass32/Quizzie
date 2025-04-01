from flask import Flask, jsonify, render_template, request, flash, redirect, session
from flask_mysql_connector import MySQL
from flask_session import Session
import pymysql
#Create a Flask instance
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configuration for MySQL connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "users"
mysql = MySQL(app)

# Test database connection
try:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1")  # Simple query to test connection
    print("Database connected successfully!")
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    # This will print a success message if the database connection is established, or an error message if the connection fails.

# Home Page
@app.route("/")
def index():
    # Redirect to registration page if the user is not logged in
    if not session.get("username"):
        return redirect('/register')
    return render_template("index.html")


# User registration
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username and password are provided
        if not username or not password:
            flash("Username or Password is missing")
            return render_template("register.html")
        try:
            # Insert user into the database
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            session['loggedin'] = True
            session['id'] = cursor.lastrowid
            session['username'] = username
            mysql.connection.commit()
            flash(f"{session['username']} you have registered in successfully !!")
            return redirect('/')
        except:
            msg = 'Username or Password is already taken!'
            return render_template("register.html", msg = msg)
    else:
        msg = 'Please fill out the form !'
        return render_template("register.html", msg = msg)


# User login   
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get ("password")

        # Check if username and password are provided
        if not username or not password:
            flash("Username or Password is missing")
            return render_template("login.html")
        try:
            # Query database for username and password
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
            rows = cursor.fetchone()

            # Ensure username exists and password is correct
            if rows is not None:
                # Remember which user has logged in
                session['loggedin'] = True
                session['id'] = rows[0]
                session['username'] = username
                flash(f"{session['username']} you have logged in successfully !!")
                return redirect('/')
            else:
                msg = 'Username or Password is not in the database'
                return render_template("login.html", msg = msg)          
        except:
            msg = 'Username or Password is incorrect!'
            return render_template("login.html", msg = msg)
    else:
        msg = 'Please fill out the form !'
        return render_template("login.html", msg = msg)


# User logout
@app.route("/logout")
def logout():
    # Clear user session data
    session['loggedin'] = None
    session['id'] = None
    session['username'] = None
    return redirect("/")


# Scores page
@app.route("/scores")
def scores():
    # Retrieve user scores from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['id'],))
    scores = cursor.fetchall()
    return render_template("scores.html", name = session['username'], scores = scores)


# Reset scores
@app.route('/reset-scores', methods=['POST'])
def reset_scores():
    # Reset scores in the database
    reset = int(request.form.get('score'))
    print(reset)
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET maths_easy = %s, maths_intermediate = %s, maths_hard = %s, english_easy = %s, english_intermediate = %s, english_hard = %s, science_easy = %s, science_intermediate = %s, science_hard = %s WHERE id = %s", (reset, reset, reset, reset, reset, reset, reset, reset, reset, session["id"]))
    mysql.connection.commit()
    return jsonify(success=True)


# Submit scores
@app.route('/submit-scores', methods=['POST'])
def submit_scores():
    # Get the score page title of the quiz
    score = request.form.get('score')
    title = request.form.get('title')

    # Check if the title is valid
    if title not in ['Quizzie App: Easy Maths', 'Quizzie App: Intermediate Maths', 'Quizzie App: Hard Maths', 'Quizzie App: Easy English', 'Quizzie App: Intermediate English', 'Quizzie App: Hard English', 'Quizzie App: Easy Science', 'Quizzie App: Intermediate Science', 'Quizzie App: Hard Science']:
        return "An error has occurred"
    
    # Update the score in the databse
    if title == "Quizzie App: Easy Maths":
        score = int(score)/4 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET maths_easy = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Intermediate Maths":
        score = int(score)/8 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET maths_intermediate = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Hard Maths":
        score = int(score)/10 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET maths_hard = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Easy English":
        score = int(score)/4 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET english_easy = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Intermediate English":
        score = int(score)/8 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET english_intermediate = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Hard English":
        score = int(score)/10 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET english_hard = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Easy Science":
        score = int(score)/4 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET science_easy = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Intermediate Science":
        score = int(score)/8 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET science_intermediate = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    elif title == "Quizzie App: Hard Science":
        score = int(score)/10 * 100
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET science_hard = %s WHERE id = %s", (score, session['id']))
        mysql.connection.commit()
    
    return jsonify(success=True)


# Routes for different subjects
@app.route("/maths_easy")
def maths_easy():
    return render_template("maths_easy.html")

@app.route("/maths_intermediate")
def maths_intermediate():
    return render_template("maths_intermediate.html")

@app.route("/maths_hard")
def maths_hard():
    return render_template("maths_hard.html")

@app.route("/english_easy")
def english_easy():
    return render_template("english_easy.html")

@app.route("/english_intermediate")
def english_intermediate():
    return render_template("english_intermediate.html")

@app.route("/english_hard")
def english_hard():
    return render_template("english_hard.html")

@app.route("/science_easy")
def science_easy():
    return render_template("science_easy.html")

@app.route("/science_intermediate")
def science_intermediate():
    return render_template("science_intermediate.html")

@app.route("/science_hard")
def science_hard():
    return render_template('science_hard.html')

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)

'''
MySQL TABLE
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
'''