# BEAST_BOT REBORN V 2.0+
**based on telethon 1.11.3**
Customized #UniBorg based on telethon.

## How to use

#### Step1: 

goto [my.telegram.org/apps](https://telegram.org/apps) **use VPN in india to access the site**


#### step2: login and setup the app ..


you will get **APP ID**  and **APP HASH** copy these two value at safe place (you will need later)

**Figure for reference**

![APP_ID and APP_HASH ](https://i.ibb.co/CwPdL7c/app-id-hash.jpg)

#### Important Setup steps( very much imp)

##### step 2.1: clone this repo and pip install telethon first...

> git clone https://github.com/authoritydmc/BEASTBOT-REBORN.git 


using python's pip install telethon.. 

> pip install telethon

##### step2.2 run 
> python session_strings.py

##### step2.3 enter your mobile number with country code for eg +919876543210

##### step 2.4 enter the code you received 

##### step 2.5 you will get a string as a response starting with something like 1Bqvt......

 copy this String somwhere safe .this is your **HU_STRING_SESSION** value

#### step3: Create an account on [Heroku.com](https://heroku.com)

#### step4: click on deploy button

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### step5 : Fill in all the Three required Value you copied and app name(anything) ..and finally click on deploy.



![heroku setting page ](https://i.ibb.co/B2RPWWn/heroku-setting.jpg)
![heroku setting page](https://i.ibb.co/YPFkpzR/heroku-settting2.jpg)

#### Finished .. your bot must be up and running by now..

## NOT FOR DEPLOYERS... below information only for Developers and Collaborators

### Installing


Simply clone the repository and run the main file:
```sh
git clone https://github.com/uniborg/uniborg.git
cd uniborg
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
# <Create config.py with variables as given below>
python3 -m stdborg
```

An example `config.py` file could be:

**Not All of the variables are mandatory**

__The UniBorg should work by setting only the first two variables__

```python3
from sample_config import Config

class Development(Config):
  APP_ID = 6
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
  TG_BOT_TOKEN_BF_HER = ""
  TG_BOT_USER_NAME_BF_HER = ""
  UB_BLACK_LIST_CHAT = []
  # chat ids or usernames, it is recommended to use chat ids,
  # providing usernames means an additional overhead for the user
  CHATS_TO_MONITOR_FOR_ANTI_FLOOD = []
  # specify LOAD and NO_LOAD
  LOAD = []
  NO_LOAD = []
```
