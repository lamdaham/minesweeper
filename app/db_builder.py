import sqlite3
import json

class Builder:
  def __init__(self):  
    DB_FILE="minesweeper.db"
    self.db = sqlite3.connect(DB_FILE, check_same_thread=False)
    self.dbsetup()

  def dbsetup(self):
    c = self.db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    command = "CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, mode TEXT, difficulty TEXT, monkey_win_streak INTEGER, kiddy_win_streak INTEGER)"
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string

    self.db.commit() #save changes

  # Authorization, username, and user_id functions
  ##

  # Adds to the user database if the username is availible
  # Returns an error message to display if there was an issue or an empty string otherwise
  def signup(self, username, password):
    c = self.db.cursor()

    c.execute("""SELECT username FROM user WHERE username=?""",[username])
    result = c.fetchone()

    if result:
        return "Error: Username already exists"

    else:
        c.execute('INSERT INTO user VALUES (null, ?, ?, ?, ?, ?, ?)', (username, password, "light", "script kiddie", 0, 0))
        
        self.db.commit()
        # Uses empty quotes since it will return false when checked as a boolean
        return  ""

  # Tries to check if the username and password are valid
  def login(self, username, password):
    c = self.db.cursor()

    c.execute("""SELECT username FROM user WHERE username=? AND password=?""",[username, password])
    result = c.fetchone()

    if result:
        ##access this specifc user data
        return False

    else:
        return True

  def get_mode(self, username):
    c = self.db.cursor()

    c.execute("""SELECT mode FROM user WHERE username=?""",[username])
    result = c.fetchone()

    return result

  def get_difficulty(self, username):
    c = self.db.cursor()

    c.execute("""SELECT difficulty FROM user WHERE username=?""",[username])
    result = c.fetchone()

    return result

  def change_mode(self, username):
    c = self.db.cursor()

    c.execute("""SELECT mode FROM user WHERE username=?""",[username])
    result = c.fetchone()

    if result[0] == "dark":
      c.execute('UPDATE user SET mode = ? WHERE username = ?', ("light", username))
    else:
      c.execute('UPDATE user SET mode = ? WHERE username = ?', ("dark", username))
    self.db.commit()

  def change_difficulty(self, username, new_diff):
    c = self.db.cursor()
    
    c.execute('UPDATE user SET difficulty = ? WHERE username = ?', (new_diff, username))

    self.db.commit()

  def increase_win_streak(self, username, diff):
    c = self.db.cursor()

    if diff == "script kiddie":
      c.execute("""SELECT kiddy_win_streak FROM user WHERE username=?""",[username])
      result = c.fetchone()[0] + 1  
      c.execute('UPDATE user SET kiddy_win_streak = ? WHERE username = ?', (result, username))
    else:
      c.execute("""SELECT monkey_win_streak FROM user WHERE username=?""",[username])
      result = c.fetchone()[0] + 1
      c.execute('UPDATE user SET monkey_win_streak = ? WHERE username = ?', (result, username))

    

    self.db.commit()

    return result

  def reset_win_streak(self, username, diff):
    c = self.db.cursor()
    if diff == "script kiddie":
      c.execute("""SELECT kiddy_win_streak FROM user WHERE username=?""",[username])
      result = c.fetchone()[0]

      c.execute('UPDATE user SET kiddy_win_streak = ? WHERE username = ?', (0, username))
    else:
      c.execute("""SELECT monkey_win_streak FROM user WHERE username=?""",[username])
      result = c.fetchone()[0]

      c.execute('UPDATE user SET monkey_win_streak = ? WHERE username = ?', (0, username))

    self.db.commit()

    return result

  def get_scores(self):
    c = self.db.cursor()

    c.execute("""SELECT * FROM user""")

    users = c.fetchall()

    kiddy_scores = []
    monkey_scores = []

    for x in users:
      p = []
      p.append(x[1])
      p.append(x[5])
      monkey_scores.append(p)
      p = []
      p.append(x[1])
      p.append(x[6])
      kiddy_scores.append(p)
      

    kiddy_scores.sort(key=lambda x:(-x[1],x[0]))
    monkey_scores.sort(key=lambda x:(-x[1],x[0]))
    print(kiddy_scores)
    print(monkey_scores)
    print(users)
    return kiddy_scores, monkey_scores
