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
    r = fr"<meta property=\"og:image\" content=\"https:\/\/dirkjan\.nl\/wp-content\/uploads\/20[0-9][0-9]\/[0-1][0-9]\/[a-z0-9]+\.jpg"

    if png_url := search(r, content)[0].split('content="')[1]:
        return png_url, png_name
    else:
        return None, f"Geen .png URL gevonden voor deze cartoon: {nice_date}"


def getWeekdayOnline():
    resp = request.urlopen(
        'https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterdam'
    )

    current_day = json.loads(
        resp.read().decode()
    )["dayOfWeek"]

    return current_day == "Friday"


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
        print("loading packages")
        from datetime import datetime, timedelta, date
        import os
        from urllib import request, error
        from re import search
        from time import sleep
        import json

        # Telebot to make this work with a Telegram bot
        # https://github.com/eternnoir/pyTelegramBotAPI
        import telebot

        print("loading keys")
        API_KEY = os.environ['API_KEY']
        CHAT_ID = os.environ['CHAT_ID']

        # Number of connection tries
        tries = 0
        # Sleep time after failed connection attempt
        s_time = 5

        bot = telebot.TeleBot(API_KEY)

        print("starting while")
        while tries < 30:
            try:
                tries += 1

                # If weekday is day 4 (friday)
                if getWeekdayOnline():
                    print(f"{tries} tries, finally success.\n")

                    main()
                # else:
                #     bot.send_message(
                #         CHAT_ID,
                #         "Vandaag is geen vrijdag, dus geen cartoons"
                #     )
                #     break

                break
            except request.URLError:
                    print(f"no connection yet ({tries} tries), sleeping {s_time} seconds.")
                    sleep(s_time)