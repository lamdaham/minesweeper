from flask import Flask, app, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    try:
        return render_template("login.html")
    except:
        return render_template("error.html")

@app.route('/loading')
def load():
    try:
        return render_template("load.html")
    except:
        return render_template("error.html")

@app.route('/menu')
def menu():
    try:
        return render_template("menu.html")
    except:
        return render_template("error.html")

@app.route('/gamepage')
def about():
    try:
        return render_template("gamepage.html")
    except:
        return render_template("error.html")
        
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()