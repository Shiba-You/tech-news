import requests
from dotenv import load_dotenv
load_dotenv()
import os

class TokenGenerator():
  def __init__(self, target):
    with open(f"../data/token/{target}.txt") as f:
      self.refresh_token = f.read()
      self.access_token = ""
  
  def get_access_token(self):
    url = "https://www.googleapis.com/oauth2/v4/token"
    payload = {
      "client_secret": os.getenv('TEXT_TO_SPEECH_CLIENT_SECRET'),
      "grant_type": "refresh_token",
      "refresh_token": self.refresh_token,
      "client_id": os.getenv('TEXT_TO_SPEECH_CLIENT_ID')
    }

    res = requests.post(url, json=payload)
    return res.json()["access_token"]
