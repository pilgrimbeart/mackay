# Collates all tributes into .md files by section
# Formatted with pandocs-style ":::" fenced-div blocks

import pandas as pd
import sys
import time

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTHBL_p4dyp6P3e1Htfkv68EDi1W9POHJ17Xnr0BtnzyjsZC6MymfIu9dSmAa4v9-mH7J0mJWQei00/pub?gid=45077070&single=true&output=csv"
url += f"&_cb={int(time.time())}" # Cache-busting so we always get the latest copy

df = pd.read_csv(url)  # pandas follows redirects

section_names = []
section_files = []
section_count = []

for row in df.itertuples(index=False):
    S, N, H, T = row.Section, row.Name, row.How_knew_David, row.Tribute
    if not isinstance(S,str):
        print("ENTRY NEEDS LABELLING WITH A SECTION")
        print(row)
        sys.exit(-1)
    if S not in section_names:
        f = open(S+".md","wt")
        section_names.append(S)
        section_files.append(f)
        section_count.append(1)
    else:
        i = section_names.index(S)
        f = section_files[i]
        section_count[i] += 1
    f.write("::: tribute\n")
    f.write(T + "\n")
    f.write("\n")
    f.write("::: attrib\n")
    if isinstance(N,str):
        f.write("- "+N+"\n")
    else:
        f.write("- (anonymous)\n")
    if isinstance(H,str):
        f.write("("+H+")\n")
    f.write(":::\n")
    f.write(":::\n")

total = 0
print("Section Entries")
for i in range(len(section_names)):
    print(section_names[i]," ", section_count[i])
    total += section_count[i]
print("Total:",total)
