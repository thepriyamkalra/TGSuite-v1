# For The-TG-Bot

import os
import heroku3

api_key = ENV.HEROKU_API_KEY
app_name = ENV.TG_APP_NAME
heroku = heroku3.from_key(api_key) if api_key and app_name else None
try:
    app = heroku.apps()[ENV.TG_APP_NAME]
except KeyError:
    app = None

@client.on(events(pattern="shutdown"))
async def shutdown(e):
    if heroku is None:
        return await e.edit("`Mind reading .help heroku?`")
    await e.edit("`Scaling to worker@0`")
    if not app:
        return await e.edit("The `TG_APP_NAME` is invalid!")
    app.process_formation()['worker'].scale(0)
    await e.edit(f"`Switched off\nTurn on the `[dynos switch](https://dashboard.heroku.com/apps/{app_name}/resources)` to restart The-TG-Bot`")
     
@client.on(events(pattern="update ?(.*)", allow_sudo=True))
async def update(e):
        if not heroku:
            return await e.edit("Read `.help heroku` first!")
        if not app:
            return await e.edit("The `TG_APP_NAME` is invalid!")
        app.restart()
        return await e.edit("```The-TG-Bot v3 has been updated, it should be back online in a few seconds.```")


@client.on(events("env (get|set|del) (.*)"))
async def env_variables(event):
    if heroku is None: 
        return await event.edit("bruh, checkout `.help heroku`")
    if not app:
        return await event.edit("The `TG_APP_NAME` is invalid!")
    command = event.pattern_match.group(1)
    args = event.pattern_match.group(2)
    env = app.config()
    if command == "get":
        args = args.upper()
        if args in env:
            await event.edit(f"Key: `{args}`\nValue: `{env[args]}`")
        else:
            await event.edit(f"ENV Variable `{args}` doesn't exist!")
    elif command == "set":
        configs = {}
        message = ""
        for config in args.split(";"):
            key = config.strip().split()[0]
            value = config.strip().split()[1]
            configs.update({key: value})
            message += f"Key: `{key}`\nValue: `{value}`\n\n"
        env.update(configs)
        await event.edit("**Modified/new env variables:**\n\n" + message)
    elif command == "del":
        del env[args]
        await event.edit(f"Deleted env variable `{args}`")
        

@client.on(events("logs ?(.*)", allow_sudo=True))
async def heroku_logs(event):
    if heroku is None:
        return await event.edit("Stop trying to be a bigbrain, just read `.help heroku`!")
    if not app:
        return await event.edit("The `TG_APP_NAME` is invalid!")
    args = event.pattern_match.group(1)
    if args:
        try: lines = int(args)
        except: return await event.edit("`Count must be an integer`")
    else:
        lines = 100
    logs = app.get_log(lines=lines, timeout=10)
    with open(f"{app_name}_logs.txt", "w") as f:
        f.write(logs)
    await event.reply(f"Recent logs for {app_name}", file=f.name, silent=True)
    await event.delete()
    os.remove(f.name)
   
        
        
ENV.HELPER.update({
    "heroku": "\
```.update```\
\nUsage: Updates the bot to the latest version (exclusive for heroku users).\
\n\n`.shutdown`\
\nUsage: Turns off the the bot by turning off dynos.\
\n\n`.env get [key]`\
\nUsage: Return the value of an env variable.\
\n\n`.env set [key] [value]`\
\nUsage: Sets a new env variable or updates an existing variable.\
\nSeperate with `;` to set multiple variables at once.\
\n\n`.env del [key]`\
\nUsage: Deletes an env variable.\
\n\n`.logs [number of lines (optional), default: 100]`\
\nUsage: Sends logs as a .txt file.\
\n\n\n**NOTE:** This module requires the following env variables:\
\n\n~ `HEROKU_API_KEY` :  __To get a valid API key, goto https://dashboard.heroku.com/account/__\
\n\n~ `TG_APP_NAME` :  __Simply copy and paste the bot app name in ENV variable TG_APP_NAME__\
"
})
