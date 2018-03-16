import cv2
import time

endTime = time.time() + 2*60*60

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

folder = 'imgs/'
count = 0
delay = 1
while time.time() < endTime:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    frame_num = "%08d" % (count,)
    cv2.imwrite(folder + frame_num + '.jpg', frame)
    k = cv2.waitKey(1)
    count = count + 1
    time.sleep(delay)

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
