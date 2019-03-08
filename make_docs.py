import csv

docpath = r"C:\Users\heat3463\Documents\data\Companies\Clearterra\demo_data\Hyderabad_test.csv"
outputloc = r"C:\Users\heat3463\Documents\data\Companies\Clearterra\demo_data\demo_output"

with open(docpath) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
# for each row in filetoread
	for row in csv_reader:
		newfilename = r"{}\{}.txt".format(outputloc, row[3]) # gives NAI
		if line_count == 0:
			# print(f'Column names are {", ".join(row)}')
			line_count += 1
		else:
			# print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
			newfile = open(newfilename, "w")
			newfile.write("DATE AND TIME: {} {}".format(row[0], "\n \n"))
			newfile.write("ACTIVITY: {} {}".format(row[1], "\n \n"))
			newfile.write("TITLE: {} {}".format(row[2], "\n \n"))
			newfile.write("NAI: {} {}".format(row[3], "\n \n"))
			newfile.write("TYPE: {} {}".format(row[4], "\n \n"))
			newfile.write("LATITUDE/LONGITUDE: {} {} {}".format(row[5], row[6], "\n \n"))
			newfile.write("DETAILS: {} {}".format(row[7], "\n \n"))
			newfile.close()
			line_count += 1
	print(f'Processed {line_count} lines.')
