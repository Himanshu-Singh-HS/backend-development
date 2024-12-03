# haystack = "sadbutsad"
# needle = "sad"
# if needle not in haystack:
#     print('-1')
# else:
#     print("yes present but how to calculate in many times occures ")

haystack = "sadbutsad"
needle = "sad"

if needle not in haystack:
    print('-1')
else:
    # Count how many times `needle` appears in `haystack`
    count = haystack.count(needle)
    print(f"The substring '{needle}' appears {count} times in the string.")

haystack = "sadbutsad"
needle = "sad"

 
if needle not in haystack:
    print('-1')
else:
   
    indices = []
    start = 0
    
    while True:
       
        index = haystack.find(needle, start)
        
       
        if index == -1:
            break
        
        
        indices.append(index)
        
        start = index + 1
    
    print(f"The substring '{needle}' appears at indices {indices}.")
print(haystack.find(needle))

