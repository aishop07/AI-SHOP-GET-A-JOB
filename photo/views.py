from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
import numpy as np
import cv2
import paramiko 
# from time import sleep

# Create your views here.
def index(request):
    now = datetime.datetime.now
    return render(request,'photo/index.html',locals())

def takephoto(request):
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
            cv2.imwrite("./photo/static/images/test.jpg", frame)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    #將檔案上傳至Linux
    t = paramiko.Transport(('192.168.1.101',22))
    t.connect(username = 'pi', password = 'raspberry')
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/pi/test/test.jpg'
    localpath='./photo/static/images/test.jpg'


    sftp.put(localpath,remotepath) #上传文件
    sftp.close()
    t.close()

    #執行臉部偵測(fdetect2.py))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.1.101",22,"pi", "raspberry")
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 fdetect2.py")
    print(stdout.readlines())
    ssh.close()

    # return render(request,'home/index.html',locals())
    return HttpResponse('123')

    
def getphoto(request):
    t = paramiko.Transport(('192.168.1.101',22))
    t.connect(username = 'pi', password = 'raspberry')
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/pi/test/test_result.jpg'
    localpath='./photo/static/images/test_result.jpg'

    sftp.get(remotepath,localpath) #上传文件
    sftp.close()
    t.close()
    return HttpResponse('123')

def image(request):
    return render(request,'photo/image.html',locals())