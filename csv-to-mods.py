import os.path
#os.path.exists(file_path)
#os.path.isfile(fname)


import csv
input_list = [] #a list of dictionary objects with the raw CSV input
output_list = [] #a list of dictionary objects that have been checked and will be outputted
invalid_list = [] #a list of dictionary objects that did not pass checks and will not be outputted

try:
	csvfile = open('input.csv')
	csv_input = csv.DictReader(csvfile)
	for row in csv_input:
		input_list.append(row)
except:
	raise ValueError('lol cannot find input.csv')

#checking for correct values in each column
for row in input_list:
	if 'uuid' in row['uuid']:
		uuidValid=True
	else:
		uuidValid=False
	if 'http://' in row['link']:
		linkValid=True
	else:
		linkValid=False
	if 'DF' in row['df'] or 'DI' in row['df']:
		DFValid=True
	else:
		DFValid=False
	if len(row['label']) > 0:
		labelValid=True
	else:
		labelValid=False
	if uuidValid and linkValid and DFValid and labelValid:
		output_list.append(row)
	else:
		invalid_list.append(row)
		
	
#open XML file
f=open('output.xml', 'w')
#XML declaration
f.write('<?xml version="1.0" encoding="UTF-8"?>')
#XML root element
f.write('\n'+'<bulkmetadata>')


for row in output_list:
	#XML child elements
	f.write('\n' + '<object pid="' + row['uuid'] + '">')
	f.write('<update type="MODS"><mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
	f.write('\n' + '<mods:titleInfo><mods:title>' + row['label'] + '</mods:title></mods:titleInfo>') 
	f.write('\n' + '<mods:identifier displayLabel="Digital Folder">' + row['df'] + '</mods:identifier>')
	f.write('\n' + '<mods:relatedItem type="isReferencedBy"><mods:location><mods:url displayLabel="Link to finding aid">' + row['link'] + '</mods:url></mods:location></mods:relatedItem>')
	f.write('\n' + '</mods:mods></update></object>')
	
#XML end root element
f.write('\n'+'</bulkmetadata>')
f.close()

print('The following items were not added to mods because they are invalid. check the contents and try again')
print(invalid_list)

csvfile.close()