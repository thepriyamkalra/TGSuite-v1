# For The-TG-Bot v3
# Orignally made for PaperPlane Extended by @Three_Cube_TeKnoways
# Modified by Priyam Kalra on 6/21/2020

import os
import sys
import git
import asyncio
import requests


# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "`Looks like a beta build: {branch_name} `"
    "`is being used:\n`"
    "`Please switch to a stable build, and restart the updater.`"
)
OFFICIAL_UPSTREAM_REPO = "https://github.com/PriyamKalra/The-TG-Bot-3.0/"
BOT_IS_UP_TO_DATE = "`The-TG-Bot is up-to-date.\nEnjoy!`"
NEW_BOT_UP_DATE_FOUND = "`The-TG-Bot update is on its way!\nThis should take about 2 minutes, please wait and then try to run .alive`"
REPO_REMOTE_NAME = "updater"
ACTIVE_BRANCH_NAME = "v3"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "`No heroku application found, invalid key provided.`"
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/v3"
INVALID_HEROKU_API_KEY = "INVALID API KEY: To get a valid API key, goto https://dashboard.heroku.com/account \nOn the this website open API key tab.. \nThen click on **REVEAL** button and you will see your **HEROKU API key** \n**Copy and paste that in ENV variable `HEROKU_API_KEY`**"
INVALID_APP_NAME = "INVALID APP NAME: Please set the name of your bot in ENV variable `TG_APP_NAME`"
# -- Constants End -- #


@client.on(register(pattern="update ?(.*)", allow_sudo=True))
async def updater(message):
    await message.edit("Looking for updates // The-TG-Bot v3.0")
    try:
        repo = git.Repo()
    except git.exc.InvalidGitRepositoryError as e:
        repo = git.Repo.init()
        origin = repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(ACTIVE_BRANCH_NAME, origin.refs.v3)
        repo.heads.v3.checkout(True)

    active_branch_name = repo.active_branch.name
    if active_branch_name != ACTIVE_BRANCH_NAME:
        await message.edit(IS_SELECTED_DIFFERENT_BRANCH.format(
            branch_name=active_branch_name
        ))
        return False

    try:
        repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
    except Exception as e:
        print(e)
        pass

    temp_upstream_remote = repo.remote(REPO_REMOTE_NAME)
    temp_upstream_remote.fetch(active_branch_name)

    if Config.HEROKU_API_KEY is not None:
        import heroku3
        logger.info("Heroku API Key: " + Config.HEROKU_API_KEY)
        heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            logger.info("Heroku APP: " + f"{Config.TG_APP_NAME}")
            heroku_app = None
            for i in heroku_applications:
                if i.name == Config.TG_APP_NAME:
                    heroku_app = i
            if heroku_app is None:
                try:
                    heroku_app = heroku_applications[0]
                except:
                    await message.edit(INVALID_APP_NAME)
                    return
            heroku_git_url = heroku_app.git_url.replace(
                "https://",
                "https://api:" + Config.HEROKU_API_KEY + "@"
            )
            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)
            await message.edit(NEW_BOT_UP_DATE_FOUND)    
            asyncio.get_event_loop().create_task(
                deploy_start(bot, message, HEROKU_GIT_REF_SPEC, remote))
        else:
            await message.edit(NO_HEROKU_APP_CFGD)
    else:
        await message.edit(INVALID_HEROKU_API_KEY)


def generate_change_log(git_repo, diff_marker):
    out_put_str = ""
    d_form = "%d/%m/%y"
    for repo_change in git_repo.iter_commits(diff_marker):
        out_put_str += f"•[{repo_change.committed_datetime.strftime(d_form)}]: {repo_change.summary} <{repo_change.author}>\n"
    return out_put_str


async def deploy_start(bot, message, refspec, remote):
    try:
        await remote.push(refspec=refspec)
    except TypeError:
        await message.edit(BOT_IS_UP_TO_DATE)
    await client.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)

Config.HELPER.update({"updater": "\
```.update```\
\nUsage: Update The-TG-Bot to the lastest stable build.\
\n\n**`HEROKU_API_KEY` ENV variable is mandatory:**\
\nTo get a valid API key, goto https://dashboard.heroku.com/account\
\nThen open API key tab..\
\nThen click on **REVEAL** button and you will see your **HEROKU API key**\
\nCopy and paste that in ENV variable `HEROKU_API_KEY`\
\n**If you have more than one heroku apps then setting `TG_APP_NAME` ENV variable is also mandatory:**\
\nSimply copy and paste the bot app name in ENV variable TG_APP_NAME\
"})
