import sqlite3
import json

DB_FILE="minesweeper.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)

def dbsetup():
  c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
  
  command = "CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, mode TEXT, difficulty TEXT)"
  c.execute(command)      # test SQL stmt in sqlite3 shell, save as string

  db.commit() #save changes

dbsetup()

# Authorization, username, and user_id functions
##

# Adds to the user database if the username is availible
# Returns an error message to display if there was an issue or an empty string otherwise
def signup(username, password):
  c = db.cursor()

  c.execute("""SELECT username FROM user WHERE username=?""",[username])
  result = c.fetchone()

  if result:
      return "Error: Username already exists"

  else:
      c.execute('INSERT INTO user VALUES (null, ?, ?, ?, ?)', (username, password, "light", "script kiddie"))
      
      db.commit()
      # Uses empty quotes since it will return false when checked as a boolean
      return  ""

# Tries to check if the username and password are valid
def login(username, password):
  c = db.cursor()

  c.execute("""SELECT username FROM user WHERE username=? AND password=?""",[username, password])
  result = c.fetchone()

  if result:
      ##access this specifc user data
      return False

  else:
      return True

def get_mode(username):
  c = db.cursor()

  c.execute("""SELECT mode FROM user WHERE username=?""",[username])
  result = c.fetchone()

  return result

def get_difficulty(username):
  c = db.cursor()

  c.execute("""SELECT difficulty FROM user WHERE username=?""",[username])
  result = c.fetchone()

  return result

def change_mode(username):
  c = db.cursor()

  c.execute("""SELECT mode FROM user WHERE username=?""",[username])
  result = c.fetchone()

  if result == "dark":
    c.execute('UPDATE user SET mode = ? WHERE username = ?', ("light", username))
  else:
    c.execute('UPDATE user SET mode = ? WHERE username = ?', ("dark", username))
  db.commit()

def change_difficulty(username, new_diff):
  c = db.cursor()
  
  c.execute('UPDATE user SET difficulty = ? WHERE username = ?', (new_diff, username))

  db.commit()