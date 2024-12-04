import json,requests,pprint
with open("rough/output3/results.json", 'r') as file:
    data = json.load(file)
# print(data)
unique_ucids = {}

for patent in data["patents"]:
    patent_number=patent["patent_number"]
    publication_date = patent["publication_date"]
    x,y,z = patent_number.split("-")
    _ucid= f'{x}{y}'
    if _ucid in unique_ucids:
        if publication_date > unique_ucids[_ucid][0]:
            unique_ucids[_ucid]=(publication_date,patent_number)
    else:
        unique_ucids[_ucid]=(publication_date,patent_number)
pprint.pprint(unique_ucids,width=150)
print(len(unique_ucids))

# for i in unique_ucids:
#     if i == 'CN101460863':
#         print(unique_ucids[i])
