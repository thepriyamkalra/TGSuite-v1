@client.on(events(pattern="@(.*)", outgoing=True, no_handler=True))
async def handler(e):
    reply = await e.get_reply_message()
    mentions = e.pattern_match.group(1).split("=>")
    if len(mentions) > 1:
        try:
            user = await client.get_entity(mentions[0].strip())
        except:
            return
        await client.send_message(e.chat_id, f"[{mentions[-1].strip()}](tg://user?id={user.id})", reply_to=reply)
        await e.delete()
        
        
ENV.HELPER.update({
    "mention": "\
```@original => @fake```\
\nUsage: Tag a user with a fake username, for example `@justaprudev => @justanubdev`.\
"
})