from bs4 import BeautifulSoup
import lxml.html.clean as clean
import requests
Links = []
def shortenHTML(html):

    #open("HTML.htm", 'w').write(str(html))
    
    parsed = BeautifulSoup(html, "html.parser")
    for data in parsed(['script', 'head', 'meta', 'img']):
        data.decompose()
    


    safe_attrs = clean.defs.safe_attrs
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
    
    out = cleaner.clean_html(parsed.decode())
    for data in parsed(['a']):
        Links.append(str(data))
    

    out = BeautifulSoup(out, "html.parser").get_text()
    #open("Text.htm", 'w').write(out)

    return out

from googlesearch import search

#results = search("This is my query")


import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def processResult(page):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[{'role': 'system', 'content': 'summarize the article'}, {'role': 'user', 'content': page}],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        ).choices[0].message.content
    except:
        print("Oopsie! Looks like the page was way too colossal for ChatGPT's teeny-tiny brain, and it got a little overwhelmed.")
        response = ""
    return response

def searchGPT(query):
    print(query)
    return "The latest google pixel is the pixel fold"

    results = []
    for url in search(query, stop=3):
        
        results.append(processResult(shortenHTML(requests.get("http://www.androidpolice.com/google-pixel-7-review", headers={
            "User-Agent" : "waterwolf/5.0 (WinX11; DebintumindoradroidOS Armx86_64v8) BananaWebKit/537.36 (KHTML, like Gecko) Chrome/-1.0.2704.103 Safari/537.36"
        }).text)))
        
    #decide response
    messages = [{'role': 'system', 'content': 'use ONLY the given search results to respond to the query: ' + query}]
    out = ""
    file = open("promptTest.txt", "w")
    for txt in results:
        messages.append({'role': 'user', 'content': txt})

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    ).choices[0].message.content
    return response