from django.shortcuts import render,redirect
from django.http import HttpResponse
import numpy as np
import cv2

# Create your views here.
def index(request):
    return render(request,'photo/index.html',locals())

def getphoto(request):
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        # cv2.imshow('gray',gray)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cv2.imwrite("./images/test.jpg", frame)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    # return render(request,'home/index.html',locals())
    return HttpResponse('123')