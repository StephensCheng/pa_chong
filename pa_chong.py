import requests
from bs4 import BeautifulSoup

r = requests.session().get("http://www.baidu.com")
r.encoding = "utf-8"
demo = r.text
soup = BeautifulSoup(demo, "html.parser")
s = soup.prettify()
print(s)
