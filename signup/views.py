from django.shortcuts import render,redirect
import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpModel
from collectdata.models import BusiModel,UserDefined,ScrapedData

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpModel(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect("/login")
    else:
        form = SignUpModel()
    return render(request,'signup/register.html',{'form':form})

def loginuser(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/userpage')
        else:
            messages.error(request,"Username or password not correct")
            return redirect('/login')
    return render(request,'signup/login.html')


def userpage(request):
    mappings = {}
    newrevs = ScrapedData.objects.filter(TimeStamp=datetime.date.today())
    mags = UserDefined.objects.filter(admin_id=request.user.id)
    if request.user.is_authenticated:
        if request.user.user_type == 0:
          business = BusiModel.objects.filter(User_id=request.user.id)
        elif request.user.user_type == 1:
            business = BusiModel.objects.filter(Manager_id=request.user.id)
        for i in business:
            buss = i.Business + i.Address.split(",")[0] + ',' + i.Address.split(",")[1] + ',' + i.Address.split(",")[3]
            if i.Manager_id:
                mag_name = UserDefined.objects.get(id=i.Manager_id).first_name + ' ' + UserDefined.objects.get(id=i.Manager_id).last_name
            else:
                mag_name = 'Admin'
            review = len(ScrapedData.objects.filter(Bus_id=i.id))
            mappings[buss] = [mag_name,review]
        return render(request,'signup/index.html',{'business':business,'mapping':mappings,'newrevs':newrevs,'mags':mags})
    else:
        return redirect('/login')

def createmag(request):
    business = BusiModel.objects.filter(User_id=request.user.id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpModel(request.POST)
            if form.is_valid():
                form.save(request)
                return redirect('/userpage')
        else:
            form = SignUpModel()
        return render(request, 'signup/createmag.html', {'form': form,'business':business})
    else:
        return redirect('/login')



