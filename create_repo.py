import json, urllib.request, os
token = "***"
url = "https://api.github.com/user/repos"
data = json.dumps({"name":"mundial2026","description":"Panel interactivo del Mundial 2026","private":False,"auto_init":False}).encode()
req = urllib.request.Request(url, data=data, headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json"})
resp = urllib.request.urlopen(req)
d = json.loads(resp.read())
print(d.get("html_url","OK"))
