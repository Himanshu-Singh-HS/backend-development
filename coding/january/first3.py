ls1=[10,23,56,[78,34,899]]
ls2=ls1[:]
# ls1[3][0]=234
ls2[0]=56789
print(ls2)
print(ls1)


#immmutable objects - integes, string , tuple, float , frozenset(immutable)
a=10
print(id(a))
a=100
print(id(a))


