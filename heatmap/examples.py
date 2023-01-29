from cohere.classify import Example
import json

examples = []
with open("classification/combined_results.json") as f:
    lines = f.readlines()
    lines = [json.loads(l) for l in lines]

    for line in lines: 
        examples.append(
            Example(line["title"] + ": " + line["desc"], line["sentiment"])
        )
