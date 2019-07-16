from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from pymongo import MongoClient
from django.core import validators

connection = MongoClient('mongodb://localhost:27017/')['mimamazon']


class Userregistrtion(UserCreationForm):
    email = forms.EmailField(required=True)
    status = forms.ChoiceField(choices=[("seller",'SELLER'),('buyer','BUYER')], required=True,widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    
    def save(self,commit=True):
        user = super(Userregistrtion,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        print(self.cleaned_data['status'])
        print("In Save data user")
        
        if commit:
            user.save()
            mydict = { "Uname":self.cleaned_data['username'] , "status": self.cleaned_data['status']}
            connection['auth_user_extend'].insert_one(mydict)
        
        return user

class Product(forms.Form):
    product_name = forms.CharField(max_length=25,label='Product',required=True,widget=forms.TextInput(attrs={'placeholder':'Enter product Name'}))
    product_price= forms.IntegerField(label='Price',required=True,widget=forms.NumberInput(attrs={'placeholder':'Enter product Price'}))
    #product_man = forms.CharField(max_length=25,label='Manufacturer',required=True,widget=forms.TextInput(attrs={'placeholder':'Enter product Manufacturer Name'}))
    product_info = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),label='Discription',required=True)
    product_img = forms.FileField(label="Choose product pic",required=False)

    def save(self,arg1,arg2):
        x  = connection['Products'].find({"Product_name":self.cleaned_data['product_name'] ,"product_man": str(arg2)}).count() 
        if x <= 0:
            mydict = { "Product_name":self.cleaned_data['product_name'] , "product_price": self.cleaned_data['product_price'],"product_man": str(arg2),"product_info": self.cleaned_data['product_info'],"product_img": arg1}
            connection['Products'].insert_one(mydict)

        else:
            raise forms.ValidationError("Produc Already Exist")

class Product_edit(forms.Form):
    Eproduct_name = forms.CharField(max_length=25,label='Product',required=True,widget=forms.TextInput(attrs={'placeholder':'Enter product Name'}))
    Eproduct_price= forms.IntegerField(label='Price',required=True,widget=forms.NumberInput(attrs={'placeholder':'Enter product Price'}))
    Eproduct_man = forms.CharField(max_length=25,label='Manufacturer',required=True,widget=forms.TextInput(attrs={'placeholder':'Enter product Manufacturer Name'}))
    Eproduct_info = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),label='Discription',required=True)
    Eproduct_img = forms.FileField(label="Choose product pic",required=False)

    def save(self,arg1):
        try:
            myq={"Product_name":str(self.cleaned_data['Eproduct_name']),"product_man": str(self.cleaned_data['Eproduct_man'])}
            y = connection['Products'].find(myq).count()
            if y >0:
                q ={ "product_price": int(self.cleaned_data['Eproduct_price']),"product_info": str(self.cleaned_data['Eproduct_info']),"product_img": str(arg1) }
                newval={"$set": q}
                a =connection['Products'].update_many(myq,newval)
                print(a.modified_count)
        except: 
            raise forms.ValidationError("Eoror")
