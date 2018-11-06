n = int(input("n = "))
a = n
n = (n + 1) // 2
h = 0
for j in range(1,n): 
    for g in range(h):
        print(' ',end = "") 
    for i in range(a):
        print('*',end = "")
    a = a + 2
    h = h - 1
    print ()
for i in range(n,0,-1):
    for g in range(h):
        print(' ',end = "")
    for e in range(a):
        print('*',end = "")
    a = a - 2
    h = h + 1
    print ()
a = 3
h = n - 2



# for i in range(n,0,-1):
#     for g in range(h):
#         print(' ',end = "")
#     for e in range(a):
#         print('*',end = "")
#     a = a - 2
#     h = h + 1
#     print ()
# a = 3
# h = n - 2