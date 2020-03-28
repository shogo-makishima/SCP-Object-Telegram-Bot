import requests

class YandexTranslatorAPI:
    class Languages:
        russian = "ru"
        english = "en"

    def __init__(self, key=None):
        self.key = key

    def TranslatePhrase(self, text="Empty", languageFrom=Languages.english, languageTo=Languages.russian):
        returnText = None
        try:
            params = {"key": self.key, "text": text, "lang": f"{languageFrom}-{languageTo}"}
            response = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate", params=params)
            returnText = response.json()["text"]
        except: pass
        return returnText


yandexTranslator = YandexTranslatorAPI(key="trnsl.1.1.20200223T153509Z.041d99a1c679bc64.42fe0c0c6897d5897139c1c24d32e4df75932b9a")
