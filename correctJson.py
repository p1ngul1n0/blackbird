import json

file = open('data copy.json', 'r+')
searchData = json.load(file)

i = 1
for z in searchData['sites']:
    z['id'] = i
    i += 1

file.seek(0)

json.dump(searchData, file,indent=4, sort_keys=True)