from bs4 import BeautifulSoup
import requests

def main(content_num):
  print("Start Scraping")
  target_url = ['https://news.mynavi.jp/techplus/']
  links = get_contents(target_url, "article-content", "href")
  texts = get_contents(links, "article-body", "text")
  print("Done Scraping")
  return texts[:content_num], links[:content_num]

def get_contents(urls, class_, attr):
  session = requests.session()
  contents = []

  for url in urls:
    res = session.get(url)
    bs = BeautifulSoup(res.text, "html.parser")
    elems = bs.find_all(True, class_=class_)
    for elme in elems:
      if (attr == "text"):
        contents.append(elme.get_text().replace('\n', ''))
      else: 
        contents.append(elme.get(attr))
    
  session.close()
  return contents
