database = QFontDatabase()
f = database.font('arial', 'normal', 12)
print(f)

print(database.styles(f.family()))
print(f.family())



for family in database.families():
    #print()
    #print(family)
    for style in database.styles(family):
        #print(style)
        pass

#print(QFontDatabase.writingSystemName(QFontDatabase.Any))