import os
import time
import discord
from discord.ext import commands, tasks
import requests
import random
from duckduckgo_search import DDGS
from openai import AsyncOpenAI
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
import json
import base64
import asyncio
from tls_client import Session
from discord import SyncWebhook
import secrets
import string
import io
import contextlib
import subprocess
from art import *
config = open('config.json')
data = json.load(config)
bot_token = data["token"]
webhook_url = data["webhook"]
bot_prefix = data["prefix"]
webhook_id = data["webhook_id"]
prefix = f"{bot_prefix}"
bot = commands.Bot(command_prefix=prefix, self_bot=True, help_command=None)
token = f"{bot_token}"

#=========|
#         |
#         O
#        /|\
#         /
#=      a u r _ r a

async def checkperms(guild):  #c h e c k   p e r m s
    guild_id = guild.id
    url = f"https://discord.com/api/v9/guilds/{guild_id}/widget"
    headers = {
        "Authorization": token,
        }
    res = requests.get(url, headers=headers)
    code = res.status_code
    match code:
        case 200:
            perms = True
            return perms
        case 403:
            perms = False
            return perms
        case _:
            perms = f"Unknown return code from server {code}"


async def notsobotfunc(guild):
    notsobotid = 439205512425504771
    for member in guild.members:
        if member.id == notsobotid:
            notsobot = True
            return notsobot

async def threadcheck(ctx):
    channel_id = ctx.channel.id
    url = f"https://discord.com/api/v9/channels/{channel_id}/threads"
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        }
    payload = {
        "name":f"test",
        "type":11,
        "auto_archive_duration":4320,
        "location":"Plus Button"
        }
    res = requests.post(url, headers=headers, json=payload)
    status = res.status_code
    resjson = json.loads(res.text)
    if status == 201:
        threadid = resjson["id"]
        url = f"https://discord.com/api/v9/channels/{threadid}"
        requests.delete(url, headers=headers)
        threadbool = True
        return threadbool
    else:
        threadbool = False
        return threadbool

async def webhookcheck(ctx):
    url = "https://discord.com/api/v9/channels/{ctx.channel.id}/webhooks"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        }
    payload = {
        "name": "test"
        }
    res = requests.post(url, headers=headers, json=payload)
    status = res.status_code
    match status:
        case 200:
            webhookbool = True
            return webhookbool
        case _:
            webhookbool = False
            return webhookbool
async def checkimg(ctx):
    try:
        message = await ctx.send(file=discord.File('test.jpg'))
        await message.delete()
        imgbool = True
        return imgbool
    except discord.Forbidden:
        imgbool = False
        return imgbool


@bot.command() #new command lets you check for vulns in the server
async def vuln(ctx):
    guild = ctx.guild
    notsobot = await notsobotfunc(guild)
    if notsobot is None:
        notsobot = False
    perms = await checkperms(guild)
    threadbool = await threadcheck(ctx)
    webhookbool = await webhookcheck(ctx)
    imgbool = await checkimg(ctx)
    vulns = [notsobot, perms, threadbool, webhookbool, imgbool] #this is for later lol idek
    await ctx.send(f"`Results\nNotsobot: {notsobot}\nPerms: {perms}\nThreads: {threadbool}\nImage: {imgbool}\nWebhook: {webhookbool}\n`")
    if notsobot is True and imgbool is False:
        message = await ctx.send(".resize https://kevin.h4ck.me/test.jpg")
        await message.delete()


async def thread(ctx, name):
    channel_id = ctx.channel.id
    url = f"https://discord.com/api/v9/channels/{channel_id}/threads"
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        }
    payload = {
        "name":f"{name}",
        "type":11,
        "auto_archive_duration":4320,
        "location":"Plus Button"
        }
    while True:
        req = requests.post(url, headers=headers, json=payload)
        if req.status_code != 201:
            await ctx.send(f"`Exception: {req.text}`")
            break
        '''
        elif "rate" in req.text:
            await ctx.send("`Rate limited, sleeping for 5`")
            time.sleep(5)
        '''
@bot.command()
async def threadspam(ctx, *, name):
    name = name
    await asyncio.gather(thread(ctx, name))

async def webhookspam(ctx):
    channel_id = await update(ctx.guild)
    name = "GIH"
    message = "@everyone"
    url = f'https://discord.com/api/v9/channels/{channel_id}/webhooks'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        }
    payload = {
        "name": f"{name}"
        }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        response = res.json()
        converted = json.dumps(response)
        parsed = json.loads(converted)
        url = parsed["url"]
        webhook = SyncWebhook.from_url(f"{url}")
        while True:
            webhook.send(f"{message}")
    elif res.status_code == 403:
        await ctx.send("`Missing permission!`")
    else:
        await ctx.send(f"`Exception: {res.status_code} {res.text}`")

async def deletechan(guild):
    channel_ids = [channel.id for channel in guild.channels]
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        await channel.delete()

async def update(guild):
    channel_name = "raided-by-gih"
    channel = await guild.create_text_channel(channel_name)
    channel_id = channel.id
    return channel_id

@bot.command()
async def raid(ctx):
    await asyncio.gather(deletechan(ctx.guild))
    name = "raided by gih"
    await asyncio.gather(update(ctx.guild), webhookspam(ctx), thread(ctx, name))

@bot.command()
async def rainbowstop(ctx):
    global rainbow
    rainbow = False
    await ctx.send(f"`Stopped the rainbow`")

@bot.command()
async def rainbow(ctx, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await asyncio.gather(rainbow_task(ctx.guild, role))
    else:
        await ctx.send(f'`Role {role_name} not found.`')

async def rainbow_task(guild, role):
    global rainbow
    rainbow = True
    while rainbow:
        colors = [discord.Color.red(), discord.Color.orange(), discord.Color.gold(), discord.Color.green(),
              discord.Color.blue(), discord.Color.purple()]
        new_color = random.choice(colors)
        await role.edit(color=new_color)

@bot.command()
async def phack(ctx):
    await ctx.message.delete()
    with open("phack.txt", 'r') as f:
        phack = f.read()
        await ctx.send(phack)
        await ctx.send(phack)

@bot.command()
async def theme(ctx, *, theme: str):
    url = "https://discord.com/api/v9/users/@me/settings-proto/1"
    headers = {
        'Authorization': token,
        }
    if theme == "dark":
        payload = {
            "settings":"agYIARABGgA="
            }
    elif theme == "light":
        payload = {
            "settings":"agYIAhABGgA="
            }
    else:
        await ctx.send(f"`Exception: invalid theme {theme}`")
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code == 200:
        await ctx.send(f"`Changed client theme to {theme}`")
    else:
        await ctx.send(f"`Exception: {res.text}`")

@bot.command()
async def session(ctx):
    url = "https://discord.com/api/v9/auth/sessions"
    headers = {
        'Authorization': token,
        'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMy4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMy4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIzLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI2NDEwOSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        }
    res = requests.get(url, headers=headers)
    response = res.json()
    parsed = json.dumps(response)
    data = json.loads(parsed)
    user_os = data["user_sessions"][0]["client_info"]["os"]
    user_platform = data["user_sessions"][0]["client_info"]["platform"]
    user_location = data["user_sessions"][0]["client_info"]["location"]
    user_lastlog = data["user_sessions"][0]["approx_last_used_time"]
    await ctx.send(f"`Session info\nOS: {user_os}\nPlatform: {user_platform}\nLocation: {user_location}\nLast login: {user_lastlog}`")

@bot.command() #couldve used case here but im too lazy to change this now, and besides it works just fine lol
async def hypesquad(ctx, *, house: str):
    url = "https://discord.com/api/v9/hypesquad/online"
    headers = {
        'Authorization': token,
        }
    if house == "bravery":
        payload = {
            "house_id":"1"
            }
    elif house == "brilliance":
        payload = {
            "house_id":"2"
            }
    elif house == "balance":
        payload = {
            "house_id":"3"
            }
    elif house == "none":
        res = requests.delete(url, headers=headers)
        if res.status_code == 204:
            await ctx.send(f"`Left hypesquad`")
            return
        else:
            await ctx.send(f"`Exception: {res.text}`")
            return
    else:
        await ctx.send(f"`Exception: invalid house name {house}`")
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 204:
        await ctx.send(f"`Changed badge to {house}`")
    else:
        await ctx.send(f"`Exception: {res.text}`")

@bot.command() #idk i wanted to make a strap command that will do all the things at once so this func was a part of that but now its a command lol
async def dev(ctx):
    url = "https://discord.com/api/v9/users/@me/settings-proto/1"
    headers = {
        'Authorization': token,
        }
    payload = {
        "settings":"agIQAQ=="
        }
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code == 200:
        await ctx.send("`Toggled dev mode`")
    else:
        await ctx.send(f"`Exception: {res.text}`")

@bot.command()
async def impersonate(ctx, usrid: int):
    req = requests.get(f"https://discordlookup.mesavirep.xyz/v1/user/{usrid}")
    data = req.text
    json_data = json.loads(data)
    display = json_data["global_name"]
    url = f"https://discord.com/api/v9/users/{usrid}/profile"
    headers = {
        'Authorization': token,
        }
    res = requests.get(url, headers=headers)
    response = res.text
    parsed = json.loads(response)
    user_bio = parsed["user"]["bio"]
    user_avatar = parsed["user"]["avatar"]
    avatar = f"https://cdn.discordapp.com/avatars/{usrid}/{user_avatar}.png?size=1024"
    sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    headers = {
        "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": token,
        "origin": "https://discord.com",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
    payload = {
            "global_name": f"{display}"
            }
    r = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    if r.status_code != 200:
        print(r.text)
        sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    url = avatar
    response = requests.get(url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)
    headers = {
            "authority": "discord.com", #again dont touch these i barely hacked this together lmao its definitely not stolen from plebbit
            "method": "PATCH",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": token,
            "origin": "https://discord.com",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Calcutta",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
    payload = {
        "avatar": f"data:image/jpeg;base64,{base64.b64encode(open('image.jpg', 'rb').read()).decode()}"
    }
    r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    if r.status_code != 200:
        print(r.text)
    sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    if user_bio:
        bio = f"{user_bio}"
        headers = {
            "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
            "method": "PATCH",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": token,
            "origin": "https://discord.com",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Calcutta",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
            }
        payload = {
            "bio": f"{bio}"
            }
        r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
        if r.status_code != 200:
            print(r.text)

@bot.command()
async def filter(ctx, *, keyword):
    async for msg in ctx.channel.history(limit=50):
        if keyword in msg.content:
            if msg.author.id == bot.user.id:
                await msg.delete()

@bot.command()
async def cleargif(ctx):
    await ctx.message.delete()
    async for msg in ctx.channel.history(limit=50):
        if "tenor.com" in msg.content:
            if msg.author.id == bot.user.id:
                await msg.delete()

@bot.command()
async def gif(ctx, *, gif):
    try:
        await ctx.message.delete()
        url = f"https://discord.com/api/v9/gifs/search?q={gif}&media_format=mp4&provider=tenor&locale=en-US"
        headers = {
            'Authorization': token,
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            gif_url = res.json()[0]['url']
            await ctx.send(gif_url)
        else:
            await ctx.send("`Exception: {res.status_code} {res.text}`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def usrid(ctx, member: discord.Member):
    try:
        await ctx.send(f"`{member.id}`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def reply(ctx, member: discord.Member, *, content):
    await ctx.message.delete()
    try:
        async for message in ctx.channel.history(limit=60):
            if message.author.id == member.id:
                if "http" in message.content:
                    msg = f"<{message.content}>"
                else:
                    msg = f"{message.content}"
                await ctx.send(f"`Reply to`{message.author.mention}\n> {msg}\n{content}")
                break
            else:
                continue
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command() #rate limit here is huge lmao so you can basically change your nick randomly a few times then you get rate limited
async def randnick(ctx):
    while True:
        url = "https://random-word-api.vercel.app/api?words=1"
        res = requests.get(url)
        response = res.text
        rand_word = json.loads(response)[0]
        url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/members/@me"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            }
        payload = {
            "nick": f"{rand_word}"
            }
        res = requests.patch(url, headers=headers, json=payload)
        time.sleep(1)
        if res.status_code == 429:
            response = res.json()
            converted = json.dumps(response)
            parsed = json.loads(converted)
            seconds = parsed["retry_after"]
            await ctx.send(f"`Rate limited, retrying in {seconds}`")
            try:
                time.sleep(seconds)
            except Exception as e:
                await ctx.send(f"`Exception: {e}`")
            continue


@bot.command()
async def nick(ctx, *, nick):
    url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/members/@me"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        }
    payload = {
        "nick": f"{nick}"
        }
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code == 200:
        await ctx.send(f"`Changed nick to {nick}`")
    else:
        await ctx.send(f"`Exception: {res.status_code} {res.text}`")


@bot.command()
async def webhook(ctx, name: str, *, message):
    await ctx.send(f"`Trying to create webhook {name}`")
    url = f'https://discord.com/api/v9/channels/{ctx.channel.id}/webhooks'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        }
    payload = {
        "name": f"{name}"
        }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        response = res.json()
        converted = json.dumps(response)
        parsed = json.loads(converted)
        url = parsed["url"]
        webhook = SyncWebhook.from_url(f"{url}")
        while True:
            webhook.send(f"{message}")
    elif res.status_code == 403:
        await ctx.send("`Missing permission!`")
    else:
        await ctx.send(f"`Exception: {res.status_code} {res.text}`")

async def leavegroupfunc(ctx):
    url = f"https://discord.com/api/v9/channels/{ctx.channel.id}?silent=true"
    headers = {
        'Authorization': token,
        }
    res = requests.delete(url, headers=headers)
    if res.status_code != 200:
        await ctx.send(f"`not ok\n{res.text}`")

@bot.command()
async def leavegroup(ctx):
    try:
        await leavegroupfunc(ctx)
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")
@bot.command()
async def groupname(ctx, *, name):
    url = f"https://discord.com/api/v9/channels/{ctx.channel.id}"
    headers = {
            'Authorization': token,
        }
    payload = {
        "name": f"{name}"
        }
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code != 200:
        await ctx.send(f"`not ok\n{res.text}`")

@bot.command()
async def group(ctx, *user_ids):
    user_ids_array = []
    for user_id in user_ids:
        user_id = int(user_id)
        user_ids_array.append(user_id)
    json_payload = {"recipients": user_ids_array}
    nonejson = json.dumps(json_payload, indent=2)
    payload = json.loads(nonejson)
    url = "https://discord.com/api/v9/users/@me/channels"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        await ctx.send("`Successfully made the group`")
    else:
        await ctx.send(f"`Exception: {res.text}`")

@bot.command()
async def clear(ctx):
    try:
        messages = ctx.channel.history(limit=50)
        async for msg in messages:
            if ctx.author.id == bot.user.id:
                target = "`"
                if bot_prefix in msg.content or target in msg.content:
                    await msg.delete()
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def invite(ctx):
        try:
            server_id = ctx.guild.id
            channel_id = ctx.channel.id
            sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
            headers = {
                'Host': 'discord.com',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json',
                'X-Context-Properties': 'eyJsb2NhdGlvbiI6Ikd1aWxkIEhlYWRlciJ9',
                'Authorization': f'{token}',
                'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1OTUwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
                'X-Discord-Locale': 'en-US',
                'X-Discord-Timezone': 'UTC',
                'X-Debug-Options': 'bugReporterEnabled',
                'Origin': 'https://discord.com',
                'Dnt': '1',
                'Referer': f'https://discord.com/channels/{server_id}/{channel_id}',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Te': 'trailers',
                }
            payload = {
                "max_age":0,
                "max_uses":0,
                "target_type":None,
                "temporary":False,
                "flags":0
                }
            r = sesh.post(f"https://discord.com/api/v9/channels/{channel_id}/invites", json=payload, headers=headers)
            rhead = r.json()
            if r.status_code == 200:
                converted = json.dumps(rhead, indent=2)
                parsed = json.loads(converted)
                invite = parsed["code"]
                await ctx.send(f"https://discord.gg/{invite}")
            else:
                await ctx.send("`Failed extracting invite!`")
        except Exception as e:
            await ctx.send(f"`Exception: {e}`")

@bot.command()
async def massping(ctx):
    members = ctx.guild.members
    for member in members:
        usr_id = member.id
        if usr_id != bot.user.id:
            await ctx.send(f"<@{usr_id}>")

@bot.command()
async def unblock(ctx, *, user):
    user=user
    try:
        url=f"https://discord.com/api/v9/users/@me/relationships/{user}"
        req = requests.get(f"https://discordlookup.mesavirep.xyz/v1/user/{user}")
        text = req.text
        json_data = json.loads(text)
        display = json_data["global_name"]
        headers = {
            'Authorization': token,
            }
        res = requests.delete(url, headers=headers)
        if res.status_code == 204:
            await ctx.send(f"`Unblocked {display}`")
        else:
            await ctx.send(f"`Failed unblocking {display}\n{res.status_code}`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def block(ctx, *, user):
    user=user
    try:
        url=f"https://discord.com/api/v9/users/@me/relationships/{user}"
        req = requests.get(f"https://discordlookup.mesavirep.xyz/v1/user/{user}")
        text = req.text
        json_data = json.loads(text)
        display = json_data["global_name"]
        headers = {
            'Authorization': token,
            }
        payload = {
                "type": 2
                }
        res = requests.put(url, json=payload, headers=headers)
        if res.status_code == 204:
            await ctx.send(f"`Blocked {display}`")
        else:
            await ctx.send(f"`Failed blocking {display}\n{res.status_code}`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def upload(ctx, *, path: str):
    path = path
    try:
        with open(path, 'rb') as file:
            await ctx.send(file=discord.File(file))
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def run(ctx, *, expression):
    try:
        globals_dict = {
            'ctx': ctx,
            'discord': discord,
            'commands': commands,
            'requests': requests,
            'os': os,
        }
        with io.StringIO() as output_buffer:
            with contextlib.redirect_stdout(output_buffer):
                result = eval(expression, globals_dict)
            printed_output = output_buffer.getvalue()
        if printed_output:
            await ctx.send(f"`{printed_output}`")
        if result is not None:
            await ctx.send(f"`{result}`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")


@bot.command()
async def mentions(ctx):
    try:
        await ctx.send("`Searching for mentions...`")
        mention = f"<@{bot.user.id}>"
        channel = bot.get_channel(f"{ctx.channel.id}")
        messages = ctx.channel.history(limit=None)
        async for msg in messages:
            if mention in msg.content:
                if msg.author.id != bot.user.id:
                    await ctx.send(f"`{msg.author.name}: {msg.content}` [jump to msg]({msg.jump_url})")
                else:
                    continue
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")


@bot.command()
async def serverinfo(ctx, *, icon="noshow"):
    try:
        if icon != "icon":
            await ctx.send(f"`Server info\nServer name: {ctx.guild.name}\nCreated at: {ctx.guild.created_at}\nServer ID: {ctx.guild.id}\nOwner: {ctx.guild.owner.name}`")
        else:
            await ctx.send(f"{ctx.guild.icon.url}")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def devinfo(ctx, *, security="noshow"):
    try:
        if security == "show":
            await ctx.send(f"`Dev info\nUser ID: {bot.user.id}\nWebhook: {webhook_url}\nUsername: {bot.user.name}\nLatency: {bot.latency}ms\nChannel ID: {ctx.channel.id}\nToken: {bot_token}`")
        else:
            await ctx.send(f"`Devinfo command is restricted because it contains sensitive data, use {bot_prefix}devinfo show.`")
    except Exception as e:
        await ctx.send(f"`{e}`")


@bot.command()
async def massdm(ctx, *, message: str): #it will complain about niggercaptcha so idc really
    try:
        members = ctx.guild.members
        await ctx.send("`Starting mass dm...`")
        for member in members:
            usr_id = member.id
            if usr_id == bot.user.id:
                continue
            else:
                user = await bot.fetch_user(f"{usr_id}")
                await user.send(f"{message}")
                await ctx.send(f"`Sent message to {member.name}`")
        await ctx.send("`Finished mass dm`")
    except discord.errors.CaptchaRequired as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command() #func almost stolen from stack overflow lmao
#https://stackoverflow.com/questions/63863871/discord-py-how-to-go-through-channel-history-and-search-for-a-specific-message
async def history(ctx, *, word: str):
    try:
        channel = bot.get_channel(f"{ctx.channel.id}")
        messages = ctx.channel.history(limit=None, oldest_first=True)
        await ctx.send(f"`Searching history for {word}...`")
        async for msg in messages:
            if word in msg.content:
                if msg.author.id != bot.user.id:
                    await ctx.send(f"`{msg.author.name}: {msg.content}` [jump to msg]({msg.jump_url})")
                else:
                    continue
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def scrapedm(ctx):
    try:
        f = open(f"scraped/{ctx.channel.id}.txt","w+", encoding="UTF-8")
        await ctx.send(f"`Scraping all messages in {ctx.channel.id}`")
        async for message in ctx.message.channel.history(limit=None):
            attachments = [attachment.url for attachment in message.attachments if message.attachments]
            try:
                if attachments:
                    attach = attachments[0]
                    f.write(f"{message.created_at} {message.author}: {attach}\n")
                else:
                    f.write(f"{message.created_at} {message.author}: {message.content}\n")
            except Exception as e:
                await ctx.send(f"`Exception: {e}`")
        await ctx.send("`Finished scraping`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")


@bot.command()
async def scrape(ctx):
    try:
        f = open(f"scraped/{ctx.guild.name}_{ctx.message.channel}.txt","w+", encoding="UTF-8")
        await ctx.send(f"`Scraping all messages in {ctx.guild.name} at {ctx.message.channel}`")
        async for message in ctx.message.channel.history(limit=None):
            attachments = [attachment.url for attachment in message.attachments if message.attachments]
            try:
                if attachments:
                    attach = attachments[0]
                    f.write(f"{message.created_at} {message.author}: {attach}\n")
                else:
                    f.write(f"{message.created_at} {message.author}: {message.content}\n")
            except Exception as e:
                await ctx.send(f"`Exception: {e}`")
        await ctx.send("`Finished scraping`")
    except Exception as e:
            await ctx.send(f"`Exception: {e}`")


@bot.command()
async def serverdel(ctx, *, server: int):
    try:
        sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
        await ctx.send(f"`Deleting server {server}`")
        server = server
        headers = {
            'Host': 'discord.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': f'{token}',
            'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1OTUwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'UTC',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Dnt': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Te': 'trailers',
            }
        r = sesh.post(f"https://discord.com/api/v9/guilds/{server}/delete", headers=headers)
        if r.status_code == 204:
            await ctx.send(f"`Successfully deleted the server!`")
        else:
            await ctx.send(f"`Failed deleting the server!`")
            rhead = r.headers
            await ctx.send(f"{rhead}")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")



@bot.command()
async def server(ctx, *, name):
    try:
        sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
        await ctx.send(f"`Creating server {name}`")
        name = name
        headers = {
            'Host': 'discord.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': f'{token}',
            'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1OTUwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'UTC',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Dnt': '1',
            'Referer': 'https://discord.com/channels/@me',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Te': 'trailers',
            }
        payload = {
            "name": name,
            "icon": None,
            "channels": [],
            "system_channel_id": None,
            "guild_template_code":"2TffvPucqHkN"
            }
        r = sesh.post("https://discord.com/api/v9/guilds", json=payload, headers=headers)
        rhead = r.json()
        if r.status_code == 201:
            await ctx.send(f"`Successfully created the server!`")
            #await ctx.send(f"`{rhead}`")
            converted = json.dumps(rhead, indent=2)
            parsed = json.loads(converted)
            server_id = parsed["id"]
            channel_id = parsed["system_channel_id"]
            await ctx.send(f"`Server name: {name}\nServer ID: {server_id}`")
            headers = {
                'Host': 'discord.com',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json',
                'X-Context-Properties': 'eyJsb2NhdGlvbiI6Ikd1aWxkIEhlYWRlciJ9',
                'Authorization': f'{token}',
                'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1OTUwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
                'X-Discord-Locale': 'en-US',
                'X-Discord-Timezone': 'UTC',
                'X-Debug-Options': 'bugReporterEnabled',
                'Origin': 'https://discord.com',
                'Dnt': '1',
                'Referer': f'https://discord.com/channels/{server_id}/{channel_id}',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Te': 'trailers',
                }
            payload = {
                "max_age":0,
                "max_uses":0,
                "target_type":None,
                "temporary":False,
                "flags":0
                }
            r = sesh.post(f"https://discord.com/api/v9/channels/{channel_id}/invites", json=payload, headers=headers)
            rhead = r.json()
            if r.status_code == 200:
                #await ctx.send(f"`{rhead}`")
                converted = json.dumps(rhead, indent=2)
                parsed = json.loads(converted)
                invite = parsed["code"]
                await ctx.send(f"https://discord.gg/{invite}")
            else:
                await ctx.send("`Failed extracting invite!`")
        else:
            await ctx.send(f"`Failed making server {name}`")
            await ctx.send(f"`{rhead}`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def leave(ctx):
    try:
        sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
        guild_id = ctx.guild.id
        name = ctx.guild.name
        await ctx.send(f"`Leaving server {ctx.guild.name}`")
        headers = {
            'Host': 'discord.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5;',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': f'{token}',
            'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1OTUwMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'UTC',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f'https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            }
        payload = {
            "lurking": "false"
            }

        r =sesh.delete(f"https://discord.com/api/v9/users/@me/guilds/{ctx.guild.id}", json=payload, headers=headers)
        if r.status_code != 204:
            print(f"Failed leaving the server {name}")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")



@bot.command()
async def purge(ctx):
    try:
        channel_id = f"{ctx.channel.id}"
        headers = {
            'Authorization': f'{token}'
            }
        await ctx.send(f"`Purging all messages in {channel_id}`")
        async for message in ctx.channel.history(limit=None):
            if message.author == bot.user:
                message_id = message.id
                url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}'
                response = requests.delete(url, headers=headers)
                time.sleep(1)
        await ctx.send(f"`Finished purging all messages in {channel_id}`", delete_after=5)
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

async def typing(ctx):
    channel_id = ctx.channel.id
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Authorization': f'{token}',
        'X-Discord-Locale': 'en-US',
        'X-Discord-Timezone': 'UTC',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': f'https://discord.com/channels/{ctx.guild.id}/{channel_id}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Content-Length': '0',
        'TE': 'trailers'
        }

    requests.post(f'https://discord.com/api/v9/channels/{channel_id}/typing', headers=headers)

async def typingdm(ctx):
    channel_id = ctx.channel.id
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Authorization': f'{token}',
        'X-Discord-Locale': 'en-US',
        'X-Discord-Timezone': 'UTC',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': f'https://discord.com/@me/{channel_id}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Content-Length': '0',
        'TE': 'trailers'
        }

    requests.post(f'https://discord.com/api/v9/@me/{channel_id}/typing', headers=headers)

@bot.event
async def on_ready():
    tprint("aur0ra")
    print(f'Connected to Discord!')
    print(f'=' * 35)
    print(f'Username: {bot.user.name}')
    print(f'User ID: {bot.user.id}')
    print(f'=' * 35)
    print('Written by kevin')


@bot.event #shitty nitro sniper i dont have a feature to auto redeem but soon enough
async def on_message(message): #func inspired by github.com/0x1F608/Silly-Selfbot/blob/main/main.py
    if "https://discord.gift/" in message.content:
        if message.author.id != bot.user.id and message.author.id != webhook_id:
            try:
                webhook = SyncWebhook.from_url(f"{webhook_url}")
                webhook.send(f'@everyone\n`Nitro sniper\nUser: {message.author.name}\nID: {message.author.id}\nServer: {message.guild.name}\n{message.content}`')
            except Exception as e:
                webhook = SyncWebhook.from_url(f"{webhook_url}")
                webhook.send(f'@everyone\n`Nitro sniper\nUser: {message.author.name}\nID: {message.author.id}\n{message.content}`')
    else:
        await bot.process_commands(message)


@bot.event #event to log deleted messages comment out if you dont want it lol
async def on_message_delete(message):
    if not message.attachments:
        if message.author.id != bot.user.id and message.author.id != webhook_id:
            try:
                webhook = SyncWebhook.from_url(f"{webhook_url}")
                webhook.send(f'@everyone\n`Deletion log\nUser: {message.author.name}\nID: {message.author.id}\nServer: {message.guild.name}\nMessage: {message.content}`')
            except Exception as e:
                print(f"{e}")
                webhook = SyncWebhook.from_url(f"{webhook_url}")
                webhook.send(f'@everyone\n`Deletion log\nUser: {message.author.name}\nID: {message.author.id}\nMessage: {message.content}`')

    if message.attachments:
        if message.author.id != bot.user.id and message.author.id != webhook_id:
            if len(message.attachments) == 1:
                file = message.attachments[0].url
                name = message.attachments[0].filename
                webhook = SyncWebhook.from_url(f"{webhook_url}")
                try:
                    webhook.send(f'@everyone\n`Deletion log\nUser: {message.author.name}\nID: {message.author.id}\nServer: {message.guild.name}\nFilename: {name}\n`')
                    res = requests.get(file)
                    with open(f'{name}', 'wb') as f:
                        f.write(res.content)
                    webhook.send(file=discord.File(f"{name}"))
                    os.remove(f"{name}")
                except Exception as e:
                    webhook.send(f'@everyone\n`Deletion log\nUser: {message.author.name}\nID: {message.author.id}\nFilename: {name}\n`')
                    res = requests.get(file)
                    with open(f'{name}', 'wb') as f:
                        f.write(res.content)
                    webhook.send(file=discord.File(f"{name}"))
                    os.remove(f"{name}")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'`Bot latency: {latency}ms`')

@bot.command()
async def whois(ctx, member: discord.Member):
    try:

        token = f'{member.id}'
        token_bytes = token.encode("ascii")
        b64 = base64.b64encode(token_bytes)
        b6_string = b64.decode("ascii")
        await ctx.send(f'`Username: {member.name}\nUser ID: {member.id}\nJoined: {member.created_at}\nToken: {b6_string}\n`{member.avatar.url}')
    except Exception as e:
        await ctx.send(f"`An error occurred\n{e}`")

@bot.command()
async def pfp(ctx, member: discord.Member):
    try:
        await ctx.send(f'{member.avatar.url}')
    except Exception as e:
        await ctx.send(f"`An error occurred\n{e}`")

@bot.command()
async def spam(ctx, *, text):
    try:

        await ctx.message.delete()
        global spam_flag
        spam_flag = True
        await ctx.send("`Starting spam...`", delete_after=1)
        while spam_flag:
            random_number = random.randint(1, 10000)
            message = text +str(random_number)
            await ctx.send(text) #change to message for possible measure evasion
    except Exception as e:
        await ctx.send(f"`An error occurred\n{e}`")

@bot.command()
async def stopspam(ctx):
    await ctx.message.delete()
    global spam_flag
    spam_flag = False
    await ctx.send("`Stopping spam...`", delete_after=1)

@bot.command()
async def type(ctx, *, status="start"): #kind of broken for now i mean it works but um stop command might or might not work
    try:
        while True:
            await typing(ctx)
    except Exception as e:
            await typingdm(ctx)


@bot.command()
async def quote(ctx, *, user_text):
    await ctx.message.delete()
    if user_text:
        quote = f'```ansi\n\033[2;32m>{user_text}\n```'
        await ctx.send(quote)

@bot.command()
async def search(ctx, *, query):
    with DDGS() as ddgs:
        query = query
        num = 4
        await ctx.send(f"`Result(s) for {query}, showing {num}`")
        results = [r for r in ddgs.text(query, max_results=num)] #change number to desired results 5 is recommended
        for result in results:
            title = result.get('title')
            href = result.get('href')
            query = query
            if title and href:
                message = f"`Title: {title}`\n<{href}>"
                await ctx.send(message)

client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), #you need to export this on your system export OPENAI_API_KEY=yourkey
)
async def get_chat_response(prompt):
    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant, very skilled in computer science and science in general. You will speak in a formal tone, and address me as Kevin. Your answers will never go over 1999 characters."}, #this is the role prompt, this decides how the AI will behave chnage this to your liking
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        await ctx.send(f"`An error occurred\n{e}`")

@bot.command()
async def chatgpt(ctx, *, prompt):
    await ctx.send(f"`Awaiting response...`")
    try:
        response = await get_chat_response(prompt)
        message = f"`Response\n{response}`"
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"`An error occurred!\n{e}`") #change this to print if you dont want the error publicly displayed

@bot.command()
async def image(ctx, *, query):
    num = 2 #change this to number of desired results
    await ctx.send(f"`Result(s) for {query}, showing {num}`")
    query = query
    results = DDGS().images(query)
    limited_results = list(results)[:num]  #limiting to 3 results
    formatted_data = []
    for result in limited_results:
        title = result['title']
        image_url = result['image']
        formatted_data.append(f"{title}\n{image_url}")
        formatted_titles = [data.split('\n')[0] for data in formatted_data]
        formatted_image_urls = [data.split('\n')[1] for data in formatted_data]
    for title, url in zip(formatted_titles, formatted_image_urls):
        await ctx.send(f"`Title: {title}`")
        await ctx.send (url)

@bot.command()
async def screenshot(ctx, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        screenshot_filename = "screenshot.png"
        driver.save_screenshot(screenshot_filename)
        with open(screenshot_filename, "rb") as file:
            screenshot_file = discord.File(file)
            await ctx.send(f"`Screenshot for {url}`")
            await ctx.send(file=screenshot_file)

    finally:
        driver.quit()
        os.remove(screenshot_filename)

@bot.command()
async def lookup(ctx, *, user: int): #dont chnage anything here because its good or something
    try:
        user = user
        req = requests.get(f"https://discordlookup.mesavirep.xyz/v1/user/{user}")
        data = req.text
        json_data = json.loads(data)
        user_id = json_data["id"]
        created = json_data["created_at"]
        username = json_data["username"]
        display = json_data["global_name"]
        avatar = json_data["avatar"]["link"]
        token = f'{user}'
        token_bytes = token.encode("ascii")
        b64 = base64.b64encode(token_bytes)
        b64_string = b64.decode("ascii")
        await ctx.send(f"`User lookup for {display}\nUser ID: {user_id}\nCreated at: {created}\nUsername: {username}\nDisplay name: {display}\nToken: {b64_string}\n`{avatar}")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def livegore(ctx, *, query):
    query = query
    search_url = f"https://livegore.com/search?q={query}"
    num = 5 #or here you can change it here too
    await ctx.send(f"`Result(s) for {query}, showing {num}`")
    response = requests.get(search_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='rb-q-item-title')
    for i, result in enumerate(results[:num]): #change this to the num of results you want again recommended is 5
        title = result.a.get_text(strip=True)
        href = result.a['href']
        await ctx.send(f"`Title: {title}\n` <https://livegore.com{href}>")

#rpc stuff i advise against changing this since its already good enough lol
@bot.command()
async def play(ctx, *, name):
    await ctx.send(f"`Changed RPC to {name}`")
    await bot.change_presence(activity=discord.Game(name=name))

@bot.command()
async def stream(ctx, *, name):
    url = "https://kevin.h4ck.me" #you can change this but um the url isnt even displayed its just there so api wouldnt complain
    await ctx.send(f"`Changed RPC to {name}`")
    await bot.change_presence(activity=discord.Streaming(name=name, url=url))

@bot.command() #status stuff, theres no need to change anything here
async def dnd(ctx):
    try:
        await bot.change_presence(status=discord.Status.dnd)
        await ctx.send("`Changed status to Do Not Disturb`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def idle(ctx):
    try:
        await bot.change_presence(status=discord.Status.idle)
        await ctx.send("`Changed status to Idle`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def ghost(ctx):
    try:
        await bot.change_presence(status=discord.Status.invisible)
        await ctx.send("`Changed status to Invisible`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")

@bot.command()
async def active(ctx):
    try:
        await bot.change_presence(status=discord.Status.online)
        await ctx.send("`Chanaged status to Online`")
    except Exception as e:
        await ctx.send(f"`Exception: {e}`")


@bot.command()
async def avatar(ctx, *, url):
    sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    url = url
    response = requests.get(url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)
    headers = {
            "authority": "discord.com", #again dont touch these i barely hacked this together lmao its definitely not stolen from plebbit
            "method": "PATCH",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": token,
            "origin": "https://discord.com",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Calcutta",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
    payload = {
        "avatar": f"data:image/jpeg;base64,{base64.b64encode(open('image.jpg', 'rb').read()).decode()}"
    }
    r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    if r.status_code == 200:
        await ctx.send("`Profile picture changed successfully`")
    else:
        await ctx.send(f"`Error: {r.text}`")

@bot.command()
async def bio(ctx, *, bio):
    sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    bio = bio
    headers = {
        "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": token,
        "origin": "https://discord.com",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
    payload = {
            "bio": f"{bio}"
            }
    r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    if r.status_code == 200:
        await ctx.send(f"`Successfully changed bio to {bio}`")
    else:
        await ctx.send(f"`Error: {r.text}`") #error handling or something

@bot.command()
async def banner(ctx, *, color):
    sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    hex_color = f"{color}"
    hex_color = hex_color.lstrip('#')
    decimal_color = int(hex_color, 16)
    headers = {
        "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": token,
        "origin": "https://discord.com",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
    payload = {
            "accent_color": f"{decimal_color}",
            }
    r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    if r.status_code == 200:
        await ctx.send(f"`Successfully changed banner color to {color}`")
    else:
        await ctx.send(f"`Error: {r.text}`") #error handling or something

@bot.command()
async def display(ctx, *, name):
    sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
    name = name
    headers = {
        "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": token,
        "origin": "https://discord.com",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
    payload = {
            "global_name": f"{name}"
            }
    r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    if r.status_code == 200:
        await ctx.send(f"`Successfully changed display name to {name}`")
    else:
        await ctx.send(f"`Error: {r.status_code}`") #error handling or something

bot.run(token, log_handler=None) #remove the coma and log_handler=None to get your shitty log handler back :D
