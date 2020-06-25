# For The-TG-Bot-3.0
# By @AvinashReddy3108
# Modified by Priyam Kalta 6/21/2020
# Syntax: .ytv <url>, .yta <url>

import os
import time
import math
import asyncio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from telethon.tl.types import DocumentAttributeAudio
from userbot import syntax

@bot.on(command(pattern="yt(a|v) ?(.*)"))
async def download_video(v_url):
    """ For .ytdl command, download media from YouTube and many other sites. """

    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()
    if not url:
    	rep = await v_url.get_reply_message()
    	url = rep.text
    await v_url.edit(f"`Preparing to download {url}`")

    if type == "a":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True

    elif type == "v":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Fetching data..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{DE}`")
        return
    except ContentTooShortError:
        await v_url.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Video is not available in your region.`"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await v_url.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await v_url.edit(f"{type(e)}: {str(e)}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(ytdl_data['duration']),
                                       title=str(ytdl_data['title']),
                                       performer=str(ytdl_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{ytdl_data['title']}.mp3")))

        try:
            os.remove(f"{ytdl_data['id']}.mp4")
            os.remove(f"{ytdl_data['id']}.jpg")
        except Exception as e:
            print("error at deleting file ",e)


        await v_url.delete()
    elif video:
        await v_url.edit(f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{ytdl_data['title']}.mp4")))
        try:
            os.remove(f"{ytdl_data['id']}.mp4")
            os.remove(f"{ytdl_data['id']}.jpg")
        except Exception as e:
            print("error at deleting file ",e)

        await v_url.delete()
        
syntax.update({
    "yta": "\
```.yta <url> [or as a reply to a message to download]```\
\nUsage: Download any youtube video in audio format\
\n\n**Detailed usage of fuction(s):**\
\n\n```.ytv <url> [or as a reply to a message to download]```\
\nUsage: Download the youtube video in video format\
"
})
