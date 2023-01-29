from cohere.classify import Example
from examples import examples
from news import COUNTRIES
from time import time

import cohere
import json

co = cohere.Client('8bmPiNdnLA8op9gZ1si2ABVfig4MN7mKJvdOmcDR') # This is your trial API key
# response = co.classify(
#   model='506fb1c0-687e-442c-bf14-64bcfdded0b8-ft',
#   inputs=["<YOUR_INPUTS>"])

# print('The confidence levels of the labels are: {}'.format(response.classifications))

def sort():
    headlines = []
    with open("all_countries_news.json", "r") as f:
        headlines = [json.loads(l.strip()) for l in f.readlines()]

    lines = []
    with open("countries_ranked.txt", "r") as f:
        lines = [l.strip().split(": ") for l in f.readlines()]
        lines = [(l[0], float(l[1].rstrip(" pts"))) for l in lines]
        lines = sorted(lines, key=lambda x: x[1])

        # lines = (sorted([l.split(": ") for l in lines], key=lambda x: float(x[1].rstrip(" pts"))))
        # lines = [": ".join(l) for l in lines]

    i = 0
    for l in lines:
        l = list(l)
        l[1] = str(round(l[1] / len(headlines[i]), 2))
        lines[i] = ": ".join(l)

        i += 1

    with open("sorted_ranked.txt", "w+") as j:
        for l in lines:
            j.write(l + "\n")


def analyze_each_country():
    lines = []
    with open("all_countries_news.json", "r") as f:
        lines = [json.loads(l.strip()) for l in f.readlines()]
    
    analyized = []

    print(f"Analyzing {len(lines)} countries...")
    for c, headlines in zip(COUNTRIES, lines):
        print(f"Analyzing {c}, ({len(headlines)} headlines), ", end="")
        s = time()
        response = co.classify(
            model='506fb1c0-687e-442c-bf14-64bcfdded0b8-ft',
            inputs=headlines
        )

        total_sentiment = 0
        for sent in response.classifications:
            if sent.prediction.strip() == "negative":
                total_sentiment -= sent.confidence
            if sent.prediction.strip() == "positive":
                total_sentiment += sent.confidence

        analyized.append((c, total_sentiment))
        e = time()
        print(f"{round(e - s, 3)}s elapsed") 

    print(analyized)
    with open("countries_ranked.txt", "w+") as f:
        analyized = sorted(analyized, key=lambda x: x[1])
        for tup in analyized:
            t = list(tup)
            t[1] = str(t[1])
            t = ": ".join(t)
            f.write(t + "\n")


    print()
analyze_each_country()