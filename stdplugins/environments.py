from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import  SYNTAX, MODULE_LIST
import asyncio
from selenium import webdriver
import os
import time
import io
import requests
from PIL import Image
import hashlib
MODULE_LIST.append("test (image search query)")

def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))
@borg.on(admin_cmd(pattern="img (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("test "+input_str)
    