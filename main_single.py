def get_cartoon_url_from_date(cartoon_date, base_url="https://dirkjan.nl/cartoon/"):
  """ Get cartoon from date YYYYMMDD """

  # Try to format the entered date
  try:
    date = datetime.strptime(cartoon_date, "%Y%m%d")
  except ValueError:
    return "Geef een geldige datum mee"

  # Some date formats for the cartoon
  day_url = date.strftime("%Y%m%d")
  nice_date = date.strftime("%a %Y-%m-%d")
  png_name = date.strftime(f"Dirkjan {nice_date}")

  # Try to open the URL and decode content
  try:
    resp = request.urlopen(base_url + day_url)
    content = resp.read().decode()
  except error.HTTPError:
    return None, f"Geen cartoon gevonden voor deze datum: {nice_date}"

  # Regex to find the png url
  r = fr"<meta property=\"og:image\" content=\"https:\/\/dirkjan\.nl\/wp-content\/uploads\/20[0-9][0-9]\/[0-1][0-9]\/[a-z0-9]+\.png"

  if png_url := search(r, content)[0].split('content="')[1]:
    return png_url, png_name
  else:
    return None, f"Geen .png URL gevonden voor deze cartoon: {nice_date}"


def main():
  # Inspiration: https://stackoverflow.com/a/56163328
  # Today's date
  today = date.today()
  # Current weekday
  weekday = today.isoweekday() - 1
  # Start of the week
  start = today - timedelta(days=weekday)
  # Current week days
  dates = [start + timedelta(days=d) for d in range(7)]

  for day in dates:
    requested_date = day.strftime("%Y%m%d")

    png_url, png_name = get_cartoon_url_from_date(requested_date)

    if png_url:
      bot.send_photo(CHAT_ID, photo=png_url, caption=png_name)
    else:
      bot.send_message(CHAT_ID, png_name)

  return


if __name__ == "__main__":
    from datetime import datetime, timedelta, date

    if (wkday := datetime.now().weekday()) == 4:
      import os
      from urllib import request, error
      from re import search

      # Telebot to make this work with a Telegram bot
      # https://github.com/eternnoir/pyTelegramBotAPI
      import telebot

      API_KEY = os.environ['API_KEY']
      CHAT_ID = os.environ['CHAT_ID']

      bot = telebot.TeleBot(API_KEY)

      main()
    else:
      print(f"Vandaag is dag {wkday}, geen cartoons")
