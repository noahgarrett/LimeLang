var pythonCode = """
from requests import get

json = get('https://jsonplaceholder.typicode.com/todos/1').json()
"""

var a = exec(pythonCode)
var json = a["json"]
print(json)
print("Title: " + json["title"])