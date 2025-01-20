#shaloow copy 
#deep copy 
# =

#shallow copy example  with 1d dimension matrix or single list 
import copy
lst1=[23,34,556,3,2,45,8]
lst2 = copy.copy(lst1)
print("this is memory location",id(lst1),id(lst2))
lst2[0]=2345
print(lst2,id(lst2))
print(lst1,id(lst1))
for i in range(2):
    print()
    
# shallow copy example with 2d dimension or 2d matrix 

ls1=[10,23,56,[78,34,899]]
ls2=copy.copy(ls1)
ls2[3][0] = 789
print(ls2,id(ls2))
print(ls1,id(ls1))


for i in range(2):
    print()
    
#deepcopy top-level container and all the nested elements.
# A deep copy creates a completely independent copy of the entire structure, including all nested objects inside it.
lst1=[23,34,556,3,2,45,8,[78,34,899]]
ls2=copy.deepcopy(lst1)
ls2[7][0]=22222
print(ls2,ls1)

# = assign operator 

a=lst1=[23,34,556,3,2,45,8,[78,34,899]]
b=a
b[7][0]=23456
print(a,b) 


