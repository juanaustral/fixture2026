#!/usr/bin/env python3
import json, urllib.request
import subprocess
# Get token from git remote URL
r = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, cwd="/root/dashboard")
print("Remote:", r.stdout.strip())

# Use GitHub API via SSH-authorized curl
r2 = subprocess.run([
    "curl", "-s", "-X", "POST",
    "-H", "Accept: application/vnd.github+json",
    "https://api.github.com/repos/juanaustral/fixture2026/pages",
    "-d", '{"source":{"branch":"main","path":"/"}}'
], capture_output=True, text=True)
print(r2.stdout[:500])
