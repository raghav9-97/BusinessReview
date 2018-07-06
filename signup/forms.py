from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()
class SignUpModel(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100,required=False)
    email = forms.EmailField(max_length=250)

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1')

    def save(self,req):
        inst = super(SignUpModel,self).save(commit=False)
        if req.user.is_authenticated:
            inst.user_type = 1
            inst.admin_id = req.user.id
        else:
            inst.user_type = 0
        inst.save()