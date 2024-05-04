# DirkjanBot

Telegram [bot](https://t.me/DailyDirkjanBot) to retrieve [Dirkjan](https://dirkjan.nl/) cartoons (photo format) for various timeframes.

## Info
With this [Telegram](https://telegram.org) bot Dirkjan cartoons can be requested for various timeframes (see [Commands](#commands)). The cartoons are returned as an image with `Dirkjan YYYY-MM-DD` as the description. If no cartoon exists for a date (e.g. on the weekends), or a `.png` link to the image file cannot be found, an error/warning message is returned.

## main.py
This script needs to run to use the bot as a Telegram bot that takes commands.

### Commands
`/datum YYYYMMDD`
Use this command to request the cartoon from a certain date.

`/vandaag`
Use this command to request today's cartoon.

`/week`
Use this command to request all cartoon from the current week (mon-sun).

`/vorigeweek`
Use this command to request all cartoon from the previous week (mon-sun).

## main_single.py
This script fetches the data (cartoons for the past week) and sends them as messages to the provided CHAT_ID. This script won't take commands and only runs once.

## Sources
- Using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- Hosted on Replit, find a working version [here](https://replit.com/@mijnaam/DirkjanBot)
- Using [UptimeRobot](https://uptimerobot.com) to keep the bot running [inspiration](https://youtu.be/SPTfmiYiuok)

# Disclaimer
I do not own Dirkjan or any of the cartoons, I just enjoy the cartoons and wanted an easy way to share them with my friends. You can [contact](https://t.me/mijnaam) me via Telegram.

