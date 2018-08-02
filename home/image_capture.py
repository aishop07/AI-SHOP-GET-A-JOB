import cv2
import time
def photogetter():
    camera = cv2.VideoCapture(0)
    print('請看鏡頭，按下空白杻拍照')
    while(True):
        # Capture frame-by-frame
        ret, frame = camera.read()
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            for i in range(25):
                time.sleep(1)
                return_value, image = camera.read()
                cv2.imwrite('.\\face_recognition\\training-data\s1\\'+str(i)+'.png', image)
            break
    camera.release()
    cv2.destroyAllWindows() 