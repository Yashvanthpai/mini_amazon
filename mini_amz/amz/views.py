from django.shortcuts import render,redirect,HttpResponse,render_to_response
from . import forms
from django.http import Http404
from pymongo import MongoClient
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import json
import time
import re

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

def dicsort(name):
    li=[]
    z = connection['Products'].find({'product_man':name})
    for i in z:
       if connection['cart'].find_one({'Product_name':i['Product_name'],'product_man':i['product_man']}):
           i['cart']='yes'
       else:
            i['cart']=''
       li.append(i)
    count=1
    l=['Product_name','product_man','product_info','product_img','product_price','cart']
    loopval ={}
    for i in li:
        dic={}
        for j in l:
            dic[j]=i[j]
        loopval[count]=dic
        count+=1
    
    return loopval
    
@login_required
def logedin(request):
    loopval=dicsort(request.user.get_username())
    x = connection['auth_user_extend'].find_one({'Uname':request.user.get_username()})
    if x['status']=='seller':
        if request.method =='POST':
            form1= forms.Product(request.POST,request.FILES)
            formcart = forms.cart_data(request.POST)
            if form1.is_valid():
                myfile = request.FILES['product_img']
                fs = FileSystemStorage(location='static/product')
                filename = fs.save(myfile.name, myfile)
                try:
                    form1.save(myfile.name,request.user.get_username())
                    loopval=dicsort(request.user.get_username())
                    formobj= forms.Product()
                    formcart = forms.cart_data()
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'formcart':formcart})

                except Exception as exp:
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1,'formcart':formcart})
            
            elif formcart.is_valid():
                 try:
                    formcart.save()
                    loopval=dicsort(request.user.get_username())
                    formobj= forms.Product()
                    formscart= forms.cart_data()
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj})
                 except Exception as exp:
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1})
            else:
                return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1,'formcart':formcart})
        
        if request.method =='GET':
            formobj= forms.Product()
            formcart = forms.cart_data()
            return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'formcart':formcart})
    
    if x['status']!='seller':
        if request.method =='POST':
            formcart = forms.cart_data(request.POST)
            if formcart.is_valid():
                 try:
                    formcart.save()
                    loopval=dicsort(request.user.get_username())
                    formscart= forms.cart_data()
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':None,'formcart':formcart})
                 except Exception as exp:
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':None,'formcart':formcart})
            else:
                  return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':None,'formcart':formcart})
        if request.method =='GET':
            formcart = forms.cart_data()
            return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':None,'formcart':formcart})


def in_prod(uname):
    y = connection['Products'].find({'product_man':uname})
    count=1
    li=['Product_name','product_man','product_info','product_img','product_price']
    loopval ={}
    for i in y:
        dic={}
        for j in li:
            dic[j]=i[j]
        loopval[count]=dic
        count+=1
    if len(loopval)==0:
        loopval[1]={'emptyimage':'emptycart.png'}
    return loopval
    


@login_required
def inventory(request):
    loopval = in_prod(request.user.get_username())
    if request.method =='POST':
            form1= forms.Product(request.POST,request.FILES)
            form2= forms.Product_edit(request.POST,request.FILES)
            formcart = forms.cart_data(request.POST)
            if form1.is_valid():
                myfile = request.FILES['product_img']
                fs = FileSystemStorage(location='static/product')
                filename = fs.save(myfile.name, myfile)
                try:
                    form1.save(myfile.name,request.user.get_username())
                    loopval = in_prod(request.user.get_username())
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    formcart = forms.cart_data()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2,'formcart':formcart})
                except Exception as exp:
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2,'formcart':formcart})
            elif form2.is_valid():
                myfile = request.FILES['Eproduct_img']
                fs = FileSystemStorage(location='static/product')
                filename = fs.save(myfile.name, myfile)
                try:
                    form2.save(myfile.name)
                    loopval = in_prod(request.user.get_username())
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    formcart= forms.cart_data()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2,'formcart':formcart})
                except Exception as exp:
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2})
            
            elif formcart.is_valid():
                 try:
                    formcart.idelete()
                    loopval = in_prod(request.user.get_username())
                    formobj= forms.Product()
                    formobj2= forms.Product_edit()
                    formcart= forms.cart_data()
                    return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'formcart':formcart})
                 except Exception as exp:
                    return render(request,'logedin.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1,'formcart':formcart})

            else:
                return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':form1,'form1':form2,'formcart':formcart})
    
    if request.method =='GET':
        loopval = in_prod(request.user.get_username())
        formobj= forms.Product()
        formobj2= forms.Product_edit()
        formcart= forms.cart_data()
        return render(request,'inventory.html',{'about':'','register':'','contact':'','c_type':'seller',"loop":loopval,'form':formobj,'form1':formobj2,'formcart':formcart})

def cart_info(uname):
    y = connection['cart'].find({'product_man':uname})
    count=1
    li=['Product_name','product_man','product_info','product_img','product_price']
    loopval ={}
    for i in y:
        dic={}
        for j in li:
            dic[j]=i[j]
        loopval[count]=dic
        count+=1
    if len(loopval)==0:
        loopval[1]={'emptyimage':'emptycart.png'}

    return loopval

@login_required    
def cart(request):
    loopval = cart_info(request.user.get_username())
    if request.method=='POST':
        form = forms.cart_data(request.POST)
        if form.is_valid():
            try:
                form.cdelete()
                loopval = cart_info(request.user.get_username())
                form= forms.cart_data()
                return render(request,'cart.html',{'about':'','register':'','contact':'',"loop":loopval,'form':form})
            except:
                return render(request,'cart.html',{'about':'','register':'','contact':'',"loop":loopval,'form':form})
        else:
            return render(request,'cart.html',{'about':'','register':'','contact':'',"loop":loopval,'form':form})
    
    form = forms.cart_data()
    return render(request,'cart.html',{'about':'','register':'','contact':'',"loop":loopval,'form':form})