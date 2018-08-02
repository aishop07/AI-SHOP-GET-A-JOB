from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
import numpy as np
import cv2
import paramiko
from time import sleep
import os
import json
with open('photo/config.json' , 'r') as reader:
    config = json.loads(reader.read())

account = config['account']
password = config['password']
ip = config['ip']

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
        if cv2.waitKey(20) & 0xFF == ord(' '):
            cv2.imwrite("./photo/static/images/test.jpg", frame)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    #將檔案上傳至Linux
    t = paramiko.Transport((ip,22))
    t.connect(username = account, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/' + account + '/test/test.jpg'
    localpath='./photo/static/images/test.jpg'


    sftp.put(localpath,remotepath) #上传文件
    sftp.close()
    t.close()

    #執行臉部偵測(fdetect2.py))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22, account, password)
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 fdetect2.py")
    print(stdout.readlines())
    ssh.close()

    # return render(request,'home/index.html',locals())
    return HttpResponse('123')

    
def getphoto(request):
    t = paramiko.Transport((ip,22))
    t.connect(username = account, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/' + config['account'] + '/test/test_result.jpg'
    localpath='./photo/static/images/test_result.jpg'

    sftp.get(remotepath,localpath) #上传文件
    sftp.close()
    t.close()
    return HttpResponse('123')

def takephotos(request):
    # get cookies 抓取登入者姓名
    name = request.COOKIES.get('name1')
    # 將名字寫進labels.txt
    f = open('./photo/labels.txt','w')
    f.write(name)
    f.close()
    
    # 開啟web cam拍照
    camera = cv2.VideoCapture(0)

    while(True):
        ret, frame = camera.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord(' '):
            for i in range(1,13):
                while(True):
                    ret, frame = camera.read()
                    cv2.imshow('frame',frame)
                    cv2.imwrite("./photo/static/images/s1/" + str(i) + ".jpg", frame)
                    break
            break
        
    camera.release()
    cv2.destroyAllWindows()

    t = paramiko.Transport((ip,22))
    t.connect(username = account, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)

    local_images = os.listdir('./photo/static/images/s1/')
    for image in local_images:
        remotepath='/home/' + account + '/test/training-data/s1/'+ image
        localpath='./photo/static/images/s1/' + image
        sftp.put(localpath,remotepath) #上传文件

    sftp.put('./photo/labels.txt','/home/' + account + '/test/labels.txt')
    sftp.close()
    t.close()
    
    #訓練Model
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22, account, password)
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 Face-Recognition-Train.py labels.txt")
    getresult = stdout.readlines()
    ssh.close()
    
    getresult = getresult[-1].split(':')[1].split()
    print(getresult)
    img = {}
    if int(getresult[0]) < 5:
        img["img"] = 'error'
        print('Face Error')
    else:
        img["img"] = 'OK'
        print('註冊成功')

    

    return HttpResponse(json.dumps(img))

def login(request):
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        # cv2.imshow('gray',gray)
        if cv2.waitKey(20) & 0xFF == ord(' '):
            cv2.imwrite("./photo/static/images/pred.jpg", frame)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    #將檔案上傳至Linux
    t = paramiko.Transport((ip,22))
    t.connect(username = account, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)

    remotepath='/home/' + account + '/test/test-data/pred.jpg'
    localpath='./photo/static/images/pred.jpg'

    sftp.put(localpath,remotepath) #上传文件
    sftp.close()
    t.close()


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22, account, password)
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 Face-Recognition-Predect.py labels.txt")
    getname = stdout.readlines()
    ssh.close()
    # print(getname)
    getname = getname[-3].split()[0][:-4]
    # print(getname[:-4])
    name = {}
    if getname == 'Predic':
        name["name"] = 'error'
        print('Face Error')
    else:
        name["name"] = getname
        print(getname)
        print('登入成功')
    
    # return HttpResponse('123')
    return HttpResponse(json.dumps(name))
    # return HttpResponse(getname)

def image(request):
    return render(request,'photo/image.html',locals())