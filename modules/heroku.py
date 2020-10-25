# For The-TG-Bot

import os
import heroku3

api_key = ENV.HEROKU_API_KEY
app_name = ENV.TG_APP_NAME
heroku = heroku3.from_key(api_key) if api_key and app_name else None


@client.on(events(pattern="shutdown", allow_sudo=True))
async def scale_zero(e):
    if heroku is None:
        return await e.edit("`Mind reading the help?`")
    await e.edit("`Scaling to worker@0`")
    app = heroku.apps()[app_name]
    app.process_formation()['worker'].scale(0)
    await e.edit(f"`Switched off\nTurn on the `[dynos switch](https://dashboard.heroku.com/apps/{app_name}/resources)` to restart The-TG-Bot`")
     
     
@client.on(events(pattern="restart ?(.*)", allow_sudo=True))
async def _restart(message):
    args = message.pattern_match.group(1)
    if "-h" in args:
        if heroku is None:
            return await message.edit("Read `.help core` first!")
        app = heroku.apps()[app_name]
        app.restart()
        return await message.edit("`The-TG-Bot v3 has been updated and the heroku app has been restarted, it should be back online in a few seconds.`")
    await message.edit("`The-TG-Bot v3 has been restarted.\nTry .alive or .ping to check if its alive.`")
    client.sync(restart)  # await restart() random crash workaround


@client.on(events("env (get|set|del) (.*)"))
async def env_variables(event):
    if heroku is None: 
        return await event.edit("`Like I care.`")
    command = event.pattern_match.group(1)
    args = event.pattern_match.group(2)
    env = heroku.apps()[app_name].config()
    if command == "get":
        args = args.upper()
        if args in env:
            await event.edit(f"Key: `{args}`\nValue: `{env[args]}`")
        else:
            await event.edit(f"ENV Variable `{args}` doesn't exist!")
    elif command == "set":
        configs = {}
        message = ""
        # SYNTAX: key value ; key value ; key value ; etc.
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
        

@client.on(events("logs ?(.*)"))
async def heroku_logs(event):
    if heroku is None:
        return await event.edit("`Can you set the required env vars for good?`")
    args = event.pattern_match.group(1)
    if args:
        try: lines = int(args)
        except: return await event.edit("`Count must be an integer`")
    else:
        lines = 1500
    logs = heroku.apps()[app_name].get_log(lines=lines, timeout=10)
    with open(f"{app_name}_logs.txt", "w") as f:
        f.write(logs)
    await event.reply(f"Recent logs for {app_name}", file=f.name, silent=True)
    await event.delete()
    os.remove(f.name)
  

async def restart():
    await client.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
   
        
        
ENV.HELPER.update({
    "heroku": "\
`.restart`\
\nUsage: Restart the telegram client.\
\n\n`.restart [-h/-heroku]`\
\nUsage: Restart the heroku app and update the bot to the latest version.\
\n\n`.shutdown`\
\nUsage: Turns off the the bot by turning off dynos.\
\n\n`.env get [key]`\
\nUsage: Return the value of an env variable.\
\n\n`.env set [key] [value]`\
\nUsage: Sets a new env variable or updates an existing variable.\
\nSeperate with `;` to set multiple variables at once.\
\n\n`.env del [key]`\
\nUsage: Deletes an env variable.\
\n\n`.logs [number of lines (optional)]`\
\nUsage: Sends logs as a .txt file.\
\n\n\n**NOTE:** This module requires the following env variables:\
\n\n~ `HEROKU_API_KEY` :  __To get a valid API key, goto https://dashboard.heroku.com/account/__\
\n\n~ `TG_APP_NAME` :  __Simply copy and paste the bot app name in ENV variable TG_APP_NAME__\
"
})
