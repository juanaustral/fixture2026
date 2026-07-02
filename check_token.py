#!/usr/bin/env python3
import json, urllib.request
token = "***"
req = urllib.request.Request(
    "https://api.github.com/user",
    headers={"Authorization": f"token {token}"}
)
resp = urllib.request.urlopen(req)
d = json.loads(resp.read())
print("Login:", d["login"])
print("ID:", d["id"])
