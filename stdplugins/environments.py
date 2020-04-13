from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import  SYNTAX, MODULE_LIST
import asyncio
import os
MODULE_LIST.append("getenv")

@borg.on(admin_cmd(pattern="getenv ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    # await event.edit("test "+input_str)
    if input_str :
        reslt=f"Total env variable are **{len(os.environ.keys)}**\n"
        for k in os.environ.keys():
            reslt+=f"```{k}```\n"
        await  event.edit(reslt)

    else:
        try:
            reslt=os.environ.get(input_str,"no such environment variable exist")
            await  event.edit(f"```{input_str}``` -> {reslt}")
        except :
            await event.edit("error getting env variable")
    

@borg.on(admin_cmd(pattern="setenv ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    variable_name = event.pattern_match.group(1)
    if not variable_name:
        abe=await event.get_reply_message()
        env_value=abe.text
        if env_value is None:
            await event.edit("Reply to a environment value you want to set first")
        else:
            os.environ[variable_name]=env_value
            print(f"set the env value {variable_name} to {env_value}")
    else:
        await  event.edit(f"```Give environment variable name first for which you want to set.```")


