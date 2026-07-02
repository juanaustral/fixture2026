#!/usr/bin/env python3
import json, urllib.request, subprocess, os, sys

token = sys.stdin.readline().strip()
repo = "mundial2026"

# Crear repo
url = "https://api.github.com/user/repos"
data = json.dumps({"name": repo, "private": False, "auto_init": False})
req = urllib.request.Request(
    url, data=data.encode(),
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }
)
try:
    resp = urllib.request.urlopen(req)
    d = json.loads(resp.read())
    print(f"Repo OK: {d['html_url']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if "already exists" in body:
        print("Repo ya existe")
    else:
        print(f"Error: {body}")
        sys.exit(1)

# Push
os.chdir("/root/dashboard")
subprocess.run(["git", "remote", "set-url", "origin",
    f"https://juanaustral:{token}@github.com/juanaustral/{repo}.git"],
    capture_output=True)
r = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
print(r.stdout[-400:] or "")
print(r.stderr[-400:] or "")
if r.returncode == 0:
    print(f"\n✅ https://github.com/juanaustral/{repo}")
else:
    print("❌ Push falló")
