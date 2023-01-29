from newsapi import NewsApiClient
import datetime as dt
import json
import numpy as np


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Init
newsapi = None
with open("../newskey.key") as f:
    newsapi = NewsApiClient(api_key=f.read().strip())

countries = []
with open("countries.txt") as f:
    countries = f.readlines()
    countries = [c.strip() for c in countries]

for c in countries:
    all_articles = newsapi.get_everything(
        q=c,
        from_param=(dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d"),
        to=dt.datetime.now().strftime("%Y-%m-%d"),
        language='en',
        sort_by='relevancy',
    )

    if len(all_articles["articles"]) > 10:
        all_articles["articles"] = all_articles["articles"][:10]

    for article in all_articles["articles"]:
        with open("articles.json", "a+") as f:
            new_dict = {}
            new_dict["title"] = article["title"]
            new_dict["desc"] = article["description"]
            new_dict["country"] = c

            f.write(json.dumps(new_dict) + "\n")

# split file
newslines = []
with open("articles.json") as f:
    lines = f.readlines()
    newslines = list(np.array_split(lines, 3))
    
for idx, fname in enumerate(["stanley.json", "kevin.json", "minos.json"]):
    with open(fname, "a+") as j:
        j.writelines(newslines[idx])
    
