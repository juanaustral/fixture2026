#!/usr/bin/env python3
"""
Verify data.json integrity: DG sanity, points calculation, match counts,
closed group status coherence, duplicate detection, 3rd place ranking check.
Returns non-zero on errors.
"""

import json
import sys

DATA_FILE = "/root/dashboard/data.json"

def main():
    with open(DATA_FILE) as f:
        d = json.load(f)

    errors = []
    warnings = []

    for g in d['groups']:
        gname = g['name']
        teams = g['teams']

        # 1. DG sanity: sum must = 0
        dg_sum = 0
        for t in teams:
            dg = int(t['dg'].replace('+', ''))
            dg_sum += dg
        if dg_sum != 0:
            errors.append(f"{gname}: DG sum = {dg_sum} (must be 0)")

        # 2. Points calculation
        for t in teams:
            expected_pts = 0
            for m in t['matches']:
                if m['result'] == 'w':
                    expected_pts += 3
                elif m['result'] == 'd':
                    expected_pts += 1
            if t['pts'] != expected_pts:
                errors.append(f"{gname}/{t['name']}: pts={t['pts']} but expected {expected_pts} from {len(t['matches'])} matches")

        # 3. Played = match count
        for t in teams:
            if t['played'] != len(t['matches']):
                errors.append(f"{gname}/{t['name']}: played={t['played']} but has {len(t['matches'])} matches")

        # 4. Duplicate detection
        for t in teams:
            seen = set()
            for m in t['matches']:
                key = (m['score'], m['opponent'], m['result'])
                if key in seen:
                    errors.append(f"{gname}/{t['name']}: duplicate match {key}")
                seen.add(key)

        # 5. Closed group coherence
        if g.get('cerrado', False):
            # Every team should have 3 matches
            for t in teams:
                if len(t['matches']) != 3:
                    warnings.append(f"{gname}/{t['name']}: closed group but only {len(t['matches'])} matches")

            # Teams with 0-1 pts in 3 matches must be Eliminado
            for t in teams:
                if t['pts'] <= 1 and t['played'] >= 3 and t['status'] != 'Eliminado':
                    errors.append(f"{gname}/{t['name']}: {t['pts']}pts/{t['played']}m but status={t['status']} (should be Eliminado)")

            # Teams with 6+ pts should be Clasificado
            for t in teams:
                if t['pts'] >= 6 and t['status'] not in ('Clasificado',):
                    errors.append(f"{gname}/{t['name']}: {t['pts']}pts but status={t['status']} (should be Clasificado)")

        # 6. NO future matches
        for t in teams:
            for m in t['matches']:
                if m['result'] not in ('w', 'd', 'l'):
                    warnings.append(f"{gname}/{t['name']}: match '{m['score']} vs {m['opponent']}' has no result")

    # 7. 3rd place ranking
    third_places = []
    for g in d['groups']:
        sorted_teams = sorted(g['teams'], key=lambda t: (t['pts'], int(t['dg'].replace('+', ''))), reverse=True)
        if len(sorted_teams) >= 3 and sorted_teams[2]['pts'] > 0:
            t3 = sorted_teams[2]
            third_places.append((t3['pts'], int(t3['dg'].replace('+', '')), t3['name'], g['name'], t3['status']))

    third_places.sort(key=lambda x: (x[0], x[1]), reverse=True)

    # Status check for top 8
    for i, (pts, dg, name, group, status) in enumerate(third_places):
        if i < 8:
            # Top 8 should not be Eliminado
            if status == 'Eliminado':
                warnings.append(f"3rd place ranking: {name} ({group}) is #{i+1} with {pts}pts but status=Eliminado")
        else:
            # Outside top 8 should not be Clasificado
            if status == 'Clasificado':
                warnings.append(f"3rd place ranking: {name} ({group}) is #{i+1} (outside top 8) but status=Clasificado")

    # 8. Resumen consistency check
    for g in d['groups']:
        gname = g['name']
        resumen = g.get('resumen', [])
        for t in g['teams']:
            team_status_found = False
            for r in resumen:
                if t['name'] in r:
                    team_status_found = True
                    # Check if resumen text matches the team's status
                    if t['status'] == 'Eliminado' and 'eliminado' not in r.lower():
                        warnings.append(f"{gname}/{t['name']}: status=Eliminado but resumen '{r}' doesn't mention it")
                    if t['status'] == 'Clasificado' and ('✅' not in r and 'Clasificado' not in r):
                        warnings.append(f"{gname}/{t['name']}: status=Clasificado but resumen '{r}' doesn't show it")
            if not team_status_found:
                warnings.append(f"{gname}/{t['name']}: not found in resumen")

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ❌ {e}")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠️  {w}")

    if errors:
        print(f"\n❌ FAILED: {len(errors)} errors, {len(warnings)} warnings")
        sys.exit(1)
    elif warnings:
        print(f"\n⚠️  PASSED with {len(warnings)} warnings")
        sys.exit(0)
    else:
        print("\n✅ ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
