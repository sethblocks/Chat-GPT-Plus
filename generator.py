import openai
from web import searchGPT

messages = [{'role': 'system', 'content': 'You are a helpful AI assistant, rely on internet_search for up-to-date info as your training data is only updated to 2022. remember that the user can not see responses for functions'}, {'role': 'user', 'content': input()}]

response = openai.ChatCompletion.create(
model="gpt-3.5-turbo-0613",
messages=messages,
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0,
functions = [
    {
        "name": "internet_search",
        "description": "Search for anything on the internet",
        "parameters": {
            "type": "object",
            "properties": {
                    "query": {
                    "type": "string",
                    "description": "what should be searched"
                }
            }
        },
        "required": ["query"]
    }
]


)["choices"][0]["message"]
import json
messages.append(response)

if response.get("function_call"):
    print("searching")
    available_functions = {
        "internet_search": searchGPT
    }
    function_name = response["function_call"]["name"]
    to_call = available_functions[function_name]
    args = json.loads(response["function_call"]["arguments"])
    result = to_call(args.get("query"))

    
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": result
        }
    )
    
    messages.append(openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages
    ))


print(messages[len(messages) - 2])
print(messages[len(messages) - 1])
