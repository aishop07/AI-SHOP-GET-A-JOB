from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
import numpy as np
import cv2
import paramiko
from time import sleep
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
    t = paramiko.Transport(('192.168.2.16',22))
    t.connect(username = '你的帳號', password = '你的密碼')
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/arron1294/test/test.jpg'
    localpath='./photo/static/images/test.jpg'


    sftp.put(localpath,remotepath) #上传文件
    sftp.close()
    t.close()

    #執行臉部偵測(fdetect2.py))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.2.16",22,"你的帳號", "你的密碼")
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 fdetect2.py")
    print(stdout.readlines())
    ssh.close()

    # return render(request,'home/index.html',locals())
    return HttpResponse('123')

    
def getphoto(request):
    t = paramiko.Transport(('192.168.2.16',22))
    t.connect(username = '你的帳號', password = '你的密碼')
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/你的帳號/test/test_result.jpg'
    localpath='./photo/static/images/test_result.jpg'

    sftp.get(remotepath,localpath) #上传文件
    sftp.close()
    t.close()
    return HttpResponse('123')

def takephotos(request):
    
    camera = cv2.VideoCapture(0)
    while(True):
        ret, frame = camera.read()
        
        # Camera warm-up time
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('\r'):
            for i in range(1,13):
                while(True):
                    ret, frame = camera.read()
                    cv2.imshow('frame',frame)
                    cv2.imwrite("./photo/static/images/" + str(i) + ".jpg", frame)
                    break
            break
        

    camera.release()
    cv2.destroyAllWindows()

    t = paramiko.Transport(('192.168.2.16',22))
    t.connect(username = '你的帳號', password = '你的密碼')
    sftp = paramiko.SFTPClient.from_transport(t)

    for i in range(1,13):

        remotepath='/home/你的帳號/test/training-data/s3/' + str(i) + '.jpg'
        localpath='./photo/static/images/' + str(i) + '.jpg'

        sftp.put(localpath,remotepath) #上传文件

    sftp.close()
    t.close()
    return render(request,'photo/image.html',locals())

def image(request):
    return render(request,'photo/image.html',locals())