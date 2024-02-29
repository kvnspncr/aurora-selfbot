import requests
import time
import json
import os
import base64
from urllib.parse import quote
BASE = "https://discord.com/api/v9"

class Bot:
    def run(self, token) -> bool:
        if token is not None:
            global TOKEN 
            TOKEN = token 
            return True 
        else:
            raise Exception("Token cannot be NoneType")

    def makeserver(self, name) -> str:
        url = f"{BASE}/guilds"
        headers = {
            "Authorization": TOKEN,
            "Content-Type": "application/json",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9",
            }
        payload = {
            "name":name,
            "icon":None,
            "channels":[],
            "system_channel_id":None,
            "guild_template_code":"2TffvPucqHkN"
            }
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 201:
            rjson = res.json()
            jsonr = json.dumps(rjson)
            hello = json.loads(jsonr)
            channel_id = hello["system_channel_id"]
            url = f"{BASE}/channels/{channel_id}/invites"
            payload = {
                "max_age": 0, 
                "max_users": 0,
                "target_type":None,
                "temporary": False,
                "flags":0
                }
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                rhead = res.json()
                converted = json.dumps(rhead)
                parsed = json.loads(converted)
                inv = parsed["code"]
                invite = f"https://discord.com/invite/{inv}"
                return invite 
            else:
                print(f"Failed making server\n{res.status_code}\n{res.text}")

    def block(self, usrid) -> bool:
        url = f"{BASE}/users/@me/relationships/{usrid}"
        headers = {
            "Authorization": TOKEN,
            "Content-Type": "application/json",
            }
        payload = {
            "type": 2
            }
        res = requests.put(url, headers=headers, json=payload)
        code = res.status_code 
        match code:
            case 204:
                return True 
            case _:
                raise Exception(f"Unknown response {code}\n{res.text}")

    def convemoji(self, emoji) -> str:
        emojiencode = quote(emoji.encode('utf-8'))
        return emojiencode

    def react(self, chid:int, msgid: int, emoji: str):
        url = f"{BASE}/channels/{chid}/messages/{msgid}/reactions/{emoji}/@me?location=Message&type=0"
        headers = {
            "Authorization": TOKEN,
            "Content-Type": "application/json",
            }
        res = requests.put(url, headers=headers)
        code = res.status_code 
        match code:
            case 204:
                pass
            case 429:
                raise AttributeError("Bot is being rate limited!")

    def sendimg(self, chid: int, imgurl: str) -> bool:
        url = f"{BASE}/channels/{chid}/messages"
        if chid is not None and imgurl is not None:
            headers = {
                "Authorization": TOKEN, 
                }
            res = requests.get(imgurl)
            with open("image.jpg", "wb") as f:
                f.write(res.content)
            files = {
                "file": ("./image.jpg", open("./image.jpg", "rb")),
                }
            res = requests.post(url, headers=headers, files=files)
            code = res.status_code 
            match code:
                case 200:
                    os.remove("image.jpg")
                    return True 
                case _:
                    return False

    def makethread(self, chid: int, name: str):
        if TOKEN is not None: 
            if chid is not None: 
                url = f"{BASE}/channels/{chid}/threads"
                payload = {
                    "name":f"{name}",
                    "type":11,
                    "auto_archive_duration":4320,
                    "location":"Plus Button"
                    }
                headers = {
                    "Authorization": TOKEN, 
                    "Content-Type": "application/json",
                    }
                res = requests.post(url, headers=headers, json=payload)
                code = res.status_code 
                match code:
                    case 201:
                        print("OK")
                    case 403:
                        raise Exception("Missing permission")
                    case 429:
                        raise Exception("Bot is being rate limited")
                    case _:
                        raise Exception(f"Unknown return code {code}")

    def getuid(self):
        if TOKEN is not None:
            url = f"{BASE}/users/@me"
            headers = {
                "Authorization": TOKEN,
                "Content-Type": "application/json"
                }
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                conv = json.loads(res.text)
                user_id = conv["id"]
                return user_id 
    
    def username(self) -> str:
        if TOKEN is not None:
            url = f"{BASE}/users/@me"
            headers = {
                "Authorization": TOKEN,
                "Content-Type": "application/json",
            }
            res = requests.get(url, headers=headers)
            code = res.status_code 
            match code:
                case 200:
                    converted = json.loads(res.text)
                    username = converted["username"]
                    return username 
                case _:
                    raise Exception("Failed fetching username {code}")

    def on_ready(self) -> bool:
        if TOKEN is not None:
            url = f"{BASE}/users/@me"
            headers = {
                "Authorization": TOKEN,
                "Content-Type": "application/json",
            }
            res = requests.get(url, headers=headers)
            code = res.status_code 
            match code:
                case 200:
                    return True
                case 401:
                    raise Exception(f"Improper token has been passed")
                    return False
                case _:
                    raise Exception(f"Unknown return code {code}")
                    return False
        else:
            raise Exception("Token cannot be NoneType")

    def send_message(self, message, chid):
        if message is not None and chid is not None:
            url = f"{BASE}/channels/{chid}/messages"
            headers = {
                "Authorization": TOKEN,
                "Content-Type": "application/json",
            }
            payload = {
                "content": message,
                }
            res = requests.post(url, headers=headers, json=payload)
        
            if res.status_code != 200:
                raise Exception(f"while sending message\n{res.text}")
        else:
            raise Exception("Exception NoneType cannot be a message or channel")

    def chstatus(self, status):
        url = f"{BASE}/users/@me/settings-proto/1"
        headers = {
            "Authorization": TOKEN, 
            "Content-Type": "application/json",
            }
        if status is not None:
            match status: 
                case "online":
                    payload = {
                        "settings":"WgoKCAoGb25saW5l"
                    }
                case "dnd":
                    payload = {
                        "settings":"WgcKBQoDZG5k"
                    }
                case "idle":
                    payload = {
                        "settings":"WggKBgoEaWRsZQ=="
                    }
                case "offline":
                    payload = {
                        "settings":"Wg0KCwoJaW52aXNpYmxl"
                    }
                case _: 
                    raise Exception(f"Status cannot be {status}")
            res = requests.patch(url, headers=headers, json=payload)
            if res.status_code == 200:
                print(f"Changed status to {status}")
            else:
                raise Exception(f"Server returned code {res.status_code}")

        else:
            raise Exception("Status cannot be NoneType")

    def ping(self, start):
        end = time.time()
        finish = end - start
        return finish

    def chdisplay(self, display):
        if display is not None:
            url = f"{BASE}/users/@me"
            headers = {
                "Authorization": TOKEN,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Accept-Language": "en-US,en;q=0.5",
                "X-Super-Properties": "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMy4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMy4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIzLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5yZWRkaXQuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cucmVkZGl0LmNvbSIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNjU2MzcsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9",  
            }

            payload = {
                "global_name":f"{display}"
                }
            res = requests.patch(url, headers=headers, json=payload)
            if res.status_code == 200:
                print(f"Changed display to {display}")
            else:
                raise Exception(f"Server returned code {res.status_code}\n{res.text}")
        else:
            raise Exception("Display cannot be NoneType")


    def purge(self, chid):
        if chid is not None:
            url = f"{BASE}/channels/{chid}/messages"
            headers = {
                "Authorization": TOKEN,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Accept-Language": "en-US,en;q=0.5",
                "X-Super-Properties": "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEyMy4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMy4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIzLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5yZWRkaXQuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cucmVkZGl0LmNvbSIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNjU2MzcsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9",
                "X-Discord-Locale": "en-US",
                "X-Discord-Timezone": "UTC",
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                conv = res.json()
                for message in conv:
                    content = message.get("content")
                    msg_id = message.get("id")
                    author = message.get("author")
                    author_id = author.get("id")
                    user_id = getuid()
                    if author_id == user_id:
                        url = f"{BASE}/channels/{chid}/messages/{msg_id}"
                        res = requests.delete(url, headers=headers)
                        if res.status_code == 204:
                            pass
                        elif res.status_code == 429:
                            r = res.text 
                            j = json.loads(r)
                            s = j["retry_after"]
                            int(s)
                            time.sleep(s)
                            continue
                        else:
                            raise Exception(f"Server returned code {res.status_code}\n{res.text}")
                    else:
                        continue

    def impersonate(self, user_id):
        req = requests.get(f"https://discordlookup.mesavirep.xyz/v1/user/{user_id}")
        data = req.text
        json_data = json.loads(data)
        display = json_data["global_name"]
        url = f"{BASE}/users/{user_id}/profile"
        headers = {
            'Authorization': TOKEN, 
            }
        res = requests.get(url, headers=headers)
        response = res.text 
        parsed = json.loads(response)
        user_bio = parsed["user"]["bio"]
        user_avatar = parsed["user"]["avatar"]
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}.png?size=1024"
        headers = {
            "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
            "method": "PATCH",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": TOKEN,
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
        r = requests.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
        if r.status_code != 200:
            print(r.text)
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
                "authorization": TOKEN,
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
        r = requests.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
        if r.status_code != 200:
            print(r.text)
        if user_bio:
            bio = f"{user_bio}"
            headers = {
                "authority": "discord.com", #headers i definitely didnt steal from plebbit dont fucking touch its barely working
                "method": "PATCH",
                "scheme": "https",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "authorization": TOKEN,
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
            r = requests.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
            if r.status_code != 200:
                print(r.text)

    def session(self):
        url = f"{BASE}/auth/sessions"
        headers = {
            'Authorization': TOKEN,
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
        print("Session info")
        print(f"=" * 35)
        print(f"OS: {user_os}\nPlatform: {user_platform}\nLocation: {user_location}\nLast login: {user_lastlog}")
        print(f"=" * 35)

    def hypesquad(self, house) -> bool:
        url = f"{BASE}/hypesquad/online"
        headers = {
            'Authorization': TOKEN,
            }
        match house:
            case "bravery":
                payload = {
                    "house_id":"1"
                    }
            case "brilliance":
                payload = {
                    "house_id":"2"
                    }
            case "balance":
                payload = {
                    "house_id":"3"
                    }
            case "none":
                res = requests.delete(url, headers=headers)
                if res.status_code == 204:
                    print(f"Left hypesquad")
                    return True
                else:
                    return False
                    raise Exception(f"Server returned code {res.status_code}\n{res.text}")
                    return
            case _:
                raise Exception(f"Invalid house name {house}")
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 204:
            print(f"Changed badge to {house}")
            return True
        else:
            raise Exception(f"Server returned code {status_code}\n{res.text}")


class Check:
    def run(self, token: str) -> bool:
        if token is not None:
            global TOKEN
            TOKEN = token
            return True
        else:
            raise Exception("Token cannot be NoneType")

    def check(self) -> bool:
        if TOKEN is not None:
            url = "https://discord.com/api/v9/users/@me"
            headers = {
                "Authorization": TOKEN,
                }
            r = requests.get(url, headers=headers)
            code = r.status_code
            match code:
                case 200:
                    return True
                case 401:
                    raise Exception("Improper token has been passed")
                case _:
                    raise Exception("Unknown return code {code}")
        else:
            raise Exception("Token cannot be NoneType")


    def lookup(self, snowflake: int) -> str:
        if snowflake is not None:
            if TOKEN is not None:
                url = f"https://discord.com/api/v9/users/{snowflake}"
                headers = {
                    "Authorization": TOKEN,
                    }
                r = requests.get(url, headers=headers)
                j = json.loads(r.text)
                username = j["username"]
                userid = j["id"]
                avatar = j["avatar"]
                if avatar is None:
                    avatar = "https://cdn.discordapp.com/embed/avatars/0.png"
                else:
                    avatar = f"https://cdn.discordapp.com/avatars/{snowflake}/{avatar}.png?size=1024"
                display = j["global_name"]
                return username, userid, avatar, display
            else:
                raise Exception("Token cannot be NoneType")
        else:
            raise Exception("Snowflake cannot be NoneType")
