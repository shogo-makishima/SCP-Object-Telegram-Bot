import mysql.connector as mysql
import Classes.Core.Settings as Settings

class SQLMain:
    def __init__(self):
        self.__connection = mysql.connect(
                host = Settings.HOST_DB,
                user = Settings.USER_DB,
                passwd = Settings.PASSWD_DB,
                database = Settings.DATABASE_DB,
        )

        self.__cursor = self.__connection.cursor()

    def GetAllTables(self):
        self.__cursor.execute("SHOW TABLES")
        return self.__cursor.fetchall()

    def GetAllSources(self) -> list:
        self.__cursor.execute("""SELECT Name FROM Sources""")
        temp_list_get = self.__cursor.fetchall()
        temp_list_ret = list()
        for i in temp_list_get: temp_list_ret.append(i[0])
        return temp_list_ret

    def GetUserFromChatID(self, chat_id: int) -> list:
        self.__cursor.execute(f"""SELECT * FROM Users WHERE chat_id = {chat_id};""")
        return self.__cursor.fetchone()

    def SetUserFromChatID(self, chat_id: int) -> None:
        self.__cursor.execute(f"""INSERT INTO Users (chat_id, source) VALUES ({chat_id}, "ENG")""")
        self.__connection.commit()

    def GetSourceFromChatID(self, chat_id: int) -> str:
        self.__cursor.execute(f"""SELECT URL From Sources WHERE Name = (SELECT source FROM Users WHERE chat_id = {chat_id});""")
        return self.__cursor.fetchone()[0]

    def SetSourceFromChatID(self, chat_id: int, data: str):
        self.__cursor.execute(
        f"""
        UPDATE Users
        SET source = \'{data}\'
        WHERE chat_id = {chat_id}
        """)
        self.__connection.commit()

    def GetLastFindingFromChatID(self, chat_id: int) -> str:
        self.__cursor.execute(f"""SELECT last_finding FROM Users WHERE chat_id = {chat_id};""")
        return self.__cursor.fetchone()[0]

    def GetFavoriteFromChatID(self, chat_id: int) -> list:
        try:
            self.__cursor.execute(f"""SELECT favorite FROM Users WHERE chat_id = {chat_id};""")
            string = str(self.__cursor.fetchone()[0])
            temp_list = string.split(",")
            return temp_list if (temp_list != ['']) else ["None"]
        except TypeError:
            self.SetUserFromChatID(chat_id)
            return ["None"]

    def SetFavoriteByChatID(self, chat_id: int, data: str) -> None:
        temp_data = self.GetFavoriteFromChatID(chat_id)
        if(data not in temp_data): temp_data.append(data)
        else: return
        self.__cursor.execute(
        f"""
        UPDATE Users
        SET favorite = \"{",".join(temp_data)}\"
        WHERE chat_id = {chat_id}
        """)
        self.__connection.commit()

    def RemoveFavoriteByChatID(self, chat_id: int, data: str) -> None:
        temp_data = self.GetFavoriteFromChatID(chat_id)
        if (data in temp_data): temp_data.remove(data)
        else: return
        self.__cursor.execute(f"""
                UPDATE Users
                SET favorite = \"{",".join(temp_data)}\"
                WHERE chat_id = {chat_id}
                """)
        self.__connection.commit()

    def GetCurrencyFromCodeName(self, code_name: str):
        self.__cursor.execute(f"""SELECT * FROM Currency WHERE code_name = {code_name.upper()};""")
        return self.__cursor.fetchone()

    def UpdateCurrencyFromList(self, values: list) -> None:
        self.__cursor.execute("SELECT code_name FROM Currency")
        currency_in_db = [i[0] for i in self.__cursor.fetchall()]
        print(currency_in_db)
        for value in values:
            if (value.code_name in currency_in_db):
                self.__cursor.execute(f"""
                UPDATE Currency
                SET price = {value.price}
                WHERE code_name = '{value.code_name}'
                """)
            else:
                self.__cursor.execute(f"""INSERT INTO Currency (code_name, for_once, full_name, price) VALUES ('{value.code_name}', {value.for_once}, '{value.full_name}', {value.price})""")
        self.__connection.commit()

    def CloseDataBase(self):
        self.__connection.close()
