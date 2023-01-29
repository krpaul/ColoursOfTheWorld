from newsapi import NewsApiClient
from pygooglenews import GoogleNews
import datetime as dt
import json

COUNTRIES = []
with open("classification/countries.txt") as f:
    COUNTRIES = [l.strip() for l in f.readlines()]

# Init
newsapi = None
with open("newskey.key") as f:
    newsapi = NewsApiClient(api_key=f.read().strip())

gn = GoogleNews()   

def get_intensity(country):
    # /v2/everything
    all_articles = newsapi.get_everything(q=country,
                                        # sources='bbc-news,the-verge',
                                        # domains='bbc.co.uk,techcrunch.com',
                                        from_param=(dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d"),
                                        to=dt.datetime.now().strftime("%Y-%m-%d"),
                                        language='en',
                                        sort_by='relevancy',
    )

    # data = json.loads(all_articles)
    intensity = 0

    for article in data['articles']:
        # if bad
        intensity += 1

    return intensity / len(data['articles']) * 100

def download_all_countries_news():
    with open("all_countries_news.json", "w+") as f:
        for c in COUNTRIES:
            data = get_google_news(c)
            articles = data["entries"]
            titles = [a['title'] for a in articles]

            f.write(json.dumps(titles) + "\n")

def test(c):
    print(get_intensity(c)) 

def get_google_news(country):
    return gn.geo_headlines(country)


if __name__ == "__main__":
    # test("Sudan")
    download_all_countries_news()
    # print(get_google_news("Poland"))


# # /v2/top-headlines/sources
# sources = newsapi.get_sources()

