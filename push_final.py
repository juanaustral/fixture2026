#!/usr/bin/env python3
import subprocess, sys, os
token = sys.argv[1]
repo = "fixture2026"
os.chdir("/root/dashboard")
subprocess.run(["git", "remote", "set-url", "origin",
    f"https://juanaustral:{token}@github.com/juanaustral/{repo}.git"],
    capture_output=True)
r = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
print(r.stdout[-500:] or "")
print(r.stderr[-500:] or "")
print("Exit:", r.returncode)
