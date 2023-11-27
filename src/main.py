import importlib

import scraping
import summarize
import convert
import upload
importlib.reload(scraping)
importlib.reload(summarize)
importlib.reload(convert)
importlib.reload(upload)

def main():
  content_num = 5
  contents, links = scraping.main(content_num)
  summaries = summarize.main(contents)
  convert.main(summaries)
  upload.main(links, summaries)

main()
