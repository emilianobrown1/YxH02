import datetime as d

def get_date():
  return str(d.date.today())

def get_week():
  return d.datetime.now().isocalendar()[1]
