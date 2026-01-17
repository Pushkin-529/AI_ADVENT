import requests
import urllib3
from requests import Response
from twisted.web.html import output

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

system_prompt = "You are a helpful assistant"
user_prompt = {}
model = "GigaChat-2"
temperature = 0.5
max_tokens = 500
top_p = 1
repetition_penalty = 1
access_token = "AQVN2vAegMkW3JL4bEzWDAimcUI6JqkwSw94Mcgp"
query_type = "JSON"
response = {}

def get_model_answer(user_prompt):
  url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
  if query_type == "JSON":
    payload = {
      "modelUri": "gpt://b1guh2uj207c87m7j9t3/yandexgpt-lite",
      "completionOptions": {
        "stream": False,
        "temperature": temperature,
        "maxTokens": max_tokens,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "update_interval": 0
      },
      "messages": [
        {
          "role": "system",
          "text": system_prompt
        },
        {
          "role": "user",
          "text": user_prompt
        }
      ],
      "output_format": "JSON"
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Api-Key ' + access_token
    }
    response = requests.post(url=url, headers=headers, json=payload, verify=False)
    return response.json()
    #['result']['alternatives'][0]['message']['text']

  elif query_type == "XML":
    payload = {
      "modelUri": "gpt://b1guh2uj207c87m7j9t3/yandexgpt-lite",
      "completionOptions": {
        "stream": False,
        "temperature": temperature,
        "maxTokens": max_tokens,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "update_interval": 0,
        "output_format": "XML"
      },
      "messages": [
        {
          "role": "system",
          "text": system_prompt
        },
        {
          "role": "user",
          "text": user_prompt
        }
      ]
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Api-Key ' + access_token
    }
    result = requests.post(url=url, headers=headers, json=payload, verify=False).json()

    xml_output = f'''<?xml version="1.0" encoding="UTF-8"?><?xml version="1.0" encoding="UTF-8"?>
    <root>
      <result>
        <alternatives>
          <message>
            <role>{result["result"]["alternatives"][0]["message"]["role"]}</role>
            <text>{result["result"]["alternatives"][0]["message"]["text"]}</text>
          </message>
          <status>{result["result"]["alternatives"][0]["status"]}</status>
        </alternatives>
        <usage>
          <inputTextTokens>{result["result"]["usage"]["inputTextTokens"]}</inputTextTokens>
          <completionTokens>{result["result"]["usage"]["completionTokens"]}</completionTokens>
          <totalTokens>{result["result"]["usage"]["totalTokens"]}</totalTokens>
          <completionTokensDetails>
             <reasoningTokens>{result["result"]["usage"]["completionTokensDetails"]["reasoningTokens"]}</reasoningTokens>
          </completionTokensDetails>
        </usage>
        <modelVersion>{result["result"]["modelVersion"]}</modelVersion>
      </result>
    </root>
    '''
#    xml_output = f'''<?xml version="1.0" encoding="UTF-8"?>
#      <response>
#          <result>
#              <alternatives>
#                <message>
#                  <role>{result["result"]["alternatives"][0]["message"]["role"]}</role>
#                  <text>{result["result"]["alternatives"][0]["message"]["text"]}</text>
#                </message>
#                <status>{result["result"]["alternatives"][0]["status"]}</status>
#              </alternatives>
#              <usage>
#                <input_tokens>{result["result"]["usage"]["input_tokens"]}</input_tokens>
#                <completion_tokens>{result["result"]["usage"]["completion_tokens"]}</output_tokens>
#                <total_tokens>{result["result"]["usage"]["total_tokens"]}</total_tokens>
#                <completionTokensDetails>
#                  <reasoningTokens>{result["result"]["usage"]["completionTokensDetails"]["reasoningTokens"]}</reasoningTokens>
#                </completionTokensDetails>
#              </usage>
#              <modelVerion>{result["result"]["modelVersion"]}</modelVerion>
#          </result>
#$      </response>'''
    return xml_output

  else:
    return ""


def colored_text(text, color_code):
  return f"\033[{color_code}m{text}\033[0m"

#models = get_models(get_access_token())
print(colored_text(text="Access token obtained! Get model list:", color_code=32))
#print(colored_text(text=models,color_code=32))
print(colored_text(text="Краткая справка по командам: 1-изменение модели, 2-изменение системного промпта, 3-изменение температуры, 4-изменение top_p, 5-изменение repetition_penalty, 6-изменение max_tokens, 7-изменение query_type", color_code=32))
text = {}
while True:
  text = input(colored_text(text="Введите текст запроса к модели: ", color_code=32))
  if text == "exit":
    break
  if text == "1":
    model = input(colored_text(text="Введите название модели: ", color_code=32))
  if text == "2":
    system_prompt = input(colored_text(text="System prompt: ", color_code=32))
    continue
  if text == "3":
    temperature = input(colored_text(text="Enter temperature: ", color_code=32))
    continue
  if text == "4":
    top_p = input(colored_text(text="Enter top_p: ", color_code=32))
    continue
  if text == "5":
    repetition_penalty = input(colored_text(text="Enter repetition_penalty: ", color_code=32))
    continue
  if text == "6":
    max_tokens = input(colored_text(text="Enter max_tokens: ", color_code=32))
    continue
  if text == "7":
    query_type = input(colored_text(text="Enter query_type: ", color_code=32))
    print(colored_text(text="Query type: ", color_code=31) + colored_text(text=query_type, color_code=31))
    continue
  text = get_model_answer(user_prompt=text)
  print(colored_text(text="Ответ модели: ", color_code=32) + colored_text(text=text, color_code=33))


print(colored_text("Спасибо за использование!", "31"))

