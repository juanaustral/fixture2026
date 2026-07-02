#!/usr/bin/env python3
"""Verify data.json matches Flashscore - precise match-by-match"""
import json, re

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

# English-to-Spanish name map
name_to_spanish = {
    'mexico': 'México',
    'south africa': 'Sudáfrica',
    'south korea': 'Corea del Sur',
    'czech republic': 'Rep. Checa',
    'switzerland': 'Suiza',
    'canada': 'Canadá',
    'bosnia & herzegovina': 'Bosnia H.',
    'qatar': 'Qatar',
    'brazil': 'Brasil',
    'morocco': 'Marruecos',
    'scotland': 'Escocia',
    'haiti': 'Haití',
    'usa': 'EE.UU.',
    'australia': 'Australia',
    'paraguay': 'Paraguay',
    'turkey': 'Turquía',
    'germany': 'Alemania',
    'ivory coast': 'Costa de Marfil',
    'ecuador': 'Ecuador',
    'curacao': 'Curazao',
    'netherlands': 'Países Bajos',
    'japan': 'Japón',
    'sweden': 'Suecia',
    'tunisia': 'Túnez',
    'egypt': 'Egipto',
    'iran': 'Irán',
    'belgium': 'Bélgica',
    'new zealand': 'N. Zelanda',
    'spain': 'España',
    'uruguay': 'Uruguay',
    'cape verde': 'Cabo Verde',
    'saudi arabia': 'Arabia Saudita',
    'france': 'Francia',
    'norway': 'Noruega',
    'senegal': 'Senegal',
    'iraq': 'Irak',
    'argentina': 'Argentina',
    'austria': 'Austria',
    'algeria': 'Argelia',
    'jordan': 'Jordania',
    'colombia': 'Colombia',
    'portugal': 'Portugal',
    'd.r. congo': 'RD Congo',
    'uzbekistan': 'Uzbekistán',
    'england': 'Inglaterra',
    'croatia': 'Croacia',
    'ghana': 'Ghana',
    'panama': 'Panamá',
}

# Map from spanish name back to english
spanish_to_english = {v.lower(): k for k, v in name_to_spanish.items()}
spanish_to_english.update({
    'rep. checa': 'czech republic',
    'bosnia h.': 'bosnia & herzegovina',
    'ee.uu.': 'usa',
    'países bajos': 'netherlands',
    'n. zelanda': 'new zealand',
    'costa de marfil': 'ivory coast',
    'rd congo': 'd.r. congo',
    'uzbekistán': 'uzbekistan',
    'cabo verde': 'cape verde',
    'arabia saudita': 'saudi arabia',
})

def extract_name(opponent_field):
    """Extract just the Spanish team name from '🇿🇦 Sudáfrica' format"""
    parts = opponent_field.split()
    name_parts = [p for p in parts if all(ord(c) < 0x1F000 for c in p)]
    return ' '.join(name_parts)

# Parse flashscore into a normalized lookup
# Key: tuple of (lowercase english name, lowercase english name) for home/away
fs_match_set = {}
for line in flashscore_raw.strip().split('\n'):
    if '|' not in line:
        continue
    parts = [p.strip() for p in line.split('|')]
    home_en = parts[1].split(' vs ')[0].strip().lower()
    away_en = parts[1].split(' vs ')[1].strip().lower() if ' vs ' in parts[1] else ''
    score = parts[2]
    hs, as_ = score.split('-')
    fs_match_set[(home_en, away_en)] = (hs, as_)

# Load data.json
with open('data.json') as f:
    data = json.load(f)

# Now verify each match in data.json
errors = []
matches_checked = 0
matches_ok = 0

for group in data['groups']:
    for team in group['teams']:
        team_es = team['name'].lower().strip()
        team_en = spanish_to_english.get(team_es, team_es)
        
        for m in team.get('matches', []):
            matches_checked += 1
            opp_es = extract_name(m['opponent']).lower().strip()
            opp_en = spanish_to_english.get(opp_es, opp_es)
            
            score = m['score'].replace('–', '-')
            if '-' not in score:
                errors.append(f"BAD SCORE: {team['name']} vs {m['opponent']}: '{m['score']}'")
                continue
            ts, os_ = score.split('-')
            ts, os_ = ts.strip(), os_.strip()
            
            # Look up in flashscore
            fwd_key = (team_en, opp_en)
            rev_key = (opp_en, team_en)
            
            if fwd_key in fs_match_set:
                fhs, fas = fs_match_set[fwd_key]
                if ts == fhs and os_ == fas:
                    matches_ok += 1
                else:
                    errors.append(f"MISMATCH: {team['name']} vs {m['opponent']}: data={ts}-{os_}, FS={fhs}-{fas}")
            elif rev_key in fs_match_set:
                fhs, fas = fs_match_set[rev_key]
                if ts == fas and os_ == fhs:
                    matches_ok += 1
                else:
                    errors.append(f"MISMATCH(rev): {team['name']} vs {m['opponent']}: data={ts}-{os_}, FS={fas}-{fhs}")
            else:
                # Try fuzzy matching
                found = False
                for (h, a), (hs, as_) in fs_match_set.items():
                    if (team_en in h and opp_en in a):
                        if ts == hs and os_ == as_:
                            matches_ok += 1
                        else:
                            errors.append(f"MISMATCH(fwd): {team['name']} vs {m['opponent']}: data={ts}-{os_}, FS={hs}-{as_} (matched as {h} vs {a})")
                        found = True
                        break
                    elif (team_en in a and opp_en in h):
                        if ts == as_ and os_ == hs:
                            matches_ok += 1
                        else:
                            errors.append(f"MISMATCH(rev): {team['name']} vs {m['opponent']}: data={ts}-{os_}, FS={as_}-{hs} (matched as {a} vs {h})")
                        found = True
                        break
                if not found:
                    errors.append(f"NOT FOUND: {team['name']} vs {m['opponent']} (en: {team_en} vs {opp_en})")

print(f"Matches checked: {matches_checked}")
print(f"OK: {matches_ok}")
print(f"Errors: {len(errors)}")
for e in errors:
    print(f"  ❌ {e}")

# Now verify each match directly by building the full match list per group
print("\n\n=== MANUAL VERIFICATION BY GROUP ===")
# Let me map each group's matches manually
group_matches = {
    'Grupo A': {
        ('México', 'Sudáfrica'): '2-0',
        ('México', 'Corea del Sur'): '1-0',
        ('México', 'Rep. Checa'): '3-0',
        ('Sudáfrica', 'Rep. Checa'): '1-1',
        ('Sudáfrica', 'Corea del Sur'): '1-0',
        ('Corea del Sur', 'Rep. Checa'): '2-1',
    },
    'Grupo B': {
        ('Suiza', 'Canadá'): '2-1',
        ('Suiza', 'Bosnia H.'): '4-1',
        ('Suiza', 'Qatar'): '1-1',
        ('Canadá', 'Bosnia H.'): '1-1',
        ('Canadá', 'Qatar'): '6-0',
        ('Bosnia H.', 'Qatar'): '3-1',
    },
    'Grupo C': {
        ('Brasil', 'Marruecos'): '1-1',
        ('Brasil', 'Haití'): '3-0',
        ('Brasil', 'Escocia'): '3-0',
        ('Marruecos', 'Haití'): '4-2',
        ('Marruecos', 'Escocia'): '1-0',
        ('Escocia', 'Haití'): '1-0',
    },
    'Grupo D': {
        ('EE.UU.', 'Paraguay'): '4-1',
        ('EE.UU.', 'Australia'): '2-0',
        ('EE.UU.', 'Turquía'): '2-3',
        ('Australia', 'Turquía'): '2-0',
        ('Australia', 'Paraguay'): '0-0',
        ('Paraguay', 'Turquía'): '1-0',
    },
    'Grupo E': {
        ('Alemania', 'Curazao'): '7-1',
        ('Alemania', 'Costa de Marfil'): '2-1',
        ('Alemania', 'Ecuador'): '1-2',
        ('Costa de Marfil', 'Ecuador'): '1-0',
        ('Costa de Marfil', 'Curazao'): '2-0',
        ('Ecuador', 'Curazao'): '0-0',
    },
    'Grupo F': {
        ('Países Bajos', 'Japón'): '2-2',
        ('Países Bajos', 'Suecia'): '5-1',
        ('Países Bajos', 'Túnez'): '3-1',
        ('Japón', 'Suecia'): '1-1',
        ('Japón', 'Túnez'): '4-0',
        ('Suecia', 'Túnez'): '5-1',
    },
    'Grupo G': {
        ('Egipto', 'Irán'): '1-1',
        ('Egipto', 'N. Zelanda'): '3-1',
        ('Egipto', 'Bélgica'): '1-1',
        ('Irán', 'N. Zelanda'): '2-2',
        ('Irán', 'Bélgica'): '0-0',
        ('Bélgica', 'N. Zelanda'): '5-1',
    },
    'Grupo H': {
        ('España', 'Uruguay'): '1-0',
        ('España', 'Cabo Verde'): '0-0',
        ('España', 'Arabia Saudita'): '4-0',
        ('Uruguay', 'Cabo Verde'): '2-2',
        ('Uruguay', 'Arabia Saudita'): '1-1',
        ('Cabo Verde', 'Arabia Saudita'): '0-0',
    },
    'Grupo I': {
        ('Francia', 'Noruega'): '4-1',
        ('Francia', 'Senegal'): '3-1',
        ('Francia', 'Irak'): '3-0',
        ('Noruega', 'Senegal'): '3-2',
        ('Noruega', 'Irak'): '4-1',
        ('Senegal', 'Irak'): '5-0',
    },
    'Grupo J': {
        ('Argentina', 'Austria'): '2-0',
        ('Argentina', 'Argelia'): '3-0',
        ('Argentina', 'Jordania'): '3-1',
        ('Austria', 'Argelia'): '3-3',
        ('Austria', 'Jordania'): '3-1',
        ('Argelia', 'Jordania'): '2-1',
    },
    'Grupo K': {
        ('Colombia', 'Portugal'): '0-0',
        ('Colombia', 'RD Congo'): '1-0',
        ('Colombia', 'Uzbekistán'): '3-1',
        ('Portugal', 'RD Congo'): '1-1',
        ('Portugal', 'Uzbekistán'): '5-0',
        ('RD Congo', 'Uzbekistán'): '3-1',
    },
    'Grupo L': {
        ('Inglaterra', 'Croacia'): '4-2',
        ('Inglaterra', 'Ghana'): '0-0',
        ('Inglaterra', 'Panamá'): '2-0',
        ('Croacia', 'Ghana'): '2-1',
        ('Croacia', 'Panamá'): '1-0',
        ('Ghana', 'Panamá'): '1-0',
    },
}

# Flashscore scores in the same format (home_es vs away_es)
fs_by_group = {
    'Grupo A': {
        ('México', 'Sudáfrica'): None,  # 11.06: Mexico vs South Africa | 2-0
        ('México', 'Corea del Sur'): None,  # 18.06: Mexico vs South Korea | 1-0
        ('México', 'Rep. Checa'): None,  # 24.06: Czech Republic vs Mexico | 0-3
        ('Sudáfrica', 'Rep. Checa'): None,  # 18.06: Czech Republic vs South Africa | 1-1
        ('Sudáfrica', 'Corea del Sur'): None,  # 24.06: South Africa vs South Korea | 1-0
        ('Corea del Sur', 'Rep. Checa'): None,  # 11.06: South Korea vs Czech Republic | 2-1
    },
}

# Flashscore match mapping: en_home + en_away -> score
fs_by_en = {
    ('mexico', 'south africa'): '2-0',
    ('mexico', 'south korea'): '1-0',
    ('czech republic', 'mexico'): '0-3',
    ('czech republic', 'south africa'): '1-1',
    ('south africa', 'south korea'): '1-0',
    ('south korea', 'czech republic'): '2-1',
    ('switzerland', 'canada'): '2-1',
    ('switzerland', 'bosnia & herzegovina'): '4-1',
    ('qatar', 'switzerland'): '1-1',
    ('canada', 'bosnia & herzegovina'): '1-1',
    ('canada', 'qatar'): '6-0',
    ('bosnia & herzegovina', 'qatar'): '3-1',
    ('brazil', 'morocco'): '1-1',
    ('brazil', 'haiti'): '3-0',
    ('scotland', 'brazil'): '0-3',
    ('morocco', 'haiti'): '4-2',
    ('morocco', 'scotland'): '1-0',
    ('haiti', 'scotland'): '0-1',
    ('usa', 'paraguay'): '4-1',
    ('usa', 'australia'): '2-0',
    ('turkey', 'usa'): '3-2',
    ('australia', 'turkey'): '2-0',
    ('australia', 'paraguay'): '0-0',
    ('turkey', 'paraguay'): '0-1',
    ('germany', 'curacao'): '7-1',
    ('germany', 'ivory coast'): '2-1',
    ('ecuador', 'germany'): '2-1',
    ('ivory coast', 'ecuador'): '1-0',
    ('curacao', 'ivory coast'): '0-2',
    ('ecuador', 'curacao'): '0-0',
    ('netherlands', 'japan'): '2-2',
    ('netherlands', 'sweden'): '5-1',
    ('tunisia', 'netherlands'): '1-3',
    ('japan', 'sweden'): '1-1',
    ('japan', 'tunisia'): '4-0',
    ('sweden', 'tunisia'): '5-1',
    ('egypt', 'iran'): '1-1',
    ('new zealand', 'egypt'): '1-3',
    ('belgium', 'egypt'): '1-1',
    ('iran', 'new zealand'): '2-2',
    ('belgium', 'iran'): '0-0',
    ('belgium', 'new zealand'): '5-1',
    ('spain', 'uruguay'): '1-0',
    ('spain', 'cape verde'): '0-0',
    ('spain', 'saudi arabia'): '4-0',
    ('uruguay', 'cape verde'): '2-2',
    ('saudi arabia', 'uruguay'): '1-1',
    ('cape verde', 'saudi arabia'): '0-0',
    ('france', 'norway'): '4-1',
    ('france', 'senegal'): '3-1',
    ('france', 'iraq'): '3-0',
    ('norway', 'senegal'): '3-2',
    ('iraq', 'norway'): '1-4',
    ('senegal', 'iraq'): '5-0',
    ('argentina', 'austria'): '2-0',
    ('argentina', 'algeria'): '3-0',
    ('jordan', 'argentina'): '1-3',
    ('austria', 'algeria'): '3-3',
    ('austria', 'jordan'): '3-1',
    ('jordan', 'algeria'): '1-2',
    ('colombia', 'portugal'): '0-0',
    ('colombia', 'd.r. congo'): '1-0',
    ('uzbekistan', 'colombia'): '1-3',
    ('portugal', 'd.r. congo'): '1-1',
    ('portugal', 'uzbekistan'): '5-0',
    ('d.r. congo', 'uzbekistan'): '3-1',
    ('england', 'croatia'): '4-2',
    ('england', 'ghana'): '0-0',
    ('panama', 'england'): '0-2',
    ('croatia', 'ghana'): '2-1',
    ('croatia', 'panama'): '1-0',
    ('ghana', 'panama'): '1-0',
}

# Now let me verify: take each team pair, check data.json score vs flashscore
errors2 = []
for group in data['groups']:
    for team in group['teams']:
        team_es_lower = team['name'].lower().strip()
        team_en = spanish_to_english.get(team_es_lower, team_es_lower)
        
        for m in team.get('matches', []):
            opp_es = extract_name(m['opponent']).lower().strip()
            opp_en = spanish_to_english.get(opp_es, opp_es)
            
            score_data = m['score'].replace('–', '-')
            
            # Check both directions
            fwd = (team_en, opp_en)
            rev = (opp_en, team_en)
            
            if fwd in fs_by_en:
                fs_score = fs_by_en[fwd]
                if score_data != fs_score:
                    errors2.append(f"{group['name']}: {team['name']} vs {m['opponent']}: data={score_data}, FS={fs_score}")
            elif rev in fs_by_en:
                fs_score = fs_by_en[rev]
                # Reverse the score for comparison
                if '-' in fs_score:
                    parts = fs_score.split('-')
                    rev_score = f"{parts[1]}-{parts[0]}"
                    if score_data != rev_score:
                        errors2.append(f"{group['name']} (rev): {team['name']} vs {m['opponent']}: data={score_data}, FS={fs_score}")
            else:
                errors2.append(f"{group['name']}: NOT FOUND: {team['name']} vs {m['opponent']} (en: {team_en} vs {opp_en})")

print(f"\n=== VERIFICATION RESULTS ===")
print(f"Total errors: {len(errors2)}")
for e in errors2:
    print(f"  ❌ {e}")

if not errors2:
    print("✅ ALL MATCHES VERIFIED!")
