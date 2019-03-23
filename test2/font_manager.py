import os
import matplotlib.font_manager

font = 'Ms'
msfont = os.path.basename("Arial")
for f in matplotlib.font_manager.fontManager.ttflist:
    if os.path.basename(f.fname) == msfont:
        print("<Font '%s' (%s) %s %s %s %s>" % (f.name, os.path.basename(f.fname), f.style, f.variant, f.weight, f.stretch))
        font = f.name
        break

fl = matplotlib.font_manager.fontManager.ttflist
f = fl[5]
print(f.fname)
print(f.name)
print(os.path.basename(f.fname))
print(f.weight)
print(f.style)
print(f.variant)
print(f.stretch)