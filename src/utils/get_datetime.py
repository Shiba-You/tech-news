import datetime

def get_date():
  dt_now = datetime.datetime.now()
  return dt_now.strftime('%Y年%m月%d日')