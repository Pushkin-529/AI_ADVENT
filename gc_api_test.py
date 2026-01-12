import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

system_prompt = "You are a helpful assistant"
user_prompt = {}
model = "GigaChat-2"
temperature = 0.5
max_tokens = 100
top_p = 1
repetition_penalty = 1

def get_access_token():
  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  payload = {
    'scope': 'GIGACHAT_API_PERS'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': '9e817178-87e7-4b5f-9ed6-a56a141144e0',
    'Authorization': 'Basic MDE5YmIzMjItNjgxOC03YzhmLWJmYjQtYWVkY2Q0MjZmZGRiOjQ5NDRkOGI0LTI3OGMtNGQyOC1hMmJjLTRiZTkzOWI3MGU0NA=='
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  access_token = response.json()['access_token']
  #print(access_token)
  return access_token

def get_models(access_token):
  url = "https://gigachat.devices.sberbank.ru/api/v1/models"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("GET", url, headers=headers, data=payload,verify=False)
  data = response.json()['data']
  return data

def get_model_answer(access_token,user_prompt):
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = {
    "model": model,
    "messages": [
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": user_prompt
      }
    ],
    "temperature": temperature,
    "max_tokens": max_tokens,
    "top_p": top_p,
    "repetition_penalty": repetition_penalty,
    "update_interval": 0,
    "stream": False
  }
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.post(url=url, headers=headers, json=payload,verify=False)
  return response.json()['choices'][0]['message']['content']

def colored_text(text, color_code):
  return f"\033[{color_code}m{text}\033[0m"

models = get_models(get_access_token())
print(colored_text(text="Access token obtained! Get model list:", color_code=32))
print(colored_text(text=models,color_code=32))
print(colored_text(text="Краткая справка по командам: 1-изменение модели, 2-изменение системного промпта, 3-изменение температуры, 4-изменение top_p, 5-изменение repetition_penalty, 6-изменение max_tokens", color_code=32))
text = {}
while True:
  text = input(colored_text(text="Введите текст запроса к модели: ", color_code=32))
  if text == "exit":
    break
  if text == "1":
    model = input(colored_text(text="Введите название модели: ", color_code=32))
  if text == "2":
    system_prompt = input(colored_text(text="System prompt: ", color_code=32))
  if text == "3":
    temperature = input(colored_text(text="Enter temperature: ", color_code=32))
  if text == "4":
    top_p = input(colored_text(text="Enter top_p: ", color_code=32))
  if text == "5":
    repetition_penalty = input(colored_text(text="Enter repetition_penalty: ", color_code=32))
  if text == "6":
    max_tokens = input(colored_text(text="Enter max_tokens: ", color_code=32))
  text = get_model_answer(access_token=get_access_token(), user_prompt=text)
  print(colored_text(text="Ответ модели: ", color_code=32) + colored_text(text=text, color_code=33))


print(colored_text("Спасибо за использование!", "31"))

