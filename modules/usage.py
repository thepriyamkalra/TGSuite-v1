# The below code is a copy of https://github.com/UsergeTeam/Userge-Plugins/blob/master/plugins/usage.py
# It may be modified to suit the needs of the current environment

import math
import asyncio
import heroku3
import requests

# ================= CONSTANTS =================
Heroku = heroku3.from_key(ENV.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = f" for **{ENV.TG_APP_NAME}**" if ENV.TG_APP_NAME is not None else ""
HEROKU_API_KEY = ENV.HEROKU_API_KEY
# ================= CONSTANTS =================


@client.on(events("usage"))
async def usage(message):
    await message.edit("`Calling Heroku's CEO..`")
    await asyncio.sleep(0.5)
    if HEROKU_API_KEY is None:
    	await message.edit("`The CEO says you need to set the HEROKU_API_KEY environment variable first. Checkout .help usage`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36')
    u_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await message.edit("`Error: something bad happened`\n\n"
                                  f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    await message.edit(f" -> `Dyno usage`{HEROKU_APP_NAME}:\n"
                       f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                       f"**|**  [`{AppPercentage}`**%**]"
                       "\n"
                       " -> `Dyno hours quota remaining this month`:\n"
                       f"     •  `{hours}`**h**  `{minutes}`**m**  "
                       f"**|**  [`{percentage}`**%**]")

                       
ENV.HELPER.update({"usage": "\
```.usage```\
\nUsage: Findout if your bot is going to die soon or not.\
\n\n**`HEROKU_API_KEY` ENV variable is mandatory:**\
\nTo get a valid API key, goto https://dashboard.heroku.com/account\
\nThen open API key tab..\
\nThen click on **REVEAL** button and you will see your **HEROKU API key**\
\nCopy and paste that in ENV variable `HEROKU_API_KEY`\
\n**`TG_APP_NAME` ENV variable is not mandatory but will make the output look better:**\
\nSimply copy and paste the bot app name in ENV variable TG_APP_NAME\
"})                       