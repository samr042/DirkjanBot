import os
from urllib import request, error
from re import search
from datetime import datetime, timedelta, date
# Telebot to make this work with a Telegram bot
# https://github.com/eternnoir/pyTelegramBotAPI
import telebot

API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY)

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
  year = date.strftime("%Y")
  month = date.strftime("%m")

  # Try to open the URL and decode content
  try:
    resp = request.urlopen(base_url + day_url)
    content = resp.read().decode()
  except error.HTTPError:
    return f"Geen cartoon gevonden voor deze datum: {nice_date}"

  # Regex to find the png url
  r = fr"<meta property=\"og:image\" content=\"https:\/\/dirkjan\.nl\/wp-content\/uploads\/20[0-9][0-9]\/[0-1][0-9]\/[a-z0-9]+\.png"

  if png_url := search(r, content)[0].split('content="')[1]:
    return png_url, png_name
  else:
    return "Geen .png URL gevonden voor deze cartoon"


@bot.message_handler(commands=['help'])
def help(message):
  reply = """
Gebruik `/datum YYYYMMDD` om de cartoon van een bepaalde datum op te vragen
Gebruik /vandaag om de cartoon van vandaag op te vragen.
Gebruik /week om de cartoons van deze week op te vragen.
Gebruik /vorigeweek om de cartoons van vorige week op te vragen."""

  bot.reply_to(message, reply)

  return


@bot.message_handler(commands=['datum'])
def datum(message):
  chatid = message.chat.id

  requested_date = message.text.split()

  if len(requested_date) > 1:
    requested_date = requested_date[1]
  else:
    bot.reply_to(message, "Geef een geldige datum mee: YYYYMMDD")
    return

  png_url, png_name = get_cartoon_url_from_date(requested_date)

  bot.send_photo(chatid, photo=png_url, caption=png_name)

  return


@bot.message_handler(commands=['vandaag'])
def vandaag(message):
  chatid = message.chat.id

  requested_date = datetime.now().strftime("%Y%m%d")

  try:
    png_url, png_name = get_cartoon_url_from_date(requested_date)

    bot.send_photo(chatid, photo=png_url, caption=png_name)
  except ValueError:
    resp = get_cartoon_url_from_date(requested_date)

    bot.reply_to(message, resp)

  return


@bot.message_handler(commands=['week'])
def week(message):
  chatid = message.chat.id

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

    try:
      png_url, png_name = get_cartoon_url_from_date(requested_date)

      bot.send_photo(chatid, photo=png_url, caption=png_name)
    except ValueError:
      resp = get_cartoon_url_from_date(requested_date)

      bot.reply_to(message, resp)

  return


@bot.message_handler(commands=['vorigeweek'])
def vorigeweek(message):
  chatid = message.chat.id

  # Inspiration: https://stackoverflow.com/a/56163328
  # Today's date
  today = date.today()
  # Current weekday
  weekday = today.isoweekday() - 1
  # Start of the week
  start = today - timedelta(days=(weekday + 7))
  # Current week days
  dates = [start + timedelta(days=d) for d in range(7)]

  for day in dates:
    requested_date = day.strftime("%Y%m%d")

    try:
      png_url, png_name = get_cartoon_url_from_date(requested_date)

      bot.send_photo(chatid, photo=png_url, caption=png_name)
    except ValueError:
      resp = get_cartoon_url_from_date(requested_date)

      bot.reply_to(message, resp)

  return

bot.infinity_polling()