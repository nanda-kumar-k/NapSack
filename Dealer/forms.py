from django import forms
from .models import DealerUsers


class DLogin(forms.ModelForm):
    class Meta:
        model = DealerUsers
        fields = ('username', 'password')


class DRegistration(forms.ModelForm):
    class Meta:
        model = DealerUsers
        exclude = ['created_on','dealer_user_id']

    def __init__(self, *args, **kwargs):
        super(DRegistration, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs \
            .update({
            'placeholder': 'Full Name',
            'class': 'login__input'
        })
        self.fields['username'].widget.attrs \
            .update({
            'placeholder': 'Username',
            'class': 'login__input'
        })
        self.fields['email'].widget.attrs \
            .update({
            'placeholder': 'EMail',
            'class': 'login__input'
        })
        self.fields['password'].widget.attrs \
            .update({
            'placeholder': 'Password',
            'class': 'login__input'
        })
        self.fields['phone_number'].widget.attrs \
            .update({
            'placeholder': 'Phone Number',
            'class': 'login__input'
        })


