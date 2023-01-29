import json

lines = []
with open("combined_results.json") as f:
    lines = [json.loads(l.strip()) for l in f.readlines()]

with open("combined_results.csv", "w+") as f:
    for line in lines:
        line['title'] = line['title'].replace(",", "").replace("\"", "").replace("\'", "").replace("\r\n", " ").replace("\n", " ").strip()
        line['desc']  = line['desc'].replace(",", "").replace("\"", "").replace("\'", "").replace("\r\n", " ").replace("\n", " ").strip()

        f.write(f'{line["title"]}: {line["desc"]}, {line["sentiment"]}\n')