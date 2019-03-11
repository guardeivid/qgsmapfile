aList = [123, 'xyz', 'zara', 'abc', 123];
bList = [123, 'manni'];
aList.extend(bList)
print "Extended List : ", aList

dict1 = {'bookA': 1, 'bookB': 2, 'bookC': 3}
dict2 = {'bookC': 2, 'bookD': 4, 'bookE': 5}
print dict1
print dict2
dict1.update(dict2)
print dict1