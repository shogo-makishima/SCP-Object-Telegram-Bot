from bs4 import BeautifulSoup
from requests import get
from Classes.Core.Languages import Languanges

class URLS:
    urls = ["scp-wiki.net/scp-", "scpfoundation.net/scp-"]


class SCPFoundationAPI:
    url = URLS.urls[0]

    def __init__(self): pass

    async def GetObjectByNumber(self, number: str = "610", langunage: Languanges.Language = Languanges.RU):
        html = get(self.url + number).text
        data = BeautifulSoup(html, 'html.parser')

        strings: list = []
        string: str = ""

        for tag in data.find_all(id="page-content"):
            for element in tag.recursiveChildGenerator():
                if (element.name in ["p", "li"]):
                    if (len(element.text) + len(string) > 3000):
                        strings.append(string)
                        string = ""
                    string += f"{element.text}\n"

        strings.append(string)

        return strings
