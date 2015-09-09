from django.forms import ModelForm
from smart_access.models import User
class userForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'contact','address', 'roles']
