# ucids1 = ["US-20230404378-A1", "US-20230404439-A1", "US-20230404652-A1", "US-20230404705-A1",
#           "US-20230404755-A1", "US-20230404795-A1", "US-20230404838-A1", "US-20230404842-A1",
#           "US-20230404911-A1", "US-20230404922-A1", "US-20230404974-A1", "US-20230405015-A1",
#           "US-20230405083-A1", "US-20230405173-A1", "US-20230405175-A1", "US-20230405248-A1",
#           "US-20230405253-A1", "US-20230405279-A1", "US-20230405290-A1", "US-20230405322-A1",
#           "US-20230405362-A1", "US-20230405416-A1", "US-20230405422-A1", "US-20230405427-A1",
#           "US-20230405483-A1", "US-20230405511-A1", "US-20230405644-A1", "US-20230405714-A1",
#           "US-20230405791-A1", "US-20230405886-A1", "US-20230405901-A1", "US-20230406049-A1",
#           "US-20230406069-A1", "US-20230406500-A1", "US-20230406691-A1", "US-20230406783-A1",
#           "US-20230406853-A1", "US-20230406854-A1", "US-20230407029-A1", "US-20230407032-A1",
#           "US-20230407130-A1", "US-20230407491-A1", "US-20230407626-A1", "US-20230407662-A1"]
# ucids2 = ["US-20230397480-A1", "US-20230397527-A1", "US-20230397597-A1", "US-20230397730-A1",
#           "US-20230397764-A1", "US-20230397876-A1", "US-20230398279-A1", "US-20230398341-A1",
#           "US-20230398372-A1", "US-20230398540-A1", "US-20230398568-A1", "US-20230398710-A1",
#           "US-20230398749-A1", "US-20230399490-A1", "US-20230399582-A1", "US-20230399691-A1",
#           "US-20230399779-A1", "US-20230399940-A1", "US-20230400196-A1", "US-20230400460-A1",
#           "US-20230400521-A1", "US-20230400522-A1", "US-20230400973-A1", "US-20230401037-A1",
#           "US-20230401109-A1", "US-20230401427-A1", "US-20230401569-A1", "US-20230401602-A1",
#           "US-20230401798-A1", "US-20230401887-A1", "US-20230402148-A1", "US-20230402825-A1",
#           "US-20230402830-A1", "US-20230402838-A1", "US-20230402865-A1", "US-20230403154-A1",
#           "US-20230403210-A1", "US-20230403229-A1", "US-20230403233-A1", "US-20230403236-A1", "US-20230407130-A1", "US-20230406049-A1", "US-20230403233-A1", "US-20230406049-A1"]
import gh
search_result=[]
search_report=gh.resp["search_report"]["search_result"]
for item in search_report:
    search_result.append(item["ucid"])
print("length of search_result : ",len(search_result))    

results = ["US-20200091608-A1",
"US-20220303331-A1",
"US-20180288697-A1",
"US-20220069788-A1",
"US-20190349760-A1",
"US-20180145787-A1"]
 
# ucids1=[item.get("ucid") for item in search_result]
ucids1=search_result
ucids2=[]
common_ucids = list(set(ucids1) & set(ucids2))
print("common_ucids", common_ucids)
print("length of common_ucids", len(common_ucids))

for res1 in results:
    for i, res2 in enumerate(ucids1):
        if res1 == res2:
            print("In data1 : this is similiar %s at index : %s", res1, i)

for ucd in results:
    for j, ucds in enumerate(ucids2):
        if ucd == ucds:
            print("In data2 : this is similiar %s at index : %s", ucd, j)
