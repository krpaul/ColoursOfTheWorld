import requests as rq
from bs4 import BeautifulSoup

def grab_charities(keyword, num=3):
    response = rq.get("https://www.change.org/search?q=" + keyword)

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select("a[class^=corgi-]")[::2]

    if len(links) > num:
        links = links[:num]

    ret = []
    for link in links:
        ret.append(
            (link.text, "https://www.change.org" + link.attrs['href'])
        )
    
    return ret

if __name__ == "__main__":
    print(grab_charities("China"))