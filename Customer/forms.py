from django import forms
from .models import CustomerUsers

class CLogin(forms.ModelForm):
    class Meta:
        model = CustomerUsers
        fields = ('username', 'password')


class CRegistration(forms.ModelForm):
    class Meta:
        model = CustomerUsers
        exclude = ['created_on']

    def __init__(self, *args, **kwargs):
        super(CRegistration, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs \
            .update({
            'placeholder': 'Full Name',
            # 'class': 'input-calss_name'
        })
        self.fields['username'].widget.attrs \
            .update({
            'placeholder': 'Username',
        })
        self.fields['email'].widget.attrs \
            .update({
            'placeholder': 'EMail',
        })
        self.fields['password'].widget.attrs \
            .update({
            'placeholder': 'Password',
        })
        self.fields['phone_number'].widget.attrs \
            .update({
            'placeholder': 'Phone Number',
        })


