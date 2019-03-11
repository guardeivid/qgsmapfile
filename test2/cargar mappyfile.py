
import mappyfile

s = '''
    LAYER
        NAME 'b_act_industrial'
        TYPE POLYGON
        CONNECTIONTYPE postgis
        CONNECTION "dbname='ada' host=localhost port=5432 user='postgres' password='123456' options='-c client_encoding=LATIN1'" #INCLUDE "../../connection/latin.con"
        DATA 'geom FROM catastro.partidos USING UNIQUE id USING srid=22185'
        PROCESSING "CLOSE_CONNECTION=DEFER"
        PROCESSING "LABEL_NO_CLIP=True"
        labelmaxscaledenom 1
        CLASS
            NAME 'Actividad Industrial'
            #EXPRESSION ''
            #TEXT "1"
            STYLE
                COLOR 231 72 50
                OUTLINECOLOR 28 7 4
                WIDTH 0.5
                ANGLE auto
            END

        END
        CLASS
            NAME 'Actividad Industrial'
            STYLE
                COLOR 231 72 50
                OUTLINECOLOR 28 7 4
                WIDTH 0.5
                ANGLE AUTO
            END
            LABEL
                TEXT "1"
                SIZE [size]
                COLOR 255 255 255
                #EXPRESSION ([wspeed] > 20 and [wspeed] <= 30)
                STYLE
                    GEOTRANSFORM labelpoly
                    COLOR 0 0 0
                END
                STYLE
                    GEOTRANSFORM labelpoly
                    COLOR 10 10 10
                END
                STYLE
                    GEOTRANSFORM labelpoly
                    COLOR 20 20 20
                END
            END
        END
    END
'''
mlayer = mappyfile.loads(s)
#print(mlayer)

#s2 = mappyfile.dumps(mlayer, indent=4, spacer=' ', quote='"', newlinechar='\n')
#print(s2)


#print(mlayer["__type__"])
print((mlayer["classes"][1]["labels"][0]["styles"][3-1]))




"""
num_classes = 0
num_labels = 0
exp_label = False
exp_class = True
max_label = False
min_label = False
max_class = False
min_class = False
text_class = True
text_label = True

for c in mlayer.get("classes", []):
    num_classes += 1
    if num_classes == 1:
        text_class = c.get("text", True)
    else:
        if text_class != c.get("text", True):
            text_class = False
    if num_classes == 1:
        exp_class = c.get("expression", True)
    else:
        if exp_class != c.get("expression", True):
            exp_class = False

    for l in c.get("labels", []):
        num_labels += 1
        if num_labels == 1:
            text_label = l.get("text", True)
        else:
            if text_label != l.get("text", True):
                text_label = False
        if l.get("expression"):
            exp_label = True
        if l.get("maxscaledenom"):
            max_label = True
        if l.get("minscaledenom"):
            min_label = True

    if num_labels == 1:
        if c.get("maxscaledenom"):
            max_class = True
        if c.get("minscaledenom"):
            min_class = True

labelmaxscaledenom = mlayer.get("labelmaxscaledenom", -1)
labelminscaledenom = mlayer.get("labelminscaledenom", -1)

print("labelmaxscaledenom:", labelmaxscaledenom)
print("labelminscaledenom:", labelminscaledenom)
print("num_classes:", num_classes)
print("num_labels:", num_labels)
print("exp_label:", exp_label, "Defecto: False")
print("max_label:", max_label, "Defecto: False")
print("min_label:", min_label, "Defecto: False")
print("text_class:", text_class, "Defecto: True")
print("text_label:", text_label, "Defecto: True")
print("exp_class:", exp_class, "Defecto: True")
print("max_class:", max_class, "Defecto: False")
print("min_class:", min_class, "Defecto: False")

if num_labels:
    if (num_labels == num_classes or \
        (num_labels == 1 and not max_class and not min_class)) \
    and text_class and text_label and exp_class and \
    not exp_label and not max_label and not min_label and \
    labelmaxscaledenom == -1 and labelminscaledenom == -1:
        print("simple")
    else:
        print("rule-based")
else:
    print("no label")
"""

