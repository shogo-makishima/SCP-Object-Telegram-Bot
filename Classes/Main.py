import json, os, math, sqlite3

class SQLMain:
    __connection = sqlite3.connect("app\\Saves\\SCPBot.db", check_same_thread=False)
    __cursor = __connection.cursor()

    def GetAllSources(self) -> list:
        temp_list_get = self.__cursor.execute("""SELECT Name FROM Sources""").fetchall()
        temp_list_ret = list()
        for i in temp_list_get: temp_list_ret.append(i[0])
        return temp_list_ret

    def GetUserFromChatID(self, chat_id: int) -> list:
        return self.__cursor.execute(f"""SELECT * FROM Users WHERE chat_id = {chat_id};""").fetchone()

    def SetUserFromChatID(self, chat_id: int) -> None:
        self.__cursor.execute(f"""INSERT INTO Users (chat_id, source) VALUES ({chat_id}, "ENG")""")
        self.__connection.commit()

    def GetSourceFromChatID(self, chat_id: int) -> str:
        return self.__cursor.execute(f"""SELECT URL From Sources WHERE Name = (SELECT source FROM Users WHERE chat_id = {chat_id});""").fetchone()[0]

    def SetSourceFromChatID(self, chat_id: int, data: str):
        self.__cursor.execute(
        f"""
        UPDATE Users
        SET source = \'{data}\'
        WHERE chat_id = {chat_id}
        """)
        self.__connection.commit()

    def GetLastFindingFromChatID(self, chat_id: int) -> str:
        return self.__cursor.execute(f"""SELECT last_finding FROM Users WHERE chat_id = {chat_id};""").fetchone()[0]

    def GetFavoriteFromChatID(self, chat_id: int) -> list:
        string = str(self.__cursor.execute(f"""SELECT favorite FROM Users WHERE chat_id = {chat_id};""").fetchone()[0])
        temp_list = string.split(",")
        return temp_list if (temp_list != ['']) else list()

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

    def CloseDataBase(self):
        self.__connection.close()


class Main:
    @staticmethod
    def LoadPerson(self, chat_id: int) -> dict:
        try:
            with open(f"/app/Saves/{chat_id}.json") as file:
                return json.load(file)
        except: return None

    @staticmethod
    def SavePerson(self, chat_id: int, newUrl: str) -> None:
        data = {
            "chat_id": chat_id,
            "url": newUrl,
        }

        with open(f"/app/Saves/{chat_id}.json", "w") as file:
            file.write(json.dumps(data))
