# encoding with utf-8-sig makes the file open in Excel and GeoEvent without crazy chars
# code to convert a CSV file to GeoEvent-readable file

import csv
#inpath = r'C:\temp\temp\locatext_out.csv'
inpath = r'C:\temp\temp\sigs.csv'
outpath = r'C:\temp\temp\out' 
infile = open(inpath, 'r', encoding='utf-8-sig', errors='ignore') 

# with infile as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row[0])

with infile, open(outpath + r'\sigs_new.csv', 'w', encoding='utf-8-sig') as outfile:
    text = infile.read()
    # process Unicode text
    outfile.write(text)

print("Success!")
