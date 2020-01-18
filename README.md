# The_TG_Bot

Customized #UniBorg based on telethon.

## Installing

#### The Easy Way

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### The Legacy Way
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