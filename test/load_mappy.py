import mappyfile

mapfile = mappyfile.open("C:/Users/User/apps/gis/config/users/layers/arsenico.lay")

# print(mapfile)

output = mappyfile.dumps(mapfile, indent=2, spacer=" ")
print(output)