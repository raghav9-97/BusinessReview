from django.shortcuts import render,redirect
from .forms import BusiModelForm
import datetime
from .models import BusiModel,ScrapedData
from .updatescript import UpdateReviews
from signup.models import UserDefined
from django.views import View
# Create your views here.


def busimodel(request):
    business = BusiModel.objects.filter(User_id=request.user.id)
    form_class = BusiModelForm
    if request.method == 'POST':
        form = form_class(request.POST,request=request)
        if form.is_valid():
            form.save(request.user.id)
            return redirect('/userpage')
    else:
        form = BusiModelForm(request=request)
    return render(request, 'collectdata/addbusiness.html',{'form':form,'business':business})

def reviews(request,user_id):
    today = datetime.date.today()
    newrevs = ScrapedData.objects.filter(TimeStamp=today)
    userview = ScrapedData.objects.filter(Bus_id=user_id)
    business = BusiModel.objects.filter(User_id=request.user.id)
    busname = BusiModel.objects.get(id=user_id)

    return render(request, 'collectdata/reviewstable.html',{'business':business,'busname':busname,'userview':userview,'newrevs':newrevs})

def deladmin(request):
    user = UserDefined.objects.get(id=request.user.id)
    user.delete()
    return redirect('/login')

def management(request):
    form = BusiModelForm(request.POST,request=request)
    business = BusiModel.objects.filter(User_id=request.user.id)
    managers = UserDefined.objects.filter(admin=request.user.id)
    return render(request,'collectdata/management.html',{'form':form,'business':business,'managers':managers})

def delmag(request,mag_id):
    manager = UserDefined.objects.filter(id=mag_id)
    manager.delete()
    return redirect('/management')

def delbus(request,busin_id):
    business = BusiModel.objects.filter(id=busin_id)
    business.delete()
    return redirect('/management')

def updatemag(request,bus_id):
    business = BusiModel.objects.get(id=bus_id)
    if request.POST:
        new_mag = request.POST.get('Manager')
        business.Manager_id = new_mag
        business.save()
    return redirect('/management')