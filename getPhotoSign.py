import cv2
import numpy as np
from pdf2image import convert_from_path
poppler_path = r'C:\Users\DELL\Desktop\tesseract\poppler-24.08.0\Library\bin'

# Load image
# image = cv2.imread('formJPG/page1.jpg')
def getPhotoFromImg(pil_image):
    # Convert PIL to OpenCV image (numpy array)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    height, width = image.shape[:2]

    # Define the crop box as percentages
    x_pct, y_pct, w_pct, h_pct = 0.745, 0.105, 0.16, 0.15  # 10% from left, 40% from top, 30% width, 20% height

    # Convert to pixel values
    x = int(x_pct * width)
    y = int(y_pct * height)
    w = int(w_pct * width)
    h = int(h_pct * height)

    # Crop the image
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

   
    
def getSignFromImg(pil_image):
    
    
    # Convert PIL to OpenCV image (numpy array)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    height, width = image.shape[:2]

    # Define the crop box as percentages
    x_pct, y_pct, w_pct, h_pct = 0.65, 0.34, 0.25, 0.07  # 10% from left, 40% from top, 30% width, 20% height

    # Convert to pixel values
    x = int(x_pct * width)
    y = int(y_pct * height)
    w = int(w_pct * width)
    h = int(h_pct * height)

    # Crop the image
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

   
# getPhotoFromImg('formJPG/page1.jpg')
# getSignFromImg('formJPG/page2.jpg')

