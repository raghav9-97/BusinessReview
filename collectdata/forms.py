from django.forms import ModelForm
from .models import BusiModel
from signup.models import UserDefined
from .tasks import scrapegoogle,scrapezomato


class BusiModelForm(ModelForm):
    class Meta:
        model = BusiModel
        fields = ['Business','Manager','Zomato_URL','Google_URL']

    def save(self,user):
        inst = super(BusiModelForm,self).save(commit=False)
        inst.User = UserDefined.objects.get(id=user)
        inst.Address = self.request.POST.get('address')
        inst.save()
        scrapegoogle.delay(inst.Google_URL,inst.User_id,inst.id)
        scrapezomato.delay(inst.Zomato_URL,inst.User_id,inst.id)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BusiModelForm, self).__init__(*args, **kwargs)
        choice = (( None , 'None'),)
        for i in UserDefined.objects.filter(admin=self.request.user.id):
            choice = choice + ((i.id, i.first_name + " " + i.last_name),)
        self.fields['Manager'].choices = choice