from PIL import ImageGrab as img
from io import BytesIO
import PIL

img_byte_arr = BytesIO()
screenshot = img.grab()
screenshot = screenshot.convert("RGB")
screenshot = screenshot.resize(size= (1280, 800))
screenshot.save(img_byte_arr, format= "JPEG" )
img_byte_arr.seek(0)
#img_bytes = img_byte_arr.getvalue()

#print(len(img_bytes))
opendimg = PIL.Image.open(img_byte_arr)
opendimg.show()