# Collates all tributes into .md files by section
# Formatted with pandocs-style ":::" fenced-div blocks

from io import StringIO
import pandas as pd
import random
import requests
import sys
import time

DIR = "tmp/"
SHUFFLE_SEED = 20260313

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTHBL_p4dyp6P3e1Htfkv68EDi1W9POHJ17Xnr0BtnzyjsZC6MymfIu9dSmAa4v9-mH7J0mJWQei00/pub?gid=45077070&single=true&output=csv"
url += f"&_cb={time.time_ns()}"  # Stronger cache-busting than second-resolution timestamps

response = requests.get(
    url,
    headers={
        "Cache-Control": "no-cache, max-age=0",
        "Pragma": "no-cache",
    },
    timeout=30,
)
response.raise_for_status()
df = pd.read_csv(StringIO(response.content.decode("utf-8-sig")))

section_names = []
section_tributes = [] 

def normalise_for_pdf(s):
    if s is None:
        return ""
    s = str(s)
    s = s.replace("\ufe0f", "")   # drop variation selector-16
    s = s.replace("❤", "♥")       # use U+2665 (widely supported)
    return s

def clean_text_field(s):
    if not isinstance(s, str):
        return s
    return s.strip()


# Read in all tributes, and store by section name
for row in df.itertuples(index=False):
    S, N, H, T, I = row.Section, row.Name, row.How_knew_David, row.Tribute, row.Name_for_index
    S = clean_text_field(S)
    N = clean_text_field(N)
    H = clean_text_field(H)
    I = clean_text_field(I)
    if not isinstance(T,str):
        print("MISSING TRIBUTE!")
        print(row)
        sys.exit(-1)
    T = normalise_for_pdf(T)
    if not isinstance(S,str):
        print("ENTRY NEEDS LABELLING WITH A SECTION")
        print(row)
        sys.exit(-1)
    if S not in section_names:
        section_names.append(S)
        section_tributes.append([])
        i = len(section_names)-1
    else:
        i = section_names.index(S)
    tribute = ""
    tribute += "::: {.tribute}\n"
    tribute += T + "\n"
    tribute += "\n"
    tribute += "::: {.attrib}\n" 
    if isinstance(N,str) and isinstance(I,str):
        tribute += N+"\index{" + I + "|hyperpage}\n"
    else:
        tribute += "Anonymous\n"
    if isinstance(H,str):
        tribute += "(" + H + ")\n"
    tribute += ":::\n"
    tribute += ":::\n"
    section_tributes[i].append(tribute)

# Create files
random.seed(SHUFFLE_SEED)
for i in range(len(section_names)):
    S = section_names[i]
    f = open(DIR + S + ".md","wt")
    random.shuffle(section_tributes[i]) # Put tributes in deterministic pseudo-random order
    count = 0
    for j in range(len(section_tributes[i])):
        f.write(section_tributes[i][j])
        count += len(section_tributes[i][j])
    f.close()
    print(S,len(section_tributes[i]),"tributes",count,"chars")
