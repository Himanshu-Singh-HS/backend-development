ucids1 = ["US-20230404378-A1", "US-20230404439-A1", "US-20230404652-A1", "US-20230404705-A1",
          "US-20230404755-A1", "US-20230404795-A1", "US-20230404838-A1", "US-20230404842-A1",
          "US-20230404911-A1", "US-20230404922-A1", "US-20230404974-A1", "US-20230405015-A1",
          "US-20230405083-A1", "US-20230405173-A1", "US-20230405175-A1", "US-20230405248-A1",
          "US-20230405253-A1", "US-20230405279-A1", "US-20230405290-A1", "US-20230405322-A1",
          "US-20230405362-A1", "US-20230405416-A1", "US-20230405422-A1", "US-20230405427-A1",
          "US-20230405483-A1", "US-20230405511-A1", "US-20230405644-A1", "US-20230405714-A1",
          "US-20230405791-A1", "US-20230405886-A1", "US-20230405901-A1", "US-20230406049-A1",
          "US-20230406069-A1", "US-20230406500-A1", "US-20230406691-A1", "US-20230406783-A1",
          "US-20230406853-A1", "US-20230406854-A1", "US-20230407029-A1", "US-20230407032-A1",
          "US-20230407130-A1", "US-20230407491-A1", "US-20230407626-A1", "US-20230407662-A1"]
ucids2 = ["US-20230397480-A1", "US-20230397527-A1", "US-20230397597-A1", "US-20230397730-A1",
          "US-20230397764-A1", "US-20230397876-A1", "US-20230398279-A1", "US-20230398341-A1",
          "US-20230398372-A1", "US-20230398540-A1", "US-20230398568-A1", "US-20230398710-A1",
          "US-20230398749-A1", "US-20230399490-A1", "US-20230399582-A1", "US-20230399691-A1",
          "US-20230399779-A1", "US-20230399940-A1", "US-20230400196-A1", "US-20230400460-A1",
          "US-20230400521-A1", "US-20230400522-A1", "US-20230400973-A1", "US-20230401037-A1",
          "US-20230401109-A1", "US-20230401427-A1", "US-20230401569-A1", "US-20230401602-A1",
          "US-20230401798-A1", "US-20230401887-A1", "US-20230402148-A1", "US-20230402825-A1",
          "US-20230402830-A1", "US-20230402838-A1", "US-20230402865-A1", "US-20230403154-A1",
          "US-20230403210-A1", "US-20230403229-A1", "US-20230403233-A1", "US-20230403236-A1","US-20230407130-A1", "US-20230406049-A1",]



# print(ucids1, ucids2)
print(len(ucids2+ucids1))
# if ucids1==ucids2:
#     print("yes both are similiar")
# else:
#     print("this is not similiar")
# similiar_element=[]
# unsimi_el=[]
# for ucid in ucids1:
#     for ucd2 in ucids2:
#         if ucid==ucd2:
#              similiar_element.append(ucid)
#         else:
#             unsimi_el.append(ucid)
# print("similiar element",similiar_element)
# print("unsimilar element ",unsimi_el)



common_ucids = list(set(ucids1) & set(ucids2))


unique_to_ucids1 = list(set(ucids1) - set(ucids2))
unique_to_ucids2 = list(set(ucids2) - set(ucids1))

 
all_unique_ucids = sorted(set(ucids1 + ucids2)) 

 
# print("Common UCIDs:", common_ucids)
print("UCIDs unique to ucids1", unique_to_ucids1)
# print("UCIDs unique to ucids2", unique_to_ucids2)
# print("sorted  ", all_unique_ucids)


print("Total UCIDs:", len(all_unique_ucids))

