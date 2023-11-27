import requests
import importlib
from dotenv import load_dotenv
import ffmpeg
from pydub import AudioSegment
import base64
load_dotenv()
import os
from utils import token_generator
from utils import get_datetime
importlib.reload(token_generator)

systemCommand = "あなたはライターです。今から与える文章を中学生でもわかるように以下の制約条件に従って要約してください。# 制約条件：・500文字以内で出力してください。・敬語で出力してください。"

def main(contents):
  print("Start Convert")
  audio_input = '../data/audio/audio.wav'
  image_input = f'../data/image/{get_datetime.get_date()}.png'
  output_video = '../data/video/video.mp4'
  for i, content in enumerate(contents):
    text_to_speech(content, i)
  concat_audio(contents, audio_input)
  create_video(audio_input, image_input, output_video)
  print("Done Convert")
  return 

def text_to_speech(content, idx):
  target = "textToSpeech"
  generator = token_generator.TokenGenerator(target)
  access_key = generator.get_access_token()
  url = "https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize"
  header = {
    "Authorization": f"Bearer {access_key}",
    "Content-Type": "application/json; charset=utf-8"
  }
  payload =  {
    "audioConfig": {
      "audioEncoding": "LINEAR16", 
      "effectsProfileId": [
        "small-bluetooth-speaker-class-device"
      ],
      "pitch": 0,
      "speakingRate": 1
    },
    "input": {
      "text": content
    },
    "voice": {
      "languageCode": "ja-JP",
      "name": "ja-JP-Neural2-B"
    }
  }
  res = requests.post(url, headers=header, json=payload)
  print(f"res.json:\n {res.json()}")
  with open(f'../data/audio/tmp/audio_{idx}.wav', "w+b") as f:
    encode_string = res.json()["audioContent"]
    decode_string = base64.b64decode(encode_string)
    f.write(decode_string)

def concat_audio(contents, audio_input):
  dir = '../data/audio/tmp'
  for i in range(len(contents)):
    if i == 0:
      audio = AudioSegment.from_file(f'{dir}/audio_{i}.wav', "wav")
    else:
      audio += AudioSegment.from_file(f'{dir}/audio_{i}.wav', "wav")
  audio.export(audio_input, format="mp3")
  for f in os.listdir(dir):
      os.remove(os.path.join(dir, f))


def create_video(audio_file, image_file, output_file):
  if os.path.exists(output_file):
    os.remove(output_file) 
  input_image = ffmpeg.input(image_file, r=10, loop=1)
  input_audio = ffmpeg.input(audio_file)
  output_ffmpeg = ffmpeg.output(
    input_audio,
    input_image,
    output_file,
    ac=1, 
    shortest=None, 
    vcodec="libx264", 
    pix_fmt="yuv420p", 
    acodec='aac'
  )
  ffmpeg.run(output_ffmpeg)
  return
