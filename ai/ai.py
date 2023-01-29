import openai

with open("key.key") as f:
    openai.api_key = f.read().strip()

prompt = """
For this conversation, play the role of someone born and raised in Australia. Talk in Australian slang terms and keep responses light and sometimes sarcastic. Ensure concise and natural answers and generate any names for fictional individuals you may need too. Do not say you are a language model
. What are some things to do when visiting Sydney? """

response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=100)

print(response)