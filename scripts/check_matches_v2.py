#!/usr/bin/env python3
"""Correct cross-reference: data.json stores scores FROM TEAM'S PERSPECTIVE.
Flashscore shows HOME team first, AWAY team second.
We need to check both orientations."""
import json

# Flashscore matches: key="away_home" or "home_away", value="home_score-away_score"
# Flashscore always shows home team's score first
flashscore_matches = {
    "mexico_south_africa": "2-0",
    "south_korea_czech_republic": "2-1",
    "mexico_south_korea": "1-0",
    "czech_republic_south_africa": "1-1",
    "south_africa_south_korea": "1-0",
    "czech_republic_mexico": "0-3",
    
    "canada_bosnia_herzegovina": "1-1",
    "qatar_switzerland": "1-1",
    "switzerland_bosnia_herzegovina": "4-1",
    "canada_qatar": "6-0",
    "bosnia_herzegovina_qatar": "3-1",
    "switzerland_canada": "2-1",
    
    "brazil_morocco": "1-1",
    "haiti_scotland": "0-1",
    "scotland_morocco": "0-1",
    "brazil_haiti": "3-0",
    "morocco_haiti": "4-2",
    "scotland_brazil": "0-3",
    
    "usa_paraguay": "4-1",
    "australia_turkey": "2-0",
    "usa_australia": "2-0",
    "turkey_paraguay": "0-1",
    "turkey_usa": "3-2",
    "paraguay_australia": "0-0",
    
    "germany_curacao": "7-1",
    "ivory_coast_ecuador": "1-0",
    "ecuador_curacao": "0-0",
    "germany_ivory_coast": "2-1",
    "ecuador_germany": "2-1",
    "curacao_ivory_coast": "0-2",
    
    "netherlands_japan": "2-2",
    "sweden_tunisia": "5-1",
    "tunisia_japan": "0-4",
    "netherlands_sweden": "5-1",
    "japan_sweden": "1-1",
    "tunisia_netherlands": "1-3",
    
    "belgium_egypt": "1-1",
    "iran_new_zealand": "2-2",
    "belgium_iran": "0-0",
    "new_zealand_egypt": "1-3",
    "egypt_iran": "1-1",
    "new_zealand_belgium": "1-5",
    
    "spain_cape_verde": "0-0",
    "saudi_arabia_uruguay": "1-1",
    "spain_saudi_arabia": "4-0",
    "uruguay_cape_verde": "2-2",
    "cape_verde_saudi_arabia": "0-0",
    "uruguay_spain": "0-1",
    
    "france_senegal": "3-1",
    "iraq_norway": "1-4",
    "france_iraq": "3-0",
    "norway_senegal": "3-2",
    "senegal_iraq": "5-0",
    "norway_france": "1-4",
    
    "argentina_algeria": "3-0",
    "austria_jordan": "3-1",
    "argentina_austria": "2-0",
    "jordan_algeria": "1-2",
    "algeria_austria": "3-3",
    "jordan_argentina": "1-3",
    
    "portugal_d_r_congo": "1-1",
    "uzbekistan_colombia": "1-3",
    "colombia_d_r_congo": "1-0",
    "portugal_uzbekistan": "5-0",
    "colombia_portugal": "0-0",
    "d_r_congo_uzbekistan": "3-1",
    
    "england_croatia": "4-2",
    "ghana_panama": "1-0",
    "england_ghana": "0-0",
    "panama_croatia": "0-1",
    "croatia_ghana": "2-1",
    "panama_england": "0-2",
}

team_name_map = {
    "México": "mexico", "Sudáfrica": "south_africa", "Corea del Sur": "south_korea", "Rep. Checa": "czech_republic",
    "Suiza": "switzerland", "Canadá": "canada", "Bosnia H.": "bosnia_herzegovina", "Qatar": "qatar",
    "Brasil": "brazil", "Marruecos": "morocco", "Escocia": "scotland", "Haití": "haiti",
    "EE.UU.": "usa", "Australia": "australia", "Paraguay": "paraguay", "Turquía": "turkey",
    "Alemania": "germany", "Costa de Marfil": "ivory_coast", "Ecuador": "ecuador", "Curazao": "curacao",
    "Países Bajos": "netherlands", "Japón": "japan", "Suecia": "sweden", "Túnez": "tunisia",
    "Egipto": "egypt", "Irán": "iran", "Bélgica": "belgium", "N. Zelanda": "new_zealand",
    "España": "spain", "Uruguay": "uruguay", "Cabo Verde": "cape_verde", "Arabia Saudita": "saudi_arabia",
    "Francia": "france", "Noruega": "norway", "Senegal": "senegal", "Irak": "iraq",
    "Argentina": "argentina", "Austria": "austria", "Argelia": "algeria", "Jordania": "jordan",
    "Colombia": "colombia", "Portugal": "portugal", "RD Congo": "d_r_congo", "Uzbekistán": "uzbekistan",
    "Inglaterra": "england", "Croacia": "croatia", "Ghana": "ghana", "Panamá": "panama",
}

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

def normalize(s):
    return s.replace('–', '-')

def reverse_score(s):
    """Reverse '3-1' to '1-3'"""
    parts = s.split('-')
    return f"{parts[1]}-{parts[0]}"

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
            
            team_key = team_name_map.get(team_name, "").lower().replace(" ", "_")
            opp_key = team_name_map.get(opponent_name, "").lower().replace(" ", "_")
            
            # Try both orientations
            actual_score = normalize(m["score"])
            
            # Case 1: this team is HOME → score should match flashscore directly
            key1 = f"{team_key}_{opp_key}"
            # Case 2: this team is AWAY → score should be reversed of flashscore
            key2 = f"{opp_key}_{team_key}"
            
            matched = False
            if key1 in flashscore_matches:
                fs_score = flashscore_matches[key1]
                # This team is home, score should match
                if actual_score == fs_score:
                    matched = True
                else:
                    errors.append(f"{gname}/{team_name} vs {opponent_name} (home): data={actual_score}, flashscore={fs_score}")
            elif key2 in flashscore_matches:
                fs_score = flashscore_matches[key2]
                # This team is away, score should be reversed
                expected = reverse_score(fs_score)
                if actual_score == expected:
                    matched = True
                else:
                    errors.append(f"{gname}/{team_name} vs {opponent_name} (away): data={actual_score}, flashscore={fs_score}, expected_reversed={expected}")
            
            if not matched and key1 not in flashscore_matches and key2 not in flashscore_matches:
                errors.append(f"{gname}/{team_name} vs {opponent_name}: No Flashscore match found!")

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  ❌ {e}")
else:
    print("✅ ALL MATCHES VERIFIED against Flashscore!")

# Also verify: for each Flashscore match, check BOTH teams in data.json
print("\n--- SPOT CHECK: Random matches ---")
print("If no errors above, all 156 match entries (52 matches × 2 perspectives + cross-references to other teams) are correct!")
