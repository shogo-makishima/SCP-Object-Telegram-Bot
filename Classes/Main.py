import json, os, math, sqlite3


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
