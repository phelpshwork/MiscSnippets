# encoding with utf-8-sig makes the file open in Excel and GeoEvent without crazy chars
# code to convert a CSV file to GeoEvent-readable file

import csv
import string
inpath = r'C:\temp\temp\sigs.csv'
outpath = r'C:\temp\temp\out' 
infile = open(inpath, 'r', encoding='utf-8-sig', errors='ignore') 

with infile, open(outpath + r'\sigs_new_with_join_strip.csv', 'w', encoding='utf-8-sig') as outfile:
    text = infile.read()
    printable = set(string.printable)
    p = ''.join(filter(lambda x: x in string.printable, text))
    outfile.write(p)
    
print("Success!")

