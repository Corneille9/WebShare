import os
import sqlite3

from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar


class DbManager:

    def __init__(self, db_name="webshare.db"):
        self.connection = None
        self.cursor = None
        self.path = None
        self.__check_db(db_name)
        self.__createFilesTable__()

    def __check_db(self, db_name):
        print("DbManager ->> ", "DbManager started...")
        if not os.path.exists(os.environ["USERPROFILE"] + "\\.webshare"):
            os.makedirs(os.environ["USERPROFILE"] + "\\.webshare")
        self.path = os.environ["USERPROFILE"] + "\\.webshare\\"
        self.connection = sqlite3.connect(self.path + db_name)
        self.cursor = self.connection.cursor()
        print("DbManager ->> ", "Successfully established connection to ", db_name)

    def __createFilesTable__(self):
        print("DbManager ->> ", "Verifying database...")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            path VARCHAR(60) NOT NULL,
            isLocked BOOLEAN NULL
        )""")
        self.connection.commit()
        print("DbManager ->> ", "Verification completed successfully...")

    def insertFiles(self, path_list):
        valid_paths = self.getValidPaths(path_list)
        if len(valid_paths) != 0:
            for file in valid_paths:
                self.cursor.execute(""" INSERT INTO files(path, isLocked) VALUES (?,?) """, file)
                self.connection.commit()
                print("DbManager ->> ", "All done!")
        return valid_paths

    def getValidPaths(self, path_list):
        valid_paths = []
        shw_snack = False
        for path in path_list:
            if len(self.getfileByPath(path)) == 0:
                valid_paths.append((path, False))
            else:
                shw_snack = True
        if shw_snack:
            Snackbar(
                text="[color=#ddbb34]Some of these files already exist and does not added![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(Window.width - (dp(10) * 2)) / Window.width
            ).open()
        return valid_paths

    def getAllFiles(self):
        self.cursor.execute("SELECT * FROM files")
        return self.cursor.fetchall()

    def getFileById(self, id):
        self.cursor.execute(""" SELECT * FROM files WHERE id=? """, (id,))
        return self.cursor.fetchall()

    def getfileByPath(self, path):
        self.cursor.execute(""" SELECT * FROM files WHERE path=?""", (path,))
        return self.cursor.fetchall()

    def deleteFileById(self, id):
        self.cursor.execute(""" DELETE FROM files WHERE id=? """, (id,))
        self.connection.commit()

    def deleteFileByPath(self, path):
        self.cursor.execute(""" DELETE FROM files WHERE path=? """, (path,))
        self.connection.commit()
