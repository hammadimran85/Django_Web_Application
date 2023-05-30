from django.shortcuts import render, HttpResponse , redirect
from .models import customer
from .models import extended
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import jwt
from .forms import bookform
from . models import book
from .serializers import bookserializers
from django.http import JsonResponse, HttpResponse
# Create your views here.

def index(request):
     d = {'mydic':['Hammad','Imran','ALi','Ahsan','Asad'],'Age':20}
     return render(request,'myhome.html',d)

def myfunc(request):
    obj = customer.objects.all()
    #obj = customer.objects.filter(Email="maddyexx85@gmail.com")
    #obj = customer.objects.get(Email="hammadimran85@gmail.com")
    d={'obj':obj}
    return render(request,"data.html",d)

def data(request):
    if request.method == 'GET':
        return HttpResponse("You are here with Get method " + str(request.GET['fname']))
    else:
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        p = request.POST['password']
        #d = {'Fname':f,'Lname':l,'Email':e,'Password':p}
        obj = customer()
        obj.Fname=f
        obj.Lname=l
        obj.Email=e
        try:
            obj.save()
            return HttpResponse("Success")
        except:
            return HttpResponse("Fail")


def delete(request,id):
    obj=customer.objects.get(pk=id)
    obj.delete()
    return redirect("/")
def update(request,id):
    if request.method == 'POST':
        myid = request.POST['id']
        obj = customer.objects.get(pk=myid)
        obj.Fname = request.POST['fname']
        obj.Lname = request.POST['lname']
        obj.Email = request.POST['email']
        obj.save()
        return redirect('/')
    obj = customer.objects.get(pk=id)
    d = {'obj':obj,'id':id}
    return render(request,'updated.html',d)

def mylogin(request):
    if request.method == 'POST':
        usern = request.POST['username']
        passw = request.POST['password']
        user = authenticate(request,username=usern,password=passw)
        if user is not None:
            login(request,user)
            return redirect('/main/')
        else:
            return render(request,'mylogin.html',{'mes':'Wrong Credentials'})
    if request.user.is_authenticated:
        return render(request,'main.html')
    else:
        return render(request,'mylogin.html')

@login_required(login_url='/main/')

def mainpage(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        em = request.POST['email']
        p = request.POST['password']
        f = request.FILES['file']
        cx = customer.objects.create(Fname=fname, Lname=lname, Email=em, Password=p)
        try:
            cx.save()
            ex = extended()
            ex.id = cx
            ex.img = f
            ex.save()
            return render(request, 'main.html', {'msg': 'Data submit successfully'})
        except:
            return render(request, 'main.html', {'msg': 'Failed to submit :('})
    if request.user.is_authenticated:
        ob = customer.objects.all()
        d = {"obj": ob}
        return render(request, "main.html", d)
    return render(request, 'main.html')

def mysignup(request):
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        u = request.POST['username']
        p = request.POST['password']
        i = request.FILES['file']
        us = User.objects.create_user(
        email = e,
        username = u,
        password = p,
        is_active = False)
        us.first_name=f
        us.last_name=l
        mes1={'mes1':'Error Occured!... Please try again'}
        try:
            us.save()
            # ex = extended.objects.all.exclude(pk=id)
            encode = jwt.encode(payload={'id': str(us.pk)}, key="secret", algorithm="HS256")
            link = request.scheme+"://"+request.META['HTTP_HOST']+"/activate/"+str(encode)+"/"
            em = EmailMessage('info', 'Thank you for Sign Up '+link,'hammadimran85@gmail.com',[e])
            em.send()
            return render(request, 'mysignup.html', {'mes': 'Check your mail to Activate Account!'})
        except:
            return render(request, 'mysignup.html', mes1)
    return render(request, 'mysignup.html')
def mylogout(request):
    logout(request)
    return redirect('/')

def activate(request,id):
    decode = jwt.decode(id, key="secret", algorithms=["HS256"])
    act = User.objects.get(pk=int(decode['id']))
    act.is_active = True
    act.save()
    return redirect('/')
def formview(request):
    if request.method=='POST':
        data=bookform(request.POST)
        if data.is_valid():
            data.save()
            return HttpResponse("Data Saved!")
    f=bookform()
    return render(request,'myform.html',{'myform':f})
def mysection(request):
    return render(request,"sections.html")
def about(request):
    return render(request,"about.html")

def bookserializer(request):
    if request.method=='GET':
        alldata=book.objects.all()
        data=bookserializers(alldata, many=True)
        return JsonResponse(data.data, safe=False)
