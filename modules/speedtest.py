"""Check your internet speed powered by speedtest.net
Syntax: .speedtest
Available Options: image, file, text
Source: https://github.com/SpEcHiDe/Uniborg/blob/master/stdplugins/speedtest.py
Modified by @PriyamKalra - 6/19/2020"""

from datetime import datetime
import io
import speedtest



@client.on(events(pattern="speedtest ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    as_text = True
    as_document = False
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    await event.edit("Calculating server internet speed. Please wait!")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await event.edit("""Speedtest results:
Download: {}
Upload: {}
Ping: {}
Internet Service Provider: {}
ISP Rating: {}""".format(convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, i_s_p, i_s_p_rating))
        else:
            await client.send_file(
                event.chat_id,
                speedtest_image,
                caption="Speedtest results:",
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False
            )
            await event.delete()
    except Exception as exc:
        await event.edit("""Speedtest results:
Download: {}
Upload: {}
Ping: {}
With the Following ERRORs:
{}""".format(convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, str(exc)))


def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"
    }
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


ENV.HELPER.update({
    "speedtest": "\
```.speedtest <mode>```\
\nUsage: ```Get download and upload speed of your server.\
\nAvailable modes:\
\nfile: Send test results as a png file.\
\nimage: Send test results as a telegram media image.\
\ntext: Send test results as a text message.\
\nDefault mode: text."
})
