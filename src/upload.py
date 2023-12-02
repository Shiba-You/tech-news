from dotenv import load_dotenv
load_dotenv()
import os
import json
import importlib
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import google
from utils import token_generator
from utils import get_datetime
importlib.reload(token_generator)
importlib.reload(get_datetime)

scopes = ["https://www.googleapis.com/auth/drive"]

def main(links, summaries):
  print("Start Upload")
  print("=======================================")
  print("summaries: ")
  print(summaries)
  print("links: ")
  print(links)
  print("=======================================")
  
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
  drive = get_auth()
  upload(drive)
  print("Done Upload")


def get_auth():
  api_service_name = "drive"
  api_version = "v3"

  # 初回の token 取得用
  # client_secrets_file = "../client_secrets.json"
  # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
  #   client_secrets_file, scopes, redirect_uri='http://localhost')
  # credentials = flow.run_local_server()
  # print(credentials)
  # print(credentials.to_json())

  with open("../data/token/drive.json") as f:
    pre_token = json.loads(f.read())
    pre_token['client_id'] = os.getenv('DRIVE_CLIENT_ID')
    pre_token['client_secret'] = os.getenv('DRIVE_CLIENT_SECRET')
  
  credentials = google.oauth2.credentials.Credentials(
    token=None, 
    **pre_token
  )
  print(pre_token)
  print(credentials)
  http_request = google.auth.transport.requests.Request()
  credentials.refresh(http_request)

  next_token = json.loads(credentials.to_json())
  del next_token["token"]
  del next_token["client_id"]
  del next_token["client_secret"]
  with open("../data/token/drive.json", 'w') as f:
    json.dump(next_token, f, indent=2)
    
  drive = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
  return drive

def upload(drive):
  file_metadata = {
    'name': f"{get_datetime.get_date()}のITニュース",
    'parents': ['1Tl3K8WXe-hz4qQ7s-oirk11I1Xy-7P_3']
  }
  media = MediaFileUpload(
    '../data/video/video.mp4', 
    mimetype='video/mp4', 
    resumable=True
  )
  file = drive.files().create(
    body=file_metadata, media_body=media, fields='id'
  ).execute()
  print ('Folder ID: %s' % file.get('id'))
  
  
