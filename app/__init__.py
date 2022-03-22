from flask import Flask, render_template, request, session, redirect, url_for
import db_builder
# from flask_mobility import Mobility
#import db_builder

with open("app/db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_builder.py", "exec")
exec(code)

db_builder = Builder()


app = Flask(__name__)
app.secret_key = 'minesweeper'

def logged_in():
    return session.get('username') is not None

@app.route('/', methods=['GET','POST'])
def login():
    method = request.method
    # Check for session existance
    if method == 'GET':
        if logged_in():
            return redirect('/menu')
        else:
        # If not logged in, show login page
            return render_template('login.html', error=False)

    if method == 'POST':
    # Get information from request.form since it is submitted via post
        username = request.form['username']
        password = request.form['password']
        error = db_builder.login(username, password)

    if error:
    # If incorrect, give feedback to the user
        return render_template('login.html', error=error)
    else:
    # Store user info into a cookie
        session['username'] = username
        return redirect('/menu')

@app.route('/register', methods=['GET','POST'])
def register():
    method = request.method
    # Check for session existence
    if method == "GET":
        if logged_in():
            return redirect('/')
        else:
            # If not logged in, show regsiter page
            return render_template('register.html', error_message="")

    if method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        error_message = ""
        if not new_username:
            error_message = "Error: No username entered!"
        elif not new_password:
            error_message = "Error: No password entered!"
        elif confirm_password != new_password:
            error_message = "Error: Passwords do not match!"

        if error_message:
            return render_template("register.html", error_message=error_message)

        error_message = db_builder.signup(new_username, new_password)

        if error_message:
            return render_template("register.html", error_message=error_message)
        else:
            session['username'] = new_username
            return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Once again check for a key before popping it
    if logged_in():
        session.pop('username')

    # After logout, return to login page
    return redirect('/')

@app.route('/home')
def home():
    try:
        return render_template("home.html")
    except:
        return render_template("error.html")

@app.route('/menu')
def menu():
    try:
        if logged_in():
            user = session.get("username")
            mode = db_builder.get_mode(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            return render_template("menu.html", colors = colors)
        else:
            return redirect('/')
    except:
        return render_template("error.html")

@app.route('/gamepage')
def about():
    try:
        if logged_in():
            user = session.get("username")
            mode = db_builder.get_mode(user)[0]
            difficulty = db_builder.get_difficulty(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            return render_template("gamepage.html", mode = mode, user_priv = user, difficulty = difficulty, colors = colors)
        else:
            return redirect('/')
    except:
        return render_template("error.html")

@app.route('/won')
def won():
    try:
        if logged_in():
            #increase win streak by one
            user = session.get("username")
            mode = db_builder.get_mode(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            streak = db_builder.increase_win_streak(user)
            return render_template("won.html", colors = colors, streak = streak)
        else:
            return redirect('/')
    except:
        return render_template("error.html")

@app.route('/lost')
def lost():
    try:
        if logged_in():
            #set win streak to zero
            user = session.get("username")
            mode = db_builder.get_mode(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            streak = db_builder.reset_win_streak(user)
            return render_template("lost.html", colors = colors, streak = streak)
        else:
            return redirect('/')
    except:
        return render_template("error.html")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        if logged_in():
            user = session.get("username")
            mode = db_builder.get_mode(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            return render_template("settings.html", colors = colors, mode = mode)
        else:
            return redirect("/")
    except:
        return render_template("error.html")

@app.route('/change_diff', methods=['GET', 'POST'])
def result():
    try:
        if logged_in():
            user = session.get("username")
            diff = request.form['button']
            db_builder.change_difficulty(user, diff)
            mode = db_builder.get_mode(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            return render_template("settings.html", colors = colors, mode = mode)
        else:
            return redirect("/")
    except:
        return render_template("error.html")

@app.route('/change_mode', methods=['GET', 'POST'])
def other_result():
    #try:
        if logged_in():
            user = session.get("username")
            db_builder.change_mode(user)
            mode = db_builder.get_mode(user)[0]
            colors = ["#222222", "#ffffff"] if mode == "dark" else ["#ffffff", "black"]
            return render_template("settings.html", colors = colors, mode = mode)
        else:
            return redirect("/")
    #except:
        #return render_template("error.html")
        
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run(host='0.0.0.0')