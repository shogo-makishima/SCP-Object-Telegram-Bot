from bs4 import BeautifulSoup
from requests import get
from Classes.Core.Languages import Languanges

class SCPFoundationAPI:
    url = "http://scp-wiki.net"

    def __init__(self): pass

    async def GetObjectByNumber(self, number: str = "610", langunage: Languanges.Language = Languanges.RU, url: str = None):
        if (url): html = get(f"{url}/scp-{number}").text
        else: html = get(f"{self.url}/scp-{number}").text
        data = BeautifulSoup(html, 'html.parser')

        strings: list = []
        string: str = ""

        for tag in data.find_all(id="page-content"):
            for element in tag.recursiveChildGenerator():
                if (element.name in ["p", "li"]):
                    if (len(element.text) + len(string) > 4096):
                        strings.append(string)
                        string = ""
                    string += f"{element.text}\n"

        strings.append(string)

        return strings

# scpAPI = SCPFoundationAPI()
# print(scpAPI.GetObjectByNumber("3333"))

# sql = SQLMain()
# sql.SetFavoriteByChatID(666314796, "3333")
# print(sql.GetFavoriteFromChatID(666314796))
# sql.SetSourceFromChatID(666314796, "ENG")
# print(sql.GetSourceFromChatID(666314796))

