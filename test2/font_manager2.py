import matplotlib.font_manager
flist = matplotlib.font_manager.get_fontconfig_fonts()
print(flist)
names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
print(names)

font = matplotlib.font_manager.FontProperties(family='arial')
print(font)

file = matplotlib.font_manager.findfont(font)
print(file)

#print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))



for f in matplotlib.font_manager.fontManager.ttflist:
    #if os.path.basename(f.fname) == msfont:
    #print "<Font '%s' (%s) %s %s %s %s>" % (f.name, os.path.basename(f.fname), \
    #f.style, f.variant, #f.weight, f.stretch)
    print(f.name)