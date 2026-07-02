"""Verify data.json scores against Flashscore data."""
import json

# Flashscore data: (team1, team2, hscore, ascore)
flashscore = [
    ("South Africa", "Canada", 0, 1),
    ("Algeria", "Austria", 3, 3),
    ("Jordan", "Argentina", 1, 3),
    ("Colombia", "Portugal", 0, 0),
    ("D.R. Congo", "Uzbekistan", 3, 1),
    ("Croatia", "Ghana", 2, 1),
    ("Panama", "England", 0, 2),
    ("Egypt", "Iran", 1, 1),
    ("New Zealand", "Belgium", 1, 5),
    ("Cape Verde", "Saudi Arabia", 0, 0),
    ("Uruguay", "Spain", 0, 1),
    ("Norway", "France", 1, 4),
    ("Senegal", "Iraq", 5, 0),
    ("Paraguay", "Australia", 0, 0),
    ("Turkey", "USA", 3, 2),
    ("Japan", "Sweden", 1, 1),
    ("Tunisia", "Netherlands", 1, 3),
    ("Curacao", "Ivory Coast", 0, 2),
    ("Ecuador", "Germany", 2, 1),
    ("Czech Republic", "Mexico", 0, 3),
    ("South Africa", "South Korea", 1, 0),
    ("Morocco", "Haiti", 4, 2),
    ("Scotland", "Brazil", 0, 3),
    ("Bosnia & Herzegovina", "Qatar", 3, 1),
    ("Switzerland", "Canada", 2, 1),
    ("Colombia", "D.R. Congo", 1, 0),
    ("Panama", "Croatia", 0, 1),
    ("England", "Ghana", 0, 0),
    ("Portugal", "Uzbekistan", 5, 0),
    ("Jordan", "Algeria", 1, 2),
    ("Norway", "Senegal", 3, 2),
    ("France", "Iraq", 3, 0),
    ("Argentina", "Austria", 2, 0),
    ("New Zealand", "Egypt", 1, 3),
    ("Uruguay", "Cape Verde", 2, 2),
    ("Belgium", "Iran", 0, 0),
    ("Spain", "Saudi Arabia", 4, 0),
    ("Tunisia", "Japan", 0, 4),
    ("Ecuador", "Curacao", 0, 0),
    ("Germany", "Ivory Coast", 2, 1),
    ("Netherlands", "Sweden", 5, 1),
    ("Turkey", "Paraguay", 0, 1),
    ("Brazil", "Haiti", 3, 0),
    ("Scotland", "Morocco", 0, 1),
    ("USA", "Australia", 2, 0),
    ("Mexico", "South Korea", 1, 0),
    ("Canada", "Qatar", 6, 0),
    ("Switzerland", "Bosnia & Herzegovina", 4, 1),
    ("Czech Republic", "South Africa", 1, 1),
    ("Uzbekistan", "Colombia", 1, 3),
    ("Ghana", "Panama", 1, 0),
    ("England", "Croatia", 4, 2),
    ("Portugal", "D.R. Congo", 1, 1),
    ("Austria", "Jordan", 3, 1),
    ("Argentina", "Algeria", 3, 0),
    ("Iraq", "Norway", 1, 4),
    ("France", "Senegal", 3, 1),
    ("Iran", "New Zealand", 2, 2),
    ("Saudi Arabia", "Uruguay", 1, 1),
    ("Belgium", "Egypt", 1, 1),
    ("Spain", "Cape Verde", 0, 0),
    ("Sweden", "Tunisia", 5, 1),
    ("Ivory Coast", "Ecuador", 1, 0),
    ("Netherlands", "Japan", 2, 2),
    ("Germany", "Curacao", 7, 1),
    ("Australia", "Turkey", 2, 0),
    ("Haiti", "Scotland", 0, 1),
    ("Brazil", "Morocco", 1, 1),
    ("Qatar", "Switzerland", 1, 1),
    ("USA", "Paraguay", 4, 1),
    ("Canada", "Bosnia & Herzegovina", 1, 1),
    ("South Korea", "Czech Republic", 2, 1),
    ("Mexico", "South Africa", 2, 0),
]

name_to_fs = {
    'EE.UU.': 'USA',
    'N. Zelanda': 'New Zealand',
    'Cabo Verde': 'Cape Verde',
    'Costa de Marfil': 'Ivory Coast',
    'Bosnia H.': 'Bosnia & Herzegovina',
    'Rep. Checa': 'Czech Republic',
    'Países Bajos': 'Netherlands',
    'Corea del Sur': 'South Korea',
    'Arabia Saudita': 'Saudi Arabia',
    'RD Congo': 'D.R. Congo',
    'Escocia': 'Scotland',
    'Uzbekistán': 'Uzbekistan',
    'Argelia': 'Algeria',
    'Marruecos': 'Morocco',
    'México': 'Mexico',
    'Sudáfrica': 'South Africa',
    'Canadá': 'Canada',
    'Suiza': 'Switzerland',
    'Qatar': 'Qatar',
    'Brasil': 'Brazil',
    'Haití': 'Haiti',
    'Croacia': 'Croatia',
    'Panamá': 'Panama',
    'Inglaterra': 'England',
    'Ghana': 'Ghana',
    'Alemania': 'Germany',
    'Ecuador': 'Ecuador',
    'Curazao': 'Curacao',
    'Japón': 'Japan',
    'Suecia': 'Sweden',
    'Túnez': 'Tunisia',
    'Egipto': 'Egypt',
    'Irán': 'Iran',
    'Bélgica': 'Belgium',
    'España': 'Spain',
    'Uruguay': 'Uruguay',
    'Francia': 'France',
    'Senegal': 'Senegal',
    'Irak': 'Iraq',
    'Noruega': 'Norway',
    'Argentina': 'Argentina',
    'Austria': 'Austria',
    'Jordania': 'Jordan',
    'Colombia': 'Colombia',
    'Portugal': 'Portugal',
    'Turquía': 'Turkey',
    'Paraguay': 'Paraguay',
    'Australia': 'Australia',
    'Corea del Sur': 'South Korea',
}

with open('data.json') as f:
    d = json.load(f)

# Build set of all matches in data.json
data_matches = {}
for g in d['groups']:
    for t in g['teams']:
        for m in t['matches']:
            our_name = t['name']
            opp_flag = m['opponent']
            opp_name = None
            for g2 in d['groups']:
                for t2 in g2['teams']:
                    if t2['flag'] == opp_flag:
                        opp_name = t2['name']
                        break
            if not opp_name:
                continue
            our_fs = name_to_fs.get(our_name, our_name)
            opp_fs = name_to_fs.get(opp_name, opp_name)
            score_parts = m['score'].replace('–', '-').split('-')
            our_hs, our_as = int(score_parts[0]), int(score_parts[1])
            # Store in both directions
            data_matches[(our_fs.lower(), opp_fs.lower())] = (our_hs, our_as, our_name, opp_name)
            data_matches[(opp_fs.lower(), our_fs.lower())] = (our_as, our_hs, our_name, opp_name)

print("=== VERIFY ALL FLASHSCORE MATCHES ===\n")
errors = []
not_found = []
for t1, t2, fs_hs, fs_as in flashscore:
    key = (t1.lower(), t2.lower())
    if key in data_matches:
        our_hs, our_as, n1, n2 = data_matches[key]
        if our_hs == fs_hs and our_as == fs_as:
            print(f"  ✅ {t1} {fs_hs}-{fs_as} {t2}")
        else:
            print(f"  ❌ {t1} {fs_hs}-{fs_as} {t2} (Flashscore) vs {n1} {our_hs}-{our_as} {n2} (data.json)")
            errors.append(f"{t1} {fs_hs}-{fs_as} {t2}: data.json has {our_hs}-{our_as}")
    else:
        print(f"  ⚠️  {t1} vs {t2}: NOT FOUND in data.json (flag-level only?)")
        not_found.append(f"{t1} vs {t2}")

print(f"\nErrors: {len(errors)}")
for e in errors:
    print(f"  ❌ {e}")
print(f"Not found (probably flag-level only matches): {len(not_found)}")

# Check DG sanity
print("\n=== DG SANITY CHECK ===")
for g in d['groups']:
    total = sum(int(t['dg'].replace('+', '')) for t in g['teams'])
    status = "✅" if total == 0 else "❌"
    print(f"  {status} {g['name']}: sum = {total}")
