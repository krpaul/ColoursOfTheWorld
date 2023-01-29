from chronological import main, read_prompt, cleaned_completion
import openai

openai.api_key_path = "./key.env"
global first_time
first_time = True

# you can name this function anything you want, the name "logic" is arbitrary
async def logic():
    # if first_time:
    #     # you call the Chronology functions, awaiting the ones that are marked await
    #     prompt = read_prompt('example_prompt')
    #     first_time = False
    # else: 
    prompt = input("Next prompt: ")
    completion = await cleaned_completion(prompt, max_tokens=100, engine="davinci", temperature=0.5, top_p=1, frequency_penalty=0.2, stop=["\n\n"])

    print('Completion Response: {0}'.format(completion))

while True:
    main(logic)

