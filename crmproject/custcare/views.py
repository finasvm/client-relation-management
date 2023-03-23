from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View,CreateView,FormView,TemplateView,DeleteView
from .forms import SignupForm
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from custcare.models import CustomerDatas,Note as Notes
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import date
# Create your views here.

# def SignInRequired(func):
#     def wrapper(request,*args,**kwargs):
#         if request.user.is_authenticated:
#             return func(request,*args,**kwargs)
#         else:
#             return redirect('login')
#     return wrapper


class SignUp(CreateView):
    model=User
    form_class=SignupForm
    template_name='signup.html'
    success_url=reverse_lazy('login')

# @method_decorator(SignInRequired,name='dispatch')
class Home(View):
    def get(self,request):
        user1=request.user
        selected_customer=CustomerDatas.objects.filter(user=user1)
        print(selected_customer)
        no_of_customers=selected_customer.count()
        if selected_customer.filter(status='cool').exists():
            cust_cool=CustomerDatas.objects.filter(status='cool').count()
            print(cust_cool)
        else:    
                cust_cool=0
            
        if selected_customer.filter(status='Strong').exists():
            cust_strong=CustomerDatas.objects.filter(status='Strong').count()
        else:
            cust_strong=0

        if selected_customer.filter(status='intermdeiate').exists():
            cust_intermediate=CustomerDatas.objects.filter(status='intermdeiate').count()
        else:
            cust_intermediate=0

        today = date.today()
        if selected_customer.filter(nextcall=today).exists():
            cust_details_date=selected_customer.filter(nextcall=today)
            # return HttpResponse({'cust_details':cust_details_date})
            context={'customer':selected_customer,'count_customer':no_of_customers,'cust_cool':cust_cool,'cust_intermediate':cust_intermediate,
                 'cust_strong':cust_strong,'cust_details':cust_details_date}
            return render(request,'home.html',context)

        context={'customer':selected_customer,'count_customer':no_of_customers,'cust_cool':cust_cool,'cust_intermediate':cust_intermediate,
                 'cust_strong':cust_strong}
        return render(request,'home.html',context)
    


class SignIn(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user:            
                login(request,user)
                print(user.username)
                return redirect('home')
            else:
                return redirect('login')
            

# @method_decorator(SignInRequired,name='dispatch')
class AddCustomer(View):
    def get(self,request):
        user1=request.user
        selected_customer=CustomerDatas.objects.filter(user=user1)
        today = date.today()
        if selected_customer.filter(nextcall=today).exists():
            cust_details_date=selected_customer.filter(nextcall=today)
            context={'cust_details':cust_details_date}
            return render(request,'addcustomer.html',context)
        return render(request,'addcustomer.html')
    def post(self,request):
        name=request.POST['name1']
        title=request.POST['title1']
        number=request.POST['number1']
        address=request.POST['address1']
        calldate=request.POST['date1']
        nextcall=request.POST['date2']
        status=request.POST['status1']
        user1=request.user
        CustomerDatas.objects.create(name=name,title=title,phnumber=number,address=address,
                                    lastcall=calldate,nextcall=nextcall,status=status,user=user1)
        return redirect('showcustomer')
        
# @method_decorator(SignInRequired,name='dispatch')
class ShowCustomers(View):
    def get(self,request):
        user1=request.user
        selected_customer=CustomerDatas.objects.filter(user=user1)
        today = date.today()
        if selected_customer.filter(nextcall=today).exists():
            cust_details_date=selected_customer.filter(nextcall=today)
            context={'customer':selected_customer,'cust_details':cust_details_date}
            return render(request,'showcustomers.html',context)
        return render(request,'showcustomers.html', {'customer':selected_customer})

        

# @method_decorator(SignInRequired,name='dispatch')  
class EditCustomer(View):
    def get(self,request):
        custid=request.GET['pk']
        cust_details=CustomerDatas.objects.get(id=custid)
        user1=request.user
        selected_customer=CustomerDatas.objects.filter(user=user1)
        today = date.today()
        if selected_customer.filter(nextcall=today).exists():
            cust_details_date=selected_customer.filter(nextcall=today)
            context={'customer':cust_details,'cust_details':cust_details_date}
            return render(request,'editcustomers.html',context)
        return render(request,'editcustomers.html',{'customer':cust_details})
    def post(self,request):
        custid=request.GET['pk']
        name=request.POST['name1']
        title=request.POST['title1']
        number=request.POST['number1']
        address=request.POST['address1']    
        calldate=request.POST['date1']
        nextcall1=request.POST.get('date2')
        status=request.POST['status1']
        CustomerDatas.objects.filter(id=custid).update(name=name,title=title,phnumber=number
                                        ,address=address,lastcall=calldate,nextcall=nextcall1,status=status)
        return redirect('showcustomer')

# @method_decorator(SignInRequired,name='dispatch')   
class DeleteCustomer(View):
    def get(self,request):
        custid=request.GET['pk']
        print(custid)
        CustomerDatas.objects.filter(id=custid).delete()
        return redirect('showcustomer')

# @method_decorator(SignInRequired,name='dispatch')
class Note(View): 
    def get(self,request):
        custid=request.GET['pk']
        cust_details=CustomerDatas.objects.get(id=custid)
        user1=request.user
        selected_customer=CustomerDatas.objects.filter(user=user1)
        today = date.today()
        if Notes.objects.filter(user=cust_details).exists(): 
            note_details=Notes.objects.get(user=cust_details) 
            if selected_customer.filter(nextcall=today).exists():
                cust_details_date=selected_customer.filter(nextcall=today) 
                context=  {'customer':note_details,'cust_details':cust_details_date}
                return render(request,'viewnote.html',context)  
            return render(request,'viewnote.html',{'customer':note_details})  
        else:
            if selected_customer.filter(nextcall=today).exists():
                cust_details_date=selected_customer.filter(nextcall=today) 
                context= {'cust_details':cust_details_date}
                return render(request,'viewnote.html',context)  
            return render(request,'viewnote.html')  
        
       
    def post(self,request):
        custid=request.GET['pk']
        note=request.POST['note1']
        cust_details=CustomerDatas.objects.get(id=custid)
        if Notes.objects.filter(user=cust_details).exists(): 
            Notes.objects.filter(user=cust_details).update(note=note)
            note_details=Notes.objects.get(user=cust_details)    
            return redirect('showcustomer')
        else:
            Notes.objects.create(note=note,user=cust_details)
            return redirect('showcustomer')

# @method_decorator(SignInRequired,name='dispatch')
class CustomerReport(View):
    def get(self,request):
        user1=request.user
        selected_customer=CustomerDatas.objects.filter(user=user1)
        today = date.today()
        if selected_customer.filter(nextcall=today).exists():
            cust_details_date=selected_customer.filter(nextcall=today)
            context={'customer':selected_customer,'cust_details':cust_details_date}
            return render(request,'customereport.html',context)
        return render(request,'customereport.html',{'customer':selected_customer})


class LogOut(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('login')
            

    



