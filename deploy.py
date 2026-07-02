#!/usr/bin/env python3
import json, urllib.request, subprocess, os, urllib.parse

TOKEN = "***"
REPO = "mundial2026"

# Test token first
try:
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={"Authorization": f"token {TOKEN}"}
    )
    resp = urllib.request.urlopen(req)
    user = json.loads(resp.read())
    print(f"Autenticado como: {user['login']}")
except Exception as e:
    print(f"Token invalido: {e}")
    exit(1)

# 1. Crear repo
url = "https://api.github.com/user/repos"
data = json.dumps({"name": REPO, "private": False, "auto_init": False}).encode()
req = urllib.request.Request(url, data=data, headers={
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
})
try:
    resp = urllib.request.urlopen(req)
    d = json.loads(resp.read())
    print(f"Repo creado: {d.get('html_url', 'OK')}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if "already exists" in body:
        print("Repo ya existe")
    else:
        print(f"Error creando repo: {e.code}")
        exit(1)

# 2. Push con git usando token incrustado
token_encoded = urllib.parse.quote(TOKEN, safe='')
os.chdir("/root/dashboard")
remote = f"https://{user['login']}:{token_encoded}@github.com/{user['login']}/{REPO}.git"
subprocess.run(["git", "remote", "set-url", "origin", remote], capture_output=True)
r = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
print(r.stdout[-500:] if r.stdout else "")
print(r.stderr[-500:] if r.stderr else "")
if r.returncode == 0:
    print(f"\n✅ SUBIDO: https://github.com/{user['login']}/{REPO}")
    print(f"   Pages: https://{user['login']}.github.io/{REPO}/")
