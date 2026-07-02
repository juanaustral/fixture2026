#!/usr/bin/env python3
"""Verify data.json matches Flashscore - direct comparison approach"""
import json, re, sys

# Flashscore data: structured DOM extraction
flashscore_raw = """27.06. 23:00 | Algeria vs Austria | 3-3
27.06. 23:00 | Jordan vs Argentina | 1-3
27.06. 20:30 | Colombia vs Portugal | 0-0
27.06. 20:30 | D.R. Congo vs Uzbekistan | 3-1
27.06. 18:00 | Croatia vs Ghana | 2-1
27.06. 18:00 | Panama vs England | 0-2
27.06. 00:00 | Egypt vs Iran | 1-1
27.06. 00:00 | New Zealand vs Belgium | 1-5
26.06. 21:00 | Cape Verde vs Saudi Arabia | 0-0
26.06. 21:00 | Uruguay vs Spain | 0-1
26.06. 16:00 | Norway vs France | 1-4
26.06. 16:00 | Senegal vs Iraq | 5-0
25.06. 23:00 | Paraguay vs Australia | 0-0
25.06. 23:00 | Turkey vs USA | 3-2
25.06. 20:00 | Japan vs Sweden | 1-1
25.06. 20:00 | Tunisia vs Netherlands | 1-3
25.06. 17:00 | Curacao vs Ivory Coast | 0-2
25.06. 17:00 | Ecuador vs Germany | 2-1
24.06. 22:00 | Czech Republic vs Mexico | 0-3
24.06. 22:00 | South Africa vs South Korea | 1-0
24.06. 19:00 | Morocco vs Haiti | 4-2
24.06. 19:00 | Scotland vs Brazil | 0-3
24.06. 16:00 | Bosnia & Herzegovina vs Qatar | 3-1
24.06. 16:00 | Switzerland vs Canada | 2-1
23.06. 23:00 | Colombia vs D.R. Congo | 1-0
23.06. 20:00 | Panama vs Croatia | 0-1
23.06. 17:00 | England vs Ghana | 0-0
23.06. 14:00 | Portugal vs Uzbekistan | 5-0
23.06. 00:00 | Jordan vs Algeria | 1-2
22.06. 21:00 | Norway vs Senegal | 3-2
22.06. 18:00 | France vs Iraq | 3-0
22.06. 14:00 | Argentina vs Austria | 2-0
21.06. 22:00 | New Zealand vs Egypt | 1-3
21.06. 19:00 | Uruguay vs Cape Verde | 2-2
21.06. 16:00 | Belgium vs Iran | 0-0
21.06. 13:00 | Spain vs Saudi Arabia | 4-0
21.06. 01:00 | Tunisia vs Japan | 0-4
20.06. 21:00 | Ecuador vs Curacao | 0-0
20.06. 17:00 | Germany vs Ivory Coast | 2-1
20.06. 14:00 | Netherlands vs Sweden | 5-1
20.06. 00:00 | Turkey vs Paraguay | 0-1
19.06. 21:30 | Brazil vs Haiti | 3-0
19.06. 19:00 | Scotland vs Morocco | 0-1
19.06. 16:00 | USA vs Australia | 2-0
18.06. 22:00 | Mexico vs South Korea | 1-0
18.06. 19:00 | Canada vs Qatar | 6-0
18.06. 16:00 | Switzerland vs Bosnia & Herzegovina | 4-1
18.06. 13:00 | Czech Republic vs South Africa | 1-1
17.06. 23:00 | Uzbekistan vs Colombia | 1-3
17.06. 20:00 | Ghana vs Panama | 1-0
17.06. 17:00 | England vs Croatia | 4-2
17.06. 14:00 | Portugal vs D.R. Congo | 1-1
17.06. 01:00 | Austria vs Jordan | 3-1
16.06. 22:00 | Argentina vs Algeria | 3-0
16.06. 19:00 | Iraq vs Norway | 1-4
16.06. 16:00 | France vs Senegal | 3-1
15.06. 22:00 | Iran vs New Zealand | 2-2
15.06. 19:00 | Saudi Arabia vs Uruguay | 1-1
15.06. 16:00 | Belgium vs Egypt | 1-1
15.06. 13:00 | Spain vs Cape Verde | 0-0
14.06. 23:00 | Sweden vs Tunisia | 5-1
14.06. 20:00 | Ivory Coast vs Ecuador | 1-0
14.06. 17:00 | Netherlands vs Japan | 2-2
14.06. 14:00 | Germany vs Curacao | 7-1
14.06. 01:00 | Australia vs Turkey | 2-0
13.06. 22:00 | Haiti vs Scotland | 0-1
13.06. 19:00 | Brazil vs Morocco | 1-1
13.06. 16:00 | Qatar vs Switzerland | 1-1
12.06. 22:00 | USA vs Paraguay | 4-1
12.06. 16:00 | Canada vs Bosnia & Herzegovina | 1-1
11.06. 23:00 | South Korea vs Czech Republic | 2-1
11.06. 16:00 | Mexico vs South Africa | 2-0"""

# Build flashscore lookup: (home_en, away_en) -> (home_score, away_score)
fs_map = {}
for line in flashscore_raw.strip().split('\n'):
    if '|' not in line:
        continue
    parts = [p.strip() for p in line.split('|')]
    home_en = parts[1].split(' vs ')[0].strip().lower()
    away_en = parts[1].split(' vs ')[1].strip().lower()
    hs, as_ = parts[2].split('-')
    fs_map[(home_en, away_en)] = (hs, as_)

# Spanish -> English name map
spanish_to_en = {
    'méxico': 'mexico',
    'sudáfrica': 'south africa',
    'corea del sur': 'south korea',
    'rep. checa': 'czech republic',
    'suiza': 'switzerland',
    'canadá': 'canada',
    'bosnia h.': 'bosnia & herzegovina',
    'qatar': 'qatar',
    'brasil': 'brazil',
    'marruecos': 'morocco',
    'escocia': 'scotland',
    'haití': 'haiti',
    'ee.uu.': 'usa',
    'australia': 'australia',
    'paraguay': 'paraguay',
    'turquía': 'turkey',
    'alemania': 'germany',
    'costa de marfil': 'ivory coast',
    'ecuador': 'ecuador',
    'curazao': 'curacao',
    'países bajos': 'netherlands',
    'japón': 'japan',
    'suecia': 'sweden',
    'túnez': 'tunisia',
    'egipto': 'egypt',
    'irán': 'iran',
    'bélgica': 'belgium',
    'n. zelanda': 'new zealand',
    'españa': 'spain',
    'uruguay': 'uruguay',
    'cabo verde': 'cape verde',
    'arabia saudita': 'saudi arabia',
    'francia': 'france',
    'noruega': 'norway',
    'senegal': 'senegal',
    'irak': 'iraq',
    'argentina': 'argentina',
    'austria': 'austria',
    'argelia': 'algeria',
    'jordania': 'jordan',
    'colombia': 'colombia',
    'portugal': 'portugal',
    'rd congo': 'd.r. congo',
    'uzbekistán': 'uzbekistan',
    'inglaterra': 'england',
    'croacia': 'croatia',
    'ghana': 'ghana',
    'panamá': 'panama',
}

def extract_team_name(opponent_field):
    """Extract just the Spanish team name from '🇿🇦 Sudáfrica' format.
    Handles multi-codepoint flags (like England/Scotland)."""
    # Remove all flag emoji characters (any character above U+1F000)
    cleaned = ''
    for c in opponent_field:
        if ord(c) < 0x1F000:
            cleaned += c
    return cleaned.strip()

# Load data.json
with open('data.json') as f:
    data = json.load(f)

errors = []
total = 0
ok = 0

for group in data['groups']:
    for team in group['teams']:
        team_es_lower = team['name'].lower().strip()
        team_en = spanish_to_en.get(team_es_lower, '???')
        
        for m in team.get('matches', []):
            total += 1
            opp_es_name = extract_team_name(m['opponent']).lower().strip()
            opp_en = spanish_to_en.get(opp_es_name, '???')
            
            score_data = m['score'].replace('–', '-')
            if '-' not in score_data:
                errors.append(f"BAD SCORE: {team['name']} vs {m['opponent']}: '{m['score']}'")
                continue
            data_ts, data_os_ = score_data.split('-')
            
            # Try to match in flashscore
            fwd_key = (team_en, opp_en)
            rev_key = (opp_en, team_en)
            
            if fwd_key in fs_map:
                fhs, fas = fs_map[fwd_key]
                if data_ts == fhs and data_os_ == fas:
                    ok += 1
                else:
                    errors.append(f"MISMATCH: {team['name']} (en:{team_en}) vs {m['opponent']} (en:{opp_en}): data={data_ts}-{data_os_}, FS={fhs}-{fas}")
            elif rev_key in fs_map:
                r_hs, r_as = fs_map[rev_key]
                if data_ts == r_as and data_os_ == r_hs:
                    ok += 1
                else:
                    errors.append(f"MISMATCH(rev): {team['name']} (en:{team_en}) vs {m['opponent']} (en:{opp_en}): data={data_ts}-{data_os_}, FS={r_as}-{r_hs}")
            else:
                errors.append(f"NOT FOUND: {team['name']} (en:{team_en}) vs {m['opponent']} (en:{opp_en})")

print(f"Total matches: {total}")
print(f"OK: {ok}")
print(f"Errors: {len(errors)}")
for e in errors:
    print(f"  ❌ {e}")

if errors:
    sys.exit(1)
else:
    print("\n✅ ALL MATCHES VERIFIED AGAINST FLASHSCORE!")
