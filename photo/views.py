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
        if cv2.waitKey(20) & 0xFF == ord('q'):
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
    name = request.COOKIES.get('name')
    # 將名字寫進labels.txt
    f = open('./photo/labels.txt','a')
    f.write('\n' + name)
    f.close()
    # 新增照片資料夾 ex:s1,s2...
    dirs = os.listdir('./photo/static/images')
    s_dirs = []
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue
        s_name = int(dir_name.replace("s", ""))
        s_dirs.append(s_name)
    new_folder = 's'+ str(s_dirs[-1] + 1)
    os.mkdir('./photo/static/images/' + new_folder + '/')
    # 開啟web cam拍照
    camera = cv2.VideoCapture(0)
    while(True):
        ret, frame = camera.read()
        
        # Camera warm-up time
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord(' '):
            for i in range(1,13):
                while(True):
                    ret, frame = camera.read()
                    cv2.imshow('frame',frame)
                    cv2.imwrite("./photo/static/images/" + new_folder + "/" + str(i) + ".jpg", frame)
                    break
            break
        

    camera.release()
    cv2.destroyAllWindows()

    t = paramiko.Transport((ip,22))
    t.connect(username = account, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.mkdir('/home/' + account + '/test/training-data/' + new_folder + '/')
    local_images = os.listdir('./photo/static/images/' + new_folder + '/')
    for image in local_images:
        
        remotepath='/home/' + account + '/test/training-data/' + new_folder + '/' + image
        localpath='./photo/static/images/' + new_folder + '/' + image
        sftp.put(localpath,remotepath) #上传文件

    sftp.put('./photo/labels.txt','/home/' + account + '/test/labels.txt')
    sftp.close()
    t.close()
    
    #訓練Model
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22, account, password)
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 Face-Recognition-Train.py labels.txt")
    print(stdout.readlines())
    ssh.close()

    return HttpResponse('123')

def login(request):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22, account, password)
    stdin, stdout, stderr = ssh.exec_command("cd test/; python3 Face-Recognition-Predect.py labels.txt")
    getname = stdout.readlines()
    ssh.close()
    print(getname)
    getname = getname[2].split(':')[1].split()[0]
    print(getname)
    return HttpResponse('123')

def image(request):
    return render(request,'photo/image.html',locals())