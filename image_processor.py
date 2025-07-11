import os, base64
 
# with open("trail.png","rb") as f:
#     # b64encode是编码，b64decode是解码
#     base64_data = base64.b64encode(f.read())
#     print(base64_data)#输出生成的base64码

from PIL import Image
filename = r'app.png'
img = Image.open(filename)

img.save('fubon.ico')
img.show()

