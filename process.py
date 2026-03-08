# Collates all tributes into .md files by section
# Formatted with pandocs-style ":::" fenced-div blocks

import pandas as pd
import sys
import time
import random

DIR = "tmp/"

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTHBL_p4dyp6P3e1Htfkv68EDi1W9POHJ17Xnr0BtnzyjsZC6MymfIu9dSmAa4v9-mH7J0mJWQei00/pub?gid=45077070&single=true&output=csv"
url += f"&_cb={int(time.time())}" # Cache-busting so we always get the latest copy

df = pd.read_csv(url)  # pandas follows redirects

section_names = []
section_tributes = [] 

def normalise_for_pdf(s):
    if s is None:
        return ""
    s = str(s)
    s = s.replace("\ufe0f", "")   # drop variation selector-16
    s = s.replace("❤", "♥")       # use U+2665 (widely supported)
    return s


# Read in all tributes, and store by section name
for row in df.itertuples(index=False):
    S, N, H, T = row.Section, row.Name, row.How_knew_David, row.Tribute
    T = normalise_for_pdf(T)
    if not isinstance(S,str):
        print("ENTRY NEEDS LABELLING WITH A SECTION - PUTTING IN 'GENERAL'")
        print(row)
        S = "GENERAL" # Default
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
    if isinstance(N,str):
        tribute += N+"\n"
    else:
        tribute += "Anonymous\n"
    if isinstance(H,str):
        tribute += "(" + H + ")\n"
    tribute += ":::\n"
    tribute += ":::\n"
    section_tributes[i].append(tribute)

# Create files
for i in range(len(section_names)):
    S = section_names[i]
    f = open(DIR + S + ".md","wt")
    random.shuffle(section_tributes[i]) # Put tributes in random order
    count = 0
    for j in range(len(section_tributes[i])):
        f.write(section_tributes[i][j])
        count += len(section_tributes[i][j])
    f.close()
    print(S,len(section_tributes[i]),"tributes",count,"chars")
