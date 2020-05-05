from bs4 import BeautifulSoup
from requests import get

class Value:
    def __init__(self, code_name: str, for_once: int, full_name: str, price: float):
        self.code_name, self.for_once, self.full_name, self.price, = code_name, for_once, full_name, price
    def __str__(self): return f"{self.code_name} {self.full_name} {self.for_once} {self.price}"


class Values(object):
    def __init__(self): self.values = list()
    def append(self, obj: Value): self.values.append(obj)
    def get(self, index: int): return self.values[index]
    def __iter__(self):
        for i in self.values: yield i


class CurrencyAPI:
    url = "https://www.profinance.ru/currency_usd.asp?s=USD/RUB"
    user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0')

    def __init__(self): pass

    async def Update(self) -> object:
        html = get(f"{self.url}", headers={'User-Agent': self.user_agent}).text
        data = BeautifulSoup(html, 'html.parser')

        values = Values()

        for tag in data.find_all(id="curtable"):
            temp_list = list()
            for element in tag.recursiveChildGenerator():
                if (len(temp_list) == 4):
                    if (temp_list[0] == "Код"): temp_list = list(); continue
                    values.append(Value(temp_list[0], int(temp_list[1]), temp_list[2], float(temp_list[3])))
                    temp_list = list()

                if (element.name == "td"):
                    temp_list.append(element.text)

        return values


'''
api = CurrencyAPI()
print([str(i) for i in run(api.Update())])
'''