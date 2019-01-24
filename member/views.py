from django.shortcuts import render,redirect
from .models import Member
from django.http import HttpResponse
from products.models import Orders,Foods,Drinks

# Create your views here.
def index(request):
    if 'name' in request.COOKIES:
        return render(request,'member/memberarea.html',locals())
    else:
        response = HttpResponse("<script>alert('請先登入喔!');location.href='/member/login'</script>")
        return response


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pwd = request.POST['userpassword']
        member = Member.objects.filter(username=username,password=pwd).values('username')
        if member:
            response = HttpResponse("<script>alert('登入成功');location.href='/member/memberarea'</script>")
            if 'rememberme' in request.POST:
                expiresdate = datetime.datetime.now() + datetime.timedelta(days=7)
                response.set_cookie("name",member[0]['username'],expires=expiresdate)
            else:
                response.set_cookie("name",member[0]['username'])
        else:
            response = HttpResponse("<script>alert('密碼錯誤');location.href='/member/login'</script>")
        return response
    title = "會員登入"
    return render(request,'member/login.html',locals())

def logout(request):
   response = HttpResponse("<script>alert('登出成功');location.href='/member/login'</script>")
   response.delete_cookie('name')
   return response

def create(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        useremail = request.POST["useremail"]
        userbirth = request.POST["userbirth"]

        # EMAIL_USE_TLS = True 
        # EMAIL_HOST = "smtp.gmail.com"
        # EMAIL_PORT = 587
        # EMAIL_HOST_USER = "a11118825@gmail.com"
        # EMAIL_HOST_PASSWORD = "a63475566"
        # from_email = EMAIL_HOST_USER
        # to_list = useremail

        # # email_conn即為SMTP物件，建立SMTP連線
        # email_conn=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        # email_conn.ehlo()
        # #TTLS安全認證機制，必須使用TTLS protocol來進行連結傳輸,故叫喚starttls這個函式
        # email_conn.starttls()
        # email_conn.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        # email_conn.sendmail(from_email, to_list, "Hi Welcome, now you are one of us!")
        # email_conn.quit()

        #todo 接收到的會員資料寫進資料庫
        Member.objects.create(username=username,password=password,useremail=useremail,userbirth=userbirth)
        
        #todo 新增完成後轉到http://localhost:8000/member
        return redirect("/member/login")
       
    title = "會員新增" 
    return render(request,'member/create.html',locals())

def forget(request):
    if request.method == 'POST':      
        useremail=request.POST['useremail']
        response = HttpResponse("<script>alert('修改密碼信件已寄出');location.href='/member/index'</script>")
        return response
    
    else:
        return render(request,'member/forget.html',locals())

def update(request,id):
    #     if request.method == 'POST' and request.COOKIES['name']:        
    #         username = request.POST["username"]      
    #         useremail = request.POST["useremail"]
    #         userbirth = request.POST["userbirth"]
    #         password=request.POST["password"]

    #     #todo 修改資料庫中的會員資料
    #         member = Member.objects.get(id)
    #         member.username = username
    #         member.useremail  = useremail
    #         member.userbirth = userbirth
    #         member.password = password
    #         member.save()
        
    #     #todo 修改完成後轉到http://localhost:8000/member
    #         return redirect('/member')

    #         title = "會員修改"

    # #todo 根據會員編號取得會員資料傳給update.html
    #         member = Member.objects.filter(id)
    #         return render(request,'member/update.html',locals())
    #     else:    
    #         return  HttpResponse("<script>alert('請先登入喔!');location.href='/member/login'</script>")

    if request.method == 'POST':        
        username = request.POST["username"]      
        useremail = request.POST["useremail"]
        userbirth = request.POST["userbirth"]
        password=request.POST["password"]

        #todo 修改資料庫中的會員資料
        member = Member.objects.get(id=int(id))
        member.username = username
        member.useremail  = useremail
        member.userbirth = userbirth
        member.password = password
        member.save()
        
        #todo 修改完成後轉到http://localhost:8000/member
        return redirect('/member')

    #todo 根據會員編號取得會員資料傳給update.html
    member = Member.objects.get(id=int(id))
    return render(request,'member/update.html',locals())


def delete(request,id):
    #todo 根據會員編號刪除會員資料
    member = Member.objects.get(id=int(id))
    member.delete()

    #todo 刪除完成後轉到http://localhost:8000/member
    return redirect('/member')

def memberarea(request):
    if 'name' in request.COOKIES:
        name=request.COOKIES['name']
        # print(name)
        member = Member.objects.get(username=name)
        orders = list(Orders.objects.filter(user_name=str(request.COOKIES['name'])).order_by('-datetime').values())
        food = list(Foods.objects.filter(name__contains= 'pringles' ).values())
        drink = list(Drinks.objects.filter(name__contains= 'cafe' ).values())
        Food = list(Foods.objects.all().values())
        Drink = list(Drinks.objects.all().values())
        print(Food, Drink)
        i=0
        result=[]
        while i < len(orders):
            #print(orders[i]['product_name'])
            result.append(orders[i]['product_name'])
            i+=1
        countresult=[result.count('pringles'),result.count('cafe')]

        #result1=[]
        if result.count('pringles')>result.count('cafe'):
            img1=food[0]['image']
            img2=food[1]['image']
            img3=food[2]['image']
            img4=food[3]['image']
            # for i in food:
            #     result1.append(i['image'])          
                
        elif  result.count('pringles')<result.count('cafe'):
            img1=drink[0]['image']
            img2=drink[1]['image']
            img3=drink[2]['image']
            img4=drink[3]['image']
            # for i in drink:
            #     result1.append(i['image'])      
        else:
            img1=Food[6]['image']
            img2=Food[7]['image']
            img3=Drink[6]['image']
            img4=Drink[7]['image']   

       
        return render(request,'member/memberarea.html',locals())

    else:
        response = HttpResponse("<script>alert('請先登入喔!');location.href='/member/login'</script>")
        return response
        # return render(request,'member/memberarea.html',locals())



     