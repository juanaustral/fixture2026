#!/usr/bin/env python3
"""Verify data_ko.json integrity."""
import json

with open("/root/dashboard/data_ko.json") as f:
    data = json.load(f)

ok = True
total_matches = 0
played = 0
upcoming = 0

for r in data["rounds"]:
    for m in r["matches"]:
        total_matches += 1
        if m["status"] == "played":
            played += 1
            if m["hscore"] is None or m["ascore"] is None:
                print(f"❌ [{r['name']} M{m['id']}] Played but no score: {m['home']} vs {m['away']}")
                ok = False
        elif m["status"] == "upcoming":
            upcoming += 1
            if m["hscore"] is not None or m["ascore"] is not None:
                print(f"❌ [{r['name']} M{m['id']}] Upcoming but has score: {m['home']} vs {m['away']} {m['hscore']}-{m['ascore']}")
                ok = False

print(f"Total matches: {total_matches}")
print(f"Played: {played}, Upcoming: {upcoming}")
print(f"✅ KO data consistent" if ok else "❌ Issues found")
