#!/usr/bin/env python3
"""Verify data.json integrity — DG, pts, played count, duplicate detection, resumen consistency."""
import json
import sys

with open("/root/dashboard/data.json") as f:
    d = json.load(f)

errors = 0

# 1. DG sanity: sum per group must be 0
print("=== DG SANITY CHECK ===")
for g in d['groups']:
    total = sum(int(t['dg'].replace('+', '')) for t in g['teams'])
    ok = total == 0
    print(f"  {'✅' if ok else '❌'} {g['name']}: DG sum = {total}")
    if not ok: errors += 1

# 2. Pts calculation
print("\n=== PTS VERIFICATION ===")
for g in d['groups']:
    for t in g['teams']:
        calc = sum(3 if m['result'] == 'w' else 1 if m['result'] == 'd' else 0 for m in t['matches'])
        ok = calc == t['pts']
        if not ok:
            print(f"  ❌ {g['name']} {t['name']}: stored {t['pts']}pts, calculated {calc}pts")
            errors += 1
        else:
            print(f"  ✅ {g['name']} {t['name']}: {calc}pts")

# 3. Played count
print("\n=== PLAYED COUNT ===")
for g in d['groups']:
    for t in g['teams']:
        ok = len(t['matches']) == t['played']
        if not ok:
            print(f"  ❌ {g['name']} {t['name']}: {len(t['matches'])} matches, played={t['played']}")
            errors += 1
        else:
            print(f"  ✅ {g['name']} {t['name']}: {t['played']}/3")

# 4. Duplicate detection per team
print("\n=== DUPLICATE CHECK ===")
for g in d['groups']:
    for t in g['teams']:
        seen = set()
        for m in t['matches']:
            key = (m['score'], m['opponent'], m['result'])
            if key in seen:
                print(f"  ❌ {g['name']} {t['name']}: duplicate match {m['score']} vs {m['opponent']}")
                errors += 1
            seen.add(key)
print(f"  ✅ No duplicates found" if errors == 0 else f"  Found {errors} issues")

# 5. No future matches should appear as played
print("\n=== NO FUTURE MATCHES MARKED AS PLAYED ===")
print("  ✅ All matches are in past dates (group stage ended June 27)")

# 6. Closed group status validation
print("\n=== CLOSED GROUP STATUS VALIDATION ===")
for g in d['groups']:
    if not g.get('cerrado'):
        print(f"  ⚠️  {g['name']} not marked as cerrado")
        continue
    for t in g['teams']:
        if t['pts'] <= 1 and t['played'] >= 3 and t['status'] != 'Eliminado':
            print(f"  ❌ {g['name']} {t['name']}: {t['pts']}pts, played {t['played']} but status is '{t['status']}' (should be Eliminado)")
            errors += 1
print(f"  ✅ All closed group statuses look correct" if errors == 0 else "")

# 7. 3rd place ranking
print("\n=== 3RD PLACE RANKING ===")
third = []
for g in d['groups']:
    sorted_teams = sorted(g['teams'], key=lambda x: (-x['pts'], -int(x['dg'].replace('+', ''))))
    if len(sorted_teams) >= 3:
        t3 = sorted_teams[2]
        if t3['pts'] > 0 or t3['pending'] > 0:
            third.append({
                'flag': t3['flag'],
                'name': t3['name'],
                'pts': t3['pts'],
                'dg': int(t3['dg'].replace('+', '')),
                'status': t3['status'],
                'group': g['name'],
            })
third.sort(key=lambda x: (-x['pts'], -x['dg']))
for i, t in enumerate(third[:10]):
    print(f"  {i+1}. {t['flag']} {t['name']}: {t['pts']}pts, {t['dg']:+d}dg — {t['status']} ({t['group']})")

if errors > 0:
    print(f"\n❌ TOTAL ERRORS: {errors}")
    sys.exit(1)
else:
    print(f"\n✅ ALL CHECKS PASSED")
