from kivy.config import Config

Config.set("graphics", "resizable", False)
Config.set("graphics", "width", 620)
Config.set("graphics", "height", 540)
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

dbname = "database.db"
c = sqlite3.connect(dbname)
c.execute("PRAGMA foreign_keys = 1")

try:
    ddl = """
    CREATE TABLE item
    (
       item_code INTEGER PRIMARY KEY AUTOINCREMENT,
       item_name TEXT NOT NULL UNIQUE
    );
     """

    c.execute(ddl)

    ddl = """
    CREATE TABLE acc_data
    ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acc_date DATE NOT NULL,
        item_code INTEGER NOT NULL,
        amount INTEGER,
        FOREIGN KEY(item_code) REFERENCES item(item_code)
    );
    """

    c.execute(ddl)
    c.execute("INSERT INTO item(item_name) VALUES('食費');")
    c.execute("INSERT INTO item(item_name) VALUES('住宅費');")
    c.execute("INSERT INTO item(item_name) VALUES('光熱費');")
    c.execute("COMMIT;")
except:
    pass

# ログインID、Pass設定

USER_ID = "test"
PASSWORD = "test"
ERROR_MESSAGE = "ログインエラー"

LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")
sm = ScreenManager()


# 　ログイン画面

class LoginScreen(Screen):

    def loginButtonClicked(self):
        userID = self.ids["text_userID"].text
        password = self.ids["text_password"].text
        if userID == USER_ID and password == PASSWORD:
            sm.current = "input"
        else:
            self.ids["error_message"].text = ERROR_MESSAGE

#   入力画面

class InputScreen(Screen):
    def clearButtonClicked(self):
        for key in self.ids:
            self.ids[key].text = ""

    def submitButtonClicked(self):
        item_name = self.ids["item_code"].text

        c = sqlite3.connect("database.db")

        item_code = c.execute("""
                 SELECT item_code FROM item
                 WHERE item_name = '{}'
                 """.format(item_name))
        item_code = item_code.fetchone()[0]

        acc_data = self.ids["acc_date"].text

        amount = self.ids["amount"].text

        # SQLを発行してDBへ登録
        try:
            c.execute("""
                INSERT INTO acc_data(acc_date,item_code,amount)
                VALUES('{}',{},{});
                """.format(acc_data, item_code, amount))
            c.execute("COMMIT;")
            print("1件登録しました")
        # エラー処理
        except:
            print("エラーにより登録できませんでした")

        self.clearButtonClicked()

    def resultButtonClicked(self):
        sm.current = "result"

#   リザルト画面

class ResultScreen(Screen):
    try:
        sql = """
        SELECT acc_date,item_name,amount
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code
        ORDER BY acc_date
        """
        list = c.execute(sql)

        list2 = c.execute(sql)

        list3 = c.execute(sql)
    except:
        list = ""

        list2 = ""

        list3 = ""

    def loginButtonClicked(self):
        sm.current = "input"

#   画面遷移

class ExpenseApp(App):
    def build(self):
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(InputScreen(name="input"))
        sm.add_widget(ResultScreen(name="result"))
        return sm


if __name__ == '__main__':
    ExpenseApp().run()
