import json
import colorama
import sys
from termcolor import cprint

colorama.init()
prt_grn = lambda s: cprint(s, 'green')
prt_red = lambda s: cprint(s, 'red')
prt_blu = lambda s: cprint(s, 'blue')

FILE = sys.argv[1] #"kevin.json"

lines = []
with open(FILE, "r") as f:
    lines = [json.loads(l.strip()) for l in f.readlines()]

for article in lines:
    prt_grn(article["title"] + ": " + article["desc"])
    result = input("Enter 1 for positive, 2 for negative, 3 for neutral: ")
    while not result.isdigit(): result = input("Bad input; Enter 1 for positive, 2 for negative, 3 for neutral: ")

    result = int(result)
    with open(FILE.rstrip(".json") + "_results.json", "a+") as n:
        article["sentiment"] = "positive" if result == 1 else "negative" if result == 2 else "neutral" 
        n.write(json.dumps(article) + "\n")
