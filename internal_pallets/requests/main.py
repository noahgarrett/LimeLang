from results import RTResult
from values import Number
import requests


class Requests:
    def __init__(self):
        self.functions: dict = {
            "get": self.get,
            "post": self.post
        }

    def get(self, args: list):
        res: RTResult = RTResult()
        url: str = args[0]

        response = requests.get(url)
        print(response.content)

        return res.success(Number(0))

    get.arg_names = ['url']

    def post(self):
        pass


def import_pallet() -> Requests:
    return Requests()


if __name__ == '__main__':
    """ This is only called for generating a new ast for the internal pallet """
    from exec import Lexer, Parser, Interpreter


