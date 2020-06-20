# The-TG-Bot

The-TG-Bot is back with the ultimate v3.0!!

## Requirements
* GIT
```
pkg install git
```
* PYTHON
```
pkg install python
```
* TELETHON
```
pip install telethon
```
* VIRTUAL ENV
```
pip install virtualenv
```

## Connecting to your Telegram Account
```
git clone https://github.com/PriyamKalra/The-TG-Bot-3.0
cd The-TG-Bot-3.0
python3 -m session
```
* Run the above code in terminal
* Enter APP ID, API HASH and phone number conntected to your telegram account
* Enter login code and/or password
* Copy the session and continue to installation

## Installing

#### The Easy Way
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

* Hit the "Deploy to Heroku" button and enter APP ID, API HASH and phone number conntected to your telegram account
* Enter the session copied while connecting your telegram account
* Click on the "Deploy" button on the next page
* After the process is completed, try running .alive on telegram

#### The Legacy Way
* Enter APP ID, API HASH, SESSION in config.py
* Run the code given below in terminal
* After the process is completed, try running .alive on telegram

```
git clone https://github.com/PriyamKalra/The-TG-Bot-3.0
cd The-TG-Bot-3.0
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
python3 -m thetgbot
```

## Note by developer for devlopers
You can use the global variables: bot, command, progres, time_formatter, humanbytes, storage, Config to create your own amazing plugins for this bot.
Here are some tips that will largely help you to understan and create plguins for this bot:

```
@bot.on(command(pattern="<command_to_detect> ?(.*)"))
async def func(var):
<python code>
```
This snippet is used to detect an incoming command like .help, the "var" variable is the snippet respresents the message or the event, which can be modified usinhg various methods. Some of these methods are:

```
arguments = var.pattern_match.group(1)
```
This is used to grab the arguments of an incoming event, like "alive" in ".help alive"

```
reply_msg_id = var.reply_to_msg_id
```
This is used to grab the message which is being replied to by the incoming event (message)

```
await var.edit("Hello World!") #await var.reply("Hello World!")
```
This is used to edit or reply to the event (message) on telegram

You can learn alot more by reading some of the preinstalled plugins, enjoy making your own stuff :P


## Credits
Repositories from which I have taken code to make things work:
(Remind me if I forgot some) 
https://github.com/SpEcHiDe/UniBorg
https://github.com/friendly-telegram/modules-repo
https://github.com/RaphielGang/Telegram-Paperplane