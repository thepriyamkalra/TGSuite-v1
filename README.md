# The-TG-Bot

![LOGO](https://raw.githubusercontent.com/justaprudev/The-TG-Bot/v3/logo.png)


## Disclaimer

```
///
    Your Telegram account may get banned.
    I am not responsible for any improper use of this bot
    This bot is intended for the purpose of having fun with memes,
    as well as efficiently managing groups.
    You ended up spamming groups, getting reported left and right,
    and you ended up in a Finale Battle with Telegram and at the end
    Telegram Team deleted your account?
    And after that, you pointed your fingers at us
    for getting your acoount deleted?
    I will be rolling on the floor laughing at you.
///
```


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

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/justaprudev/The-TG-Bot/tree/heroku)

- Hit the "Deploy to Heroku" button and enter APP ID, API HASH and phone number conntected to your telegram account
- Enter the session copied while connecting your telegram account
- Click on the "Deploy" button on the next page
- After the process is completed, click on "View app"
- Now click on the "Resources" tab
- Then click on the edit/pencil icon
- Finally toggle the switch and hit confirm
- Your bot is now up and running!
- Send .alive in any chat to test it

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

- ENV: A global object which allows access to enviroment variables defined in env.py
- client: A modified version of the telegram client.
- client.storage: A global storage object for the current session.
- events: A simple function that returns a events.NewMessage object.
- progress: Generic progress callback for both uploads and downloads.
- time_formatter: Input time in milliseconds, to get beautified time, as string.
- humanbytes: Input size in bytes, outputs in a human readable format.
- You can learn alot just by reading the telethon [documentory](https://docs.telethon.dev/en/latest/)
- Here is a simple module that adds " world" to the message if you send ".hello".

```
@client.on(events("hello"))
async def handler(event):
	await event.edit(event.text[1:] + " world.")
```

- Enjoy creating your own modules :P

## Credits

- [Telethon](https://github.com/LonamiWebs/Telethon) (Obviously)
- [Uniborg](https://github.com/SpEcHiDe/UniBorg) (The core)
- [FTG modules repo](https://github.com/friendly-telegram/modules-repo)
- [Userge modules repo](https://github.com/UsergeTeam/Userge-Plugins)
- [PPE](https://github.com/RaphielGang/Telegram-Paperplane)