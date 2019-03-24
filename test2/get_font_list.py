import os
def get_font_list():
    fonts = []
    for font_path in ["/Windows/Fonts", "/Library/Fonts", os.path.expanduser("~/Library/Fonts")]:
        if os.path.isdir(font_path):
            fonts.extend(
                [os.path.join(font_path, cur_font) 
                 for cur_font in os.listdir(font_path)
                ]
            )
    return fonts
    
print(get_font_list())