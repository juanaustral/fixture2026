#!/usr/bin/env python3
"""Cross-reference data.json matches against Flashscore data."""
import json

# Flashscore results extracted via browser_console with structured scores
flashscore_matches = {
    # Format: "away_team_home_team": score  (normalized for comparison)
    # Group A
    "mexico_south_africa": "2-0",     # 11.06. (opener)
    "south_korea_czech_republic": "2-1", # 11.06.
    "mexico_south_korea": "1-0",      # 18.06.
    "czech_republic_south_africa": "1-1", # 18.06.
    "south_africa_south_korea": "1-0",   # 24.06.
    "czech_republic_mexico": "0-3",      # 24.06.
    
    # Group B
    "canada_bosnia_herzegovina": "1-1",  # 12.06.
    "qatar_switzerland": "1-1",          # 13.06.
    "switzerland_bosnia_herzegovina": "4-1", # 18.06.
    "canada_qatar": "6-0",               # 18.06.
    "bosnia_herzegovina_qatar": "3-1",   # 24.06.
    "switzerland_canada": "2-1",         # 24.06.
    
    # Group C
    "brazil_morocco": "1-1",      # 13.06.
    "haiti_scotland": "0-1",      # 13.06.
    "scotland_morocco": "0-1",    # 19.06.
    "brazil_haiti": "3-0",        # 19.06.
    "morocco_haiti": "4-2",       # 24.06.
    "scotland_brazil": "0-3",     # 24.06.
    
    # Group D
    "usa_paraguay": "4-1",     # 12.06.
    "australia_turkey": "2-0", # 14.06.
    "usa_australia": "2-0",    # 19.06.
    "turkey_paraguay": "0-1",  # 20.06.
    "turkey_usa": "3-2",       # 25.06.
    "paraguay_australia": "0-0", # 25.06.
    
    # Group E
    "germany_curacao": "7-1",      # 14.06.
    "ivory_coast_ecuador": "1-0",  # 14.06.
    "ecuador_curacao": "0-0",      # 20.06.
    "germany_ivory_coast": "2-1",  # 20.06.
    "ecuador_germany": "2-1",      # 25.06.
    "curacao_ivory_coast": "0-2",  # 25.06.
    
    # Group F
    "netherlands_japan": "2-2", # 14.06.
    "sweden_tunisia": "5-1",    # 14.06.
    "tunisia_japan": "0-4",     # 21.06.
    "netherlands_sweden": "5-1", # 20.06.
    "japan_sweden": "1-1",      # 25.06.
    "tunisia_netherlands": "1-3", # 25.06.
    
    # Group G
    "belgium_egypt": "1-1",   # 15.06.
    "iran_new_zealand": "2-2", # 15.06.
    "belgium_iran": "0-0",    # 21.06.
    "new_zealand_egypt": "1-3", # 21.06.
    "egypt_iran": "1-1",      # 27.06.
    "new_zealand_belgium": "1-5", # 27.06.
    
    # Group H
    "spain_cape_verde": "0-0",     # 15.06.
    "saudi_arabia_uruguay": "1-1", # 15.06.
    "spain_saudi_arabia": "4-0",   # 21.06.
    "uruguay_cape_verde": "2-2",   # 21.06.
    "cape_verde_saudi_arabia": "0-0", # 26.06.
    "uruguay_spain": "0-1",         # 26.06.
    
    # Group I
    "france_senegal": "3-1",  # 16.06.
    "iraq_norway": "1-4",     # 16.06.
    "france_iraq": "3-0",     # 22.06.
    "norway_senegal": "3-2",  # 22.06.
    "senegal_iraq": "5-0",    # 26.06.
    "norway_france": "1-4",   # 26.06.
    
    # Group J
    "argentina_algeria": "3-0", # 16.06.
    "austria_jordan": "3-1",    # 17.06.
    "argentina_austria": "2-0", # 22.06.
    "jordan_algeria": "1-2",    # 23.06.
    "algeria_austria": "3-3",   # 27.06.
    "jordan_argentina": "1-3",  # 27.06.
    
    # Group K
    "portugal_d_r_congo": "1-1", # 17.06.
    "uzbekistan_colombia": "1-3", # 17.06.
    "colombia_d_r_congo": "1-0",  # 23.06.
    "portugal_uzbekistan": "5-0", # 23.06.
    "colombia_portugal": "0-0",   # 27.06.
    "d_r_congo_uzbekistan": "3-1", # 27.06.
    
    # Group L
    "england_croatia": "4-2",  # 17.06.
    "ghana_panama": "1-0",     # 17.06.
    "england_ghana": "0-0",    # 23.06.
    "panama_croatia": "0-1",   # 23.06.
    "croatia_ghana": "2-1",    # 27.06.
    "panama_england": "0-2",   # 27.06.
}

# Team name mapping from data.json to Flashscore keys
# Flashscore uses short team names. We need to map opponents in data.json
# to the Flashscore match keys.

team_name_map = {
    "México": "mexico",
    "Sudáfrica": "south_africa",
    "Corea del Sur": "south_korea",
    "Rep. Checa": "czech_republic",
    "Suiza": "switzerland",
    "Canadá": "canada",
    "Bosnia H.": "bosnia_herzegovina",
    "Qatar": "qatar",
    "Brasil": "brazil",
    "Marruecos": "morocco",
    "Escocia": "scotland",
    "Haití": "haiti",
    "EE.UU.": "usa",
    "Australia": "australia",
    "Paraguay": "paraguay",
    "Turquía": "turkey",
    "Alemania": "germany",
    "Costa de Marfil": "ivory_coast",
    "Ecuador": "ecuador",
    "Curazao": "curacao",
    "Países Bajos": "netherlands",
    "Japón": "japan",
    "Suecia": "sweden",
    "Túnez": "tunisia",
    "Egipto": "egypt",
    "Irán": "iran",
    "Bélgica": "belgium",
    "N. Zelanda": "new_zealand",
    "España": "spain",
    "Uruguay": "uruguay",
    "Cabo Verde": "cape_verde",
    "Arabia Saudita": "saudi_arabia",
    "Francia": "france",
    "Noruega": "norway",
    "Senegal": "senegal",
    "Irak": "iraq",
    "Argentina": "argentina",
    "Austria": "austria",
    "Argelia": "algeria",
    "Jordania": "jordan",
    "Colombia": "colombia",
    "Portugal": "portugal",
    "RD Congo": "d_r_congo",
    "Uzbekistán": "uzbekistan",
    "Inglaterra": "england",
    "Croacia": "croatia",
    "Ghana": "ghana",
    "Panamá": "panama",
}

# Flag-to-name mapping (from data.json)
flag_to_name = {
    "🇲🇽": "México", "🇿🇦": "Sudáfrica", "🇰🇷": "Corea del Sur", "🇨🇿": "Rep. Checa",
    "🇨🇭": "Suiza", "🇨🇦": "Canadá", "🇧🇦": "Bosnia H.", "🇶🇦": "Qatar",
    "🇧🇷": "Brasil", "🇲🇦": "Marruecos", "🏴󠁧󠁢󠁳󠁣󠁴󠁿": "Escocia", "🇭🇹": "Haití",
    "🇺🇸": "EE.UU.", "🇦🇺": "Australia", "🇵🇾": "Paraguay", "🇹🇷": "Turquía",
    "🇩🇪": "Alemania", "🇨🇮": "Costa de Marfil", "🇪🇨": "Ecuador", "🇨🇼": "Curazao",
    "🇳🇱": "Países Bajos", "🇯🇵": "Japón", "🇸🇪": "Suecia", "🇹🇳": "Túnez",
    "🇪🇬": "Egipto", "🇮🇷": "Irán", "🇧🇪": "Bélgica", "🇳🇿": "N. Zelanda",
    "🇪🇸": "España", "🇺🇾": "Uruguay", "🇨🇻": "Cabo Verde", "🇸🇦": "Arabia Saudita",
    "🇫🇷": "Francia", "🇳🇴": "Noruega", "🇸🇳": "Senegal", "🇮🇶": "Irak",
    "🇦🇷": "Argentina", "🇦🇹": "Austria", "🇩🇿": "Argelia", "🇯🇴": "Jordania",
    "🇨🇴": "Colombia", "🇵🇹": "Portugal", "🇨🇩": "RD Congo", "🇺🇿": "Uzbekistán",
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿": "Inglaterra", "🇭🇷": "Croacia", "🇬🇭": "Ghana", "🇵🇦": "Panamá",
}

def normalize_score(s):
    """Convert '0–2' to '0-2' for comparison"""
    return s.replace('–', '-')

def get_match_key(team_a_name, team_b_name):
    """Get the flashscore lookup key for a match between two teams."""
    a = team_name_map.get(team_a_name, "").lower().replace(" ", "_")
    b = team_name_map.get(team_b_name, "").lower().replace(" ", "_")
    
    key1 = f"{a}_{b}"
    key2 = f"{b}_{a}"
    
    if key1 in flashscore_matches:
        return key1
    if key2 in flashscore_matches:
        return key2
    return None

with open("/root/dashboard/data.json") as f:
    data = json.load(f)

errors = []

for g in data["groups"]:
    gname = g["name"]
    for t in g["teams"]:
        team_name = t["name"]
        for m in t["matches"]:
            opponent_flag = m["opponent"]
            opponent_name = flag_to_name.get(opponent_flag, opponent_flag)
            
            key = get_match_key(team_name, opponent_name)
            if key:
                expected_score = flashscore_matches[key]
                actual_score = normalize_score(m["score"])
                
                if actual_score != expected_score:
                    errors.append(f"{gname}/{team_name} vs {opponent_name}: data.json says {actual_score}, Flashscore says {expected_score} (key={key})")
            else:
                errors.append(f"{gname}/{team_name} vs {opponent_name}: No Flashscore match found!")

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  ❌ {e}")
else:
    print("✅ ALL MATCHES VERIFIED against Flashscore!")
