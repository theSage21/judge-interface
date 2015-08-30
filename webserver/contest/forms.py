from django.forms import Form, CharField, PasswordInput
from django.contrib.auth.models import User


class RegistrationForm(Form):
    username = CharField(label='Username: ', max_length=50)
    password = CharField(widget=PasswordInput)
    def is_valid(self):
        valid = super (Form, self).is_valid()
        if not valid:
            return valid
        uname = self.cleaned_data['username']
        users = User.objects.filter(username=uname).count()
        if users > 0:
            self._errors['Validation_Error'] = 'The username is taken. Pick a new one'
            return False
        else:
            return True
