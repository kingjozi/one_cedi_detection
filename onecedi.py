import cv2
import numpy as np
from PIL import Image
import easyocr

camera = cv2.VideoCapture(0)

while True:
    _,frame = camera.read()
    resize_frame = cv2.resize(frame, (500,300), interpolation = cv2.INTER_AREA)

    lower_bound_red = [173,100,100]
    upper_bound_red = [180,255,255]

    lowerLimit = np.array(lower_bound_red)
    upperLimit = np.array(upper_bound_red)

    hsv_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame,lowerLimit,upperLimit)

    pil_image = Image.fromarray(mask)
    bbox = pil_image.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(resize_frame, (x1,y1), (x2,y2), (0,255,255), 3)

    cv2.imshow('frame',resize_frame)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite('oneCedi.jpg',resize_frame)
        break

camera.release()
cv2.destroyAllWindows()

im_path = ''
read_image = cv2.imread(im_path)
texts = easyocr.Reader(['en'], gpu = False)
text = texts.readtext(read_image)

texts_seen = []
for info in text:
    bbox, identified_text, score = info
    texts_seen.append(identified_text)

concat_texts = " ".join(texts_seen)

if 'BANK OF GHANA' and 'One Cedi' in concat_texts:
    print("One Cedi identified")
else:
    print("Not sure what this is")
