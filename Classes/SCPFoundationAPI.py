from bs4 import BeautifulSoup
from requests import get
from Classes.Core.Languages import Languanges

class SCPFoundationAPI:
    url = 'http://scpfoundation.net/scp-'
    def __init__(self): pass

    def GetObjectByNumber(self, number: str = "610", langunage: Languanges.Language = Languanges.RU):
        html = get(self.url + number).text
        data = BeautifulSoup(html)

        string: str = ""

        for tag in data.find_all(id="page-content"):
            for element in tag.recursiveChildGenerator():
                if (element.name in ["p", "li"]): string += f"{element.text}\n"

        return string


