from django.forms import Form, CharField, PasswordInput


class RegistrationForm(Form):
    username = CharField(label='Username: ', max_length=50)
    password = CharField(widget=PasswordInput)
