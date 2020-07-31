# The-TG-Bot

![LOGO](https://raw.githubusercontent.com/justaprudev/The-TG-Bot/v3/logo.png)

The-TG-Bot is back with the ultimate v3!!

## Requirements

- openssl

```
pkg install openssl
```

- git

```
pkg install git
```

- python

```
pkg install python
```

- telethon

```
pip install telethon
```

- virtualenv

```
pip install virtualenv
```

## Connecting to your Telegram Account

```
git clone https://github.com/justaprudev/The-TG-Bot
cd The-TG-Bot
python3 -m session
```

- Run the above code in terminal
- Enter APP ID, API HASH and phone number conntected to your telegram account
- Enter login code and/or password
- Copy the session and continue to installation

## Installing

#### The Easy Way

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/justaprudev/The-TG-Bot/tree/v3)

- Hit the "Deploy to Heroku" button and enter APP ID, API HASH and phone number conntected to your telegram account
- Enter the session copied while connecting your telegram account
- Click on the "Deploy" button on the next page
- After the process is completed, try running .alive on telegram

#### The Legacy Way

- Enter APP ID, API HASH, SESSION in production.py
- Run the code given below in terminal
- After the process is completed, try running .alive on telegram

```
git clone https://github.com/justaprudev/The-TG-Bot
cd The-TG-Bot
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
python3 -m thetgbot
```

## Read the docs

Here are the most useful "global" variables that can be used on any module you create:

- Config: The class which allows access to enviroment variables defined in production.py
- client: A modified version of the telegram client.
- register: Use this with the telegram client to make your life a little easier, example:

```
@client.on(register("hello"))
async def handler(event):
	await event.reply("world")
```

- progress: Generic progress callback for both uploads and downloads.
- time_formatter: Input time in milliseconds, to get beautified time, as string.
- humanbytes: Input size in bytes, outputs in a human readable format.
- storage: A global storage dictionary for the current session.
- You can learn alot just by reading the telethon [documentory](https://docs.telethon.dev/en/latest/)
- Enjoy creating your own modules :P

## Credits

- [Telethon](https://github.com/LonamiWebs/Telethon) (Obviously)
- [Uniborg](https://github.com/SpEcHiDe/UniBorg) (The core)
- [FTG modules repo](https://github.com/friendly-telegram/modules-repo)
- [PPE](https://github.com/RaphielGang/Telegram-Paperplane)