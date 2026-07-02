#!/usr/bin/env python3
"""Verify all matches in data.json against Flashscore."""
import json
import re

# Complete flag-to-English-name mapping
FLAG_MAP = {
    "🇲🇽": "Mexico", "🇿🇦": "South Africa", "🇰🇷": "South Korea", "🇨🇿": "Czech Republic",
    "🇨🇭": "Switzerland", "🇶🇦": "Qatar", "🇧🇦": "Bosnia & Herzegovina", "🇨🇦": "Canada",
    "🇧🇷": "Brazil", "🇲🇦": "Morocco", "🇭🇹": "Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿": "Scotland",
    "🇺🇸": "USA", "🇵🇾": "Paraguay", "🇦🇺": "Australia", "🇹🇷": "Turkey",
    "🇩🇪": "Germany", "🇨🇼": "Curacao", "🇨🇮": "Ivory Coast", "🇪🇨": "Ecuador",
    "🇳🇱": "Netherlands", "🇯🇵": "Japan", "🇸🇪": "Sweden", "🇹🇳": "Tunisia",
    "🇪🇬": "Egypt", "🇧🇪": "Belgium", "🇳🇿": "New Zealand", "🇮🇷": "Iran",
    "🇪🇸": "Spain", "🇨🇻": "Cape Verde", "🇸🇦": "Saudi Arabia", "🇺🇾": "Uruguay",
    "🇫🇷": "France", "🇸🇳": "Senegal", "🇮🇶": "Iraq", "🇳🇴": "Norway",
    "🇦🇷": "Argentina", "🇩🇿": "Algeria", "🇦🇹": "Austria", "🇯🇴": "Jordan",
    "🇨🇴": "Colombia", "🇺🇿": "Uzbekistan", "🇵🇹": "Portugal", "🇨🇩": "D.R. Congo",
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿": "England", "🇭🇷": "Croatia", "🇬🇭": "Ghana", "🇵🇦": "Panama",
}

# Team name -> flag
TEAM_TO_FLAG = {v: k for k, v in FLAG_MAP.items()}

# Flashscore matches: (home, away, home_score, away_score)
fs_matches = {
    ("Mexico", "South Africa"): (2, 0),
    ("South Korea", "Czech Republic"): (2, 1),
    ("USA", "Paraguay"): (4, 1),
    ("Canada", "Bosnia & Herzegovina"): (1, 1),
    ("Qatar", "Switzerland"): (1, 1),
    ("Brazil", "Morocco"): (1, 1),
    ("Haiti", "Scotland"): (0, 1),
    ("Australia", "Turkey"): (2, 0),
    ("Germany", "Curacao"): (7, 1),
    ("Netherlands", "Japan"): (2, 2),
    ("Ivory Coast", "Ecuador"): (1, 0),
    ("Sweden", "Tunisia"): (5, 1),
    ("Spain", "Cape Verde"): (0, 0),
    ("Belgium", "Egypt"): (1, 1),
    ("Saudi Arabia", "Uruguay"): (1, 1),
    ("Iran", "New Zealand"): (2, 2),
    ("France", "Senegal"): (3, 1),
    ("Iraq", "Norway"): (1, 4),
    ("Argentina", "Algeria"): (3, 0),
    ("Austria", "Jordan"): (3, 1),
    ("Portugal", "D.R. Congo"): (1, 1),
    ("England", "Croatia"): (4, 2),
    ("Ghana", "Panama"): (1, 0),
    ("Uzbekistan", "Colombia"): (1, 3),
    ("Czech Republic", "South Africa"): (1, 1),
    ("Switzerland", "Bosnia & Herzegovina"): (4, 1),
    ("Canada", "Qatar"): (6, 0),
    ("Mexico", "South Korea"): (1, 0),
    ("USA", "Australia"): (2, 0),
    ("Scotland", "Morocco"): (0, 1),
    ("Brazil", "Haiti"): (3, 0),
    ("Turkey", "Paraguay"): (0, 1),
    ("Netherlands", "Sweden"): (5, 1),
    ("Germany", "Ivory Coast"): (2, 1),
    ("Ecuador", "Curacao"): (0, 0),
    ("Tunisia", "Japan"): (0, 4),
    ("Spain", "Saudi Arabia"): (4, 0),
    ("Belgium", "Iran"): (0, 0),
    ("Uruguay", "Cape Verde"): (2, 2),
    ("New Zealand", "Egypt"): (1, 3),
    ("Argentina", "Austria"): (2, 0),
    ("France", "Iraq"): (3, 0),
    ("Norway", "Senegal"): (3, 2),
    ("Jordan", "Algeria"): (1, 2),
    ("Portugal", "Uzbekistan"): (5, 0),
    ("England", "Ghana"): (0, 0),
    ("Panama", "Croatia"): (0, 1),
    ("Colombia", "D.R. Congo"): (1, 0),
    ("Bosnia & Herzegovina", "Qatar"): (3, 1),
    ("Switzerland", "Canada"): (2, 1),
    ("Scotland", "Brazil"): (0, 3),
    ("Morocco", "Haiti"): (4, 2),
    ("South Africa", "South Korea"): (1, 0),
    ("Czech Republic", "Mexico"): (0, 3),
    ("Ecuador", "Germany"): (2, 1),
    ("Curacao", "Ivory Coast"): (0, 2),
    ("Tunisia", "Netherlands"): (1, 3),
    ("Japan", "Sweden"): (1, 1),
    ("Turkey", "USA"): (3, 2),
    ("Paraguay", "Australia"): (0, 0),
}

def find_fs_match(team_flag, opp_flag):
    """Find a Flashscore match given two flags. Returns (home_score, away_score, home_name, away_name) or None."""
    team_name = FLAG_MAP.get(team_flag)
    opp_name = FLAG_MAP.get(opp_flag)
    if not team_name or not opp_name:
        return None
    
    # Try both orderings
    key1 = (team_name, opp_name)
    key2 = (opp_name, team_name)
    
    if key1 in fs_matches:
        hs, aw = fs_matches[key1]
        return (hs, aw, team_name, opp_name)
    elif key2 in fs_matches:
        hs, aw = fs_matches[key2]
        return (aw, hs, opp_name, team_name)  # swap: team's score is away
    
    return None

with open("/root/dashboard/data.json") as f:
    data = json.load(f)

issues = []
for g in data["groups"]:
    gname = g["name"]
    for t in g["teams"]:
        tflag = None
        # Find this team's flag by looking at its opponent matches
        for m in t.get("matches", []):
            # The opponent's flag is the key
            pass
        
        for m in t.get("matches", []):
            opp_flag = m.get("opponent", "")
            team_flag = None
            # Find this team's own flag
            for other in g["teams"]:
                if other["name"] == t["name"]:
                    team_flag = other.get("flag", "")
                    break
            if not team_flag:
                continue
            
            score_raw = m.get("score", "")
            parts = score_raw.replace("–", "-").split("-")
            if len(parts) != 2:
                continue
            try:
                s1, s2 = int(parts[0]), int(parts[1])
            except:
                continue
            
            fs = find_fs_match(team_flag, opp_flag)
            if fs is None:
                tn = FLAG_MAP.get(team_flag, "?")
                on = FLAG_MAP.get(opp_flag, "?")
                issues.append(f"{gname} - {t['name']} vs {on}: NOT FOUND in Flashscore")
            else:
                fs_hs, fs_as, home_n, away_n = fs
                if s1 != fs_hs or s2 != fs_as:
                    we_are_home = (home_n == FLAG_MAP.get(team_flag))
                    issues.append(f"{gname} - {t['name']} vs {away_n if we_are_home else home_n}: data={s1}-{s2}, flashscore={fs_hs}-{fs_as} (home={home_n}, away={away_n})")

if issues:
    print("ISSUES:")
    for i in issues:
        print(f"  {i}")
else:
    print("ALL MATCHES VERIFIED - No discrepancies.")

# Check points
print("\n--- Points verification for closed groups ---")
for g in data["groups"]:
    if not g.get("cerrado", False):
        continue
    for t in g["teams"]:
        expected = 0
        for m in t.get("matches", []):
            r = m.get("result", "")
            if r == "w": expected += 3
            elif r == "d": expected += 1
        actual = t.get("pts", 0)
        if expected != actual:
            print(f"{g['name']} - {t['name']}: PTS={actual}, expected={expected}")

print("\nDone.")
