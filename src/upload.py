from dotenv import load_dotenv
load_dotenv()
import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import google

from utils import get_datetime

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main(links, summaries):
  print("Start Upload")
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
  youtube = get_auth()
  upload(youtube, links, summaries)
  print("Done Upload")


def get_auth():
  api_service_name = "youtube"
  api_version = "v3"

  # 初回の token 取得用
  # client_secrets_file = "../client_secrets.json"
  # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
  #   client_secrets_file, scopes, redirect_uri='http://localhost')
  # credentials = flow.run_local_server()
  # print(credentials)
  # print(credentials.to_json())

  with open("../data/token/youtube.json") as f:
    pre_token = json.loads(f.read())
    pre_token['client_id'] = os.getenv('YOUTUBE_CLIENT_ID')
    pre_token['client_secret'] = os.getenv('YOUTUBE_CLIENT_SECRET')
  
  credentials = google.oauth2.credentials.Credentials(
    token=None, 
    **pre_token
  )
  http_request = google.auth.transport.requests.Request()
  credentials.refresh(http_request)

  next_token = json.loads(credentials.to_json())
  del next_token["token"]
  del next_token["client_id"]
  del next_token["client_secret"]
  with open("../data/token/youtube.json", 'w') as f:
    json.dump(next_token, f, indent=2)
    
  youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
  return youtube

def upload(youtube, links, summaries):
  request = youtube.videos().insert(
    part="snippet,status",
    body={
      "snippet": {
        "channelId": "UC71axc_6zVRdD2GGekskalw", # 動画を投稿するチャンネルIDを記載
        "title": f"{get_datetime.get_date()}のITニュース", # 動画のタイトルを設定
        "description": f"マイナビさんの Tech+（https://news.mynavi.jp/techplus/）から引用させていただきました。\n今回参考にさせていただいた記事一覧です。\n {', '.join(links)} \n 文字起こし： \n{summaries}", # 動画の説明を追加
        "tags": [], # タグを追加
        "categoryId": "28", # "19"は「旅行とイベント」のカテゴリ。
        "defaultLanguage": "ja_JP", # タイトルと説明の言語
        "defaultAudioLanguage": "ja_JP", # 動画の言語
      },
      "status": {
        "uploadStatus": "uploaded", # アップロードされたビデオのステータス
        "privacyStatus": "public", # 公開設定は「非公開」
        "license": "youtube", # 標準のYouTubeライセンス
        "embeddable": "true", # 動画の埋め込みを許可する
      },
    },
    media_body=MediaFileUpload("../data/video/video.mp4") # 修正(動画ファイルのパスを記載
  )
  response = request.execute()

  print(response)
  
