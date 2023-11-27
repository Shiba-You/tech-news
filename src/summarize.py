import requests
import importlib
from dotenv import load_dotenv
load_dotenv()
import os
import urllib.request
from openai import OpenAI
from utils import get_datetime
importlib.reload(get_datetime)

system_command_summarize = "あなたはライターです。今から与える文章を中学生でもわかるように以下の制約条件に従って要約してください。# 制約条件：・500文字以内で出力してください。・敬語で出力してください。"
system_command_thumbnail = "あなたはプロンプトエンジニアです。Youtubeに上げる動画のサムネイルを、DALL-E-3によって自動生成します。自動生成する際に使用するプロンプトを以下の制約条件に従って出力して下さい。# 制約条件：・200文字以内で出力してください。・人の目を引くような画像をDALL-E-3が出力するためのプロンプトを出力して下さい。・DALL-E-3が出力するサムネイルが、下記の動画内容を加味するようなプロンプトを出力して下さい。# 動画内容："

def main(contents):
  print("Start Summarize")
  summaries = []
  for idx, content in enumerate(contents):
    summary = summarize(content)
    summaries.append(summary)
    if idx == 1:
      get_thumbnail(summary)
  summaries = "            次の話題です。   ".join(summaries)
  summaries_list = []
  i = 0
  batch_size = 200
  while (i+1)*batch_size < len(summaries):
    summaries_list.append(summaries[i*batch_size:(i+1)*batch_size])
    i += 1
  summaries_list.append(summaries[i*batch_size:])
  print("Done Summarize")
  return summaries_list

def summarize(content):
  url = "https://api.openai.com/v1/chat/completions"
  header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
  }
  payload = {
    "model": "gpt-4-1106-preview",
    "messages": [{
        "role": "system", 
        "content": system_command_summarize
      },
      {
        "role": "user", 
        "content": content
      }
    ]}
  res = requests.post(url, headers=header, json=payload)  
  return res.json()["choices"][0]["message"]["content"]

def get_thumbnail(summary):
  client = OpenAI()

  response = client.images.generate(
    model="dall-e-3",
    prompt=system_command_thumbnail + summary,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  result_url = response.data[0].url
  output_path = f'../data/image/{get_datetime.get_date()}.png'
  urllib.request.urlretrieve(result_url, output_path)
