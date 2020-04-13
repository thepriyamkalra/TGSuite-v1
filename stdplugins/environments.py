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
    if not input_str :
        reslt=f"Total env variable are **{len(os.environ.keys())}**\n"
        for k in sorted(os.environ.keys()):
            reslt+=f"```{k}``` \n"
        await  event.edit(reslt)

    else:
        try:
            reslt=os.environ.get(input_str,"no such environment variable exist")
            await  event.edit(f"```{input_str}``` -> ```{reslt}```")
        except :
            await event.edit("error getting env variable")
    

@borg.on(admin_cmd(pattern="setenv ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    variable_name = event.pattern_match.group(1)
    if variable_name:
        abe=await event.get_reply_message()
        try:
            env_value=abe.text
            os.environ[variable_name]=env_value
            logger.info(f"set the env value {variable_name} to {env_value}")
            await  event.edit(f"set the value ```{env_value}``` for ```{variable_name}``` is **successfull**")
        except :
            await event.edit(f"Reply to a environment value you want to set first for ```{variable_name}```")

    else:
        await  event.edit(f"```Give environment variable name first for which you want to set.```")


