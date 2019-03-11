import os
import re
import matplotlib.font_manager

fontsetpath = "C:\\Users\\User\\apps\\gis\\config\\templates\\font.list"
def fonts(fontsetpath):
    f = {}
    if os.path.isfile(fontsetpath):
        with open(fontsetpath, "r") as file:
            for line in file:
                line = line.strip().split()
                if len(line) == 2:
                    f[line[0]] = line[1]
    return f

def getFont(msfont):
    """docstring for __getFont"""
    font = 'MS Shell Dlg 2'

    if msfont != '':
        msfont = os.path.basename(msfont)
        for f in matplotlib.font_manager.fontManager.ttflist:
            #print(os.path.basename(msfont))
            if os.path.basename(f.fname) == msfont:
                print "<Font '%s' (%s) %s %s %s %s>" % (f.name, os.path.basename(f.fname), \
                f.style, f.variant, f.weight, f.stretch)
                font = f.name
                break
    return font

f = fonts(fontsetpath)
#print(fonts(fontsetpath))
msfont = f['comic-sans-ms']
print(msfont)
print(os.path.basename(msfont))
print(getFont(msfont))

"""
for c in ['R', 'G', 'B', 'A']:
    print(c)
"""
al = "left2"
ALIGN = {"left": "0", "center": "1", "right": "2"}
if al in ALIGN:
    print(ALIGN[al])