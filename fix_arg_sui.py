#!/usr/bin/env python3
"""Fix Argentina vs Switzerland score: 1-0 -> 3-1 (aet). 
Fix semifinal pairings: France vs Spain, England vs Argentina."""
import json, os

with open('data_ko.json') as f:
    data = json.load(f)

# 1. Fix updated timestamp
from datetime import datetime, timezone, timedelta
t = datetime.now(timezone(timedelta(hours=-3)))
data['updated'] = t.strftime('%Y-%m-%dT%H:%M:%S-03:00')

# 2. Fix note
data['note'] = "Cuartos: Francia 2-0 Marruecos (9 jul), Noruega 1-2 Inglaterra t.e. (11 jul), Espana 2-1 Belgica (10 jul), Argentina 3-1 Suiza t.e. (11 jul, Mac Allister 10', Alvarez 112', L. Martinez 120+1'; Ndoye 67'). Semifinales: Francia vs Espana, Inglaterra vs Argentina."

# 3. Fix Cuartos match 204 (Argentina vs Suiza)
for rd in data['rounds']:
    if rd['name'] == 'Cuartos de final':
        for m in rd['matches']:
            if m['id'] == 204:
                m['hscore'] = 3
                m['ascore'] = 1
                m['status'] = 'played'
                m['extra'] = '3-1 t.e.'
                break
        break

# 4. Fix Semifinal pairings: swap them
for rd in data['rounds']:
    if rd['name'] == 'Semifinales':
        # Current: 301=Francia/Inglaterra, 302=Espana/Argentina
        # Correct: 301=Francia/Espana, 302=Inglaterra/Argentina
        rd['matches'][0]['away'] = 'España'  # France vs Spain
        rd['matches'][1]['home'] = 'Inglaterra'  # England vs Argentina
        break

# 5. Fix Argentina's ko_matches
if 'Argentina' in data.get('teams', {}):
    for km in data['teams']['Argentina'].get('ko_matches', []):
        if km.get('r') == 'Cuartos de final':
            km['s'] = '3-1'
            break

# 6. Fix Suiza's ko_matches
if 'Suiza' in data.get('teams', {}):
    for km in data['teams']['Suiza'].get('ko_matches', []):
        if km.get('r') == 'Cuartos de final':
            km['s'] = '1-3'
            break

with open('data_ko.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("data_ko.json updated successfully")
print(f"Updated: {data['updated']}")
print(f"Note: {data['note']}")
