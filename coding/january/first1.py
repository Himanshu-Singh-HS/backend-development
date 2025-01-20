# l=["wwe","wer","werty","ghjk"]
# print(l[-1])
# for i in l[-1]:
#     print(i,end=' ')
# names1 = ['Amir', 'Bear', 'Charlton', 'Daman']
# names2 = names1  #shallow copy 
# names3 = names1[:]  #deep copy 
# print()

p=[23,23,222,4,56,666]
p.append([123,345])
print("pritng is p",p)
# c=p
# pp=p[:]
# pp[0]=2345
# c[-1]=9000
# print(c,p,pp)

# print(4*[3])
p[0]=8787878
# print(p)
# def f(values):
#     values[0] = 44
 
# v = [1, 2, 3]
# f(v)
# print(v)

def f(i, values = []):
    values.append(i)
    return values
 
f(1,[34])
f(2)
v = f(3,[56])
print(v)

# ans=[]
# for i in range(4):
#     for j in range(4):    m=[(i,j) for i in range(4) for j in range(4)]
#         ans.append((i,j))
# print(ans,len(ans))
        