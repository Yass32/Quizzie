import os
import pymysql
from flask import Flask, jsonify, render_template, request, flash, redirect, session
from flask_session import Session

# Create a Flask application instance
app = Flask(__name__)

# Configure session to use the filesystem instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load MySQL configuration from environment variables
app.config["MYSQLHOST"] = os.getenv("MYSQLHOST")
app.config["MYSQLUSER"] = os.getenv("MYSQLUSER")
app.config["MYSQLPASSWORD"] = os.getenv("MYSQLPASSWORD")
app.config["MYSQLDATABASE"] = os.getenv("MYSQLDATABASE")
app.config["MYSQLPORT"] = int(os.getenv("MYSQLPORT", 3306))

# Establish a connection to the MySQL database
try:
    connection = pymysql.connect(
        host=app.config["MYSQLHOST"],
        user=app.config["MYSQLUSER"],
        password=app.config["MYSQLPASSWORD"],
        database=app.config["MYSQLDATABASE"],
        port=app.config["MYSQLPORT"],
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Database connected successfully!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    connection = None  # Prevent further database interactions if connection fails

# Route to test database connection
@app.route("/test_db")
def test_db():
    if connection is None:
        return "❌ Database connection failed!"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return "✅ Database connected successfully!"
    except Exception as e:
        return f"❌ Database error: {e}"

# Home Page Route
@app.route("/")
def index():
    # Redirect to registration page if user is not logged in
    if not session.get("username"):
        return redirect('/register')
    return render_template("index.html")

# User Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password are provided
        if not username or not password:
            flash("Username or Password is missing")
            return render_template("register.html")
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                session['loggedin'] = True
                session['id'] = cursor.lastrowid
                session['username'] = username
                connection.commit()
            flash(f"{session['username']} you have registered successfully!")
            return redirect('/')  # Redirect to home page after registration
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            msg = "Username is already taken or an error occurred!"
            return render_template("register.html", msg=msg)
    return render_template("register.html", msg='Please fill out the form!')

# User Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password are provided
        if not username or not password:
            flash("Username or Password is missing")
            return render_template("login.html")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
                row = cursor.fetchone()

            # Check if login credentials are valid
            if row:
                session['loggedin'] = True
                session['id'] = row["id"]
                print(f"{session['id']} session['id']!")
                print(f"{session[id]} session[id]!")

                print(f"{row['id']} row['id']!")
                print(f"{row[id]} row[id]!")

                session['username'] = username
                flash(f"{session['username']} you have logged in successfully!")
                return redirect('/')
            else:
                msg = 'Invalid username or password'
                return render_template("login.html", msg=msg)
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            msg = "An error occurred, please try again!"
            return render_template("login.html", msg=msg)
    return render_template("login.html", msg='Please fill out the form!')

# User Logout Route
@app.route("/logout")
def logout():
    # Clear session data to log out the user
    session.clear()
    flash("You have logged out successfully!")
    return redirect("/")

# Scores Page Route
@app.route("/scores")
def scores():
    # Retrieve user's scores from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['id'],))

        print(f"{session['id']} session['id'] Select from users where!")
        scores = cursor.fetchall()
    return render_template("scores.html", name=session['username'], scores=scores)

# Reset User Scores Route
@app.route('/reset-scores', methods=['POST'])
def reset_scores():
    # Reset all quiz scores to zero
    reset = int(request.form.get('score'))
    with connection.cursor() as cursor:
        cursor.execute("UPDATE users SET maths_easy=%s, maths_intermediate=%s, maths_hard=%s, "
                       "english_easy=%s, english_intermediate=%s, english_hard=%s, "
                       "science_easy=%s, science_intermediate=%s, science_hard=%s WHERE id=%s", 
                       (reset, reset, reset, reset, reset, reset, reset, reset, reset, session["id"]))
        connection.commit()
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
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET maths_easy = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Intermediate Maths":
        score = int(score)/8 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET maths_intermediate = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Hard Maths":
        score = int(score)/10 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET maths_hard = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Easy English":
        score = int(score)/4 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET english_easy = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Intermediate English":
        score = int(score)/8 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET english_intermediate = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Hard English":
        score = int(score)/10 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET english_hard = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Easy Science":
        score = int(score)/4 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET science_easy = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Intermediate Science":
        score = int(score)/8 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET science_intermediate = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    elif title == "Quizzie App: Hard Science":
        score = int(score)/10 * 100
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET science_hard = %s WHERE id = %s", (score, session['id']))
        connection.commit()
    
    connection.close()
    return jsonify(success=True)

# Individual Quiz Routes
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
    return render_template("science_hard.html")

# Run the Flask application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render typically uses PORT env var
    app.run(host="0.0.0.0", port=port)
    #app.run(debug=True)


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
    science_hard INT DEFAULT 0,
);
'''