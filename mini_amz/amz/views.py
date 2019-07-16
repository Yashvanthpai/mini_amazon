from django.shortcuts import render,redirect
from . import forms
from django.http import Http404
from pymongo import MongoClient
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
connection = MongoClient('mongodb://localhost:27017/')['mimamazon']

def index(request):
    return render(request,'index.html',{'about':'yes','register':'yes','contact':'yes'})

def about(request):
    return render(request,'one.html',{'about':'','register':'yes','contact':'yes'})

def contact(request):
    return render(request,'one.html',{'about':'yes','register':'yes','contact':''})


def registration(request):
    if request.method == 'POST':
        form1  = forms.Userregistrtion(request.POST)
        if form1.is_valid():
            print("in file 1 save")
            form1.save()
            return redirect('login')
        return render(request,'registratin.html',{'form':form1,'about':'yes','register':'','contact':'yes'})
    else:
        formobj = forms.Userregistrtion()
        return render(request,'registratin.html',{'form':formobj,'about':'yes','register':'','contact':'yes'})

@login_required
def logingout(request):
    logout(request)
    return redirect('index')

def dicsort():
    y = connection['Products'].find()
    count=1
    
    li=['Product_name','Product_name','product_man','product_info','product_img','product_price']
    loopval ={}
    for i in y:
        dic={}
        for j in li:
            dic[j]=i[j]
        loopval[count]=dic
        count+=1
    return loopval
    
@login_required
def logedin(request):
    loopval=dicsort()
    p = request.user.get_username()
    print(p)
    x = connection['auth_user_extend'].find_one({'Uname':p})
    if x['status']=='seller':
        if request.method =='POST':
            form1= forms.Product(request.POST,request.FILES)
            if form1.is_valid():
                myfile = request.FILES['product_img']
                fs = FileSystemStorage(location='static/product')
                filename = fs.save(myfile.name, myfile)
                try:
                    form1.save(myfile.name,request.user.get_username())
                    loopval=dicsort()
                    formobj= forms.Product()
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj})

                except Exception as exp:
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1})
            else:
                return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1})

        formobj= forms.Product()
        loopval=dicsort()
        return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj})

    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':x['status'],"loop":loopval,'form':None})

def in_prod(uname):
    y = connection['Products'].find({'product_man':uname})
    count=1
    li=['Product_name','Product_name','product_man','product_info','product_img','product_price']
    loopval ={}
    for i in y:
        dic={}
        for j in li:
            dic[j]=i[j]
        loopval[count]=dic
        count+=1
    return loopval
    


@login_required
def inventory(request):
    loopval = in_prod(request.user.get_username())
    if request.method =='POST':
            form1= forms.Product(request.POST,request.FILES)
            form2= forms.Product_edit(request.POST,request.FILES)
            if form1.is_valid():
                myfile = request.FILES['product_img']
                fs = FileSystemStorage(location='static/product')
                filename = fs.save(myfile.name, myfile)
                try:
                    form1.save(myfile.name,request.user.get_username())
                    loopval = in_prod(request.user.get_username())
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2})
                except Exception as exp:
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2})
            elif form2.is_valid():
                myfile = request.FILES['Eproduct_img']
                fs = FileSystemStorage(location='static/product')
                filename = fs.save(myfile.name, myfile)
                try:
                    form2.save(myfile.name)
                    loopval = in_prod(request.user.get_username())
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2})
                except Exception as exp:
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2})
            else:
                loopval = in_prod(request.user.get_username())
                formobj= forms.Product()
                formobj2= forms.Product_edit()
                return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1,'form1':form2})
    
    if request.method =='GET':
        loopval = in_prod(request.user.get_username())
        formobj= forms.Product()
        formobj2= forms.Product_edit()
        return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2})

