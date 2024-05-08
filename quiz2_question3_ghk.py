mylist = [2, 8, 64, 16, 2, 4, 4]
for x in mylist:
    if mylist.count(x) == 1:
        continue
    elif mylist.count(x) >= 2:
        print ("The list provided contains duplicate values")
        break
else:
    print ("The list provided does not contain duplicate values")
