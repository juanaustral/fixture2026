#!/usr/bin/env python3
"""Sync DEFAULT_KO in index.html with current data_ko.json"""
import json

with open('data_ko.json') as f:
    data = json.load(f)
dk_str = json.dumps(data, ensure_ascii=False)

with open('index.html') as f:
    html = f.read()

# Find var DEFAULT_KO=  (not the one in data_ko.json reference)
# Look for "var DEFAULT_KO=" literal in the HTML
start = html.find('var DEFAULT_KO=')
if start == -1:
    print("ERROR: var DEFAULT_KO= not found in index.html")
    exit(1)

# Find the matching closing brace
depth = 0
end = start + len('var DEFAULT_KO=')
# skip whitespace
while end < len(html) and html[end] in ' \t\n': end += 1
if html[end] == '{':
    depth = 1
    end += 1
    while end < len(html) and depth > 0:
        if html[end] == '{': depth += 1
        elif html[end] == '}': depth -= 1
        end += 1
    # now find semicolon
    semi = end
    while semi < len(html) and html[semi] != ';': semi += 1
    semi += 1  # include semicolon

    old = html[start:semi]
    new = f"var DEFAULT_KO={dk_str};"
    html = html.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(html)
    print("DEFAULT_KO updated in index.html")
    print(f"Replaced {len(old)} chars with {len(new)} chars")
else:
    print(f"ERROR: Expected '{{' at position {end}, found '{html[end]}'")
