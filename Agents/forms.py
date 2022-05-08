from django import forms
from .models import AgentsUsers


class ALogin(forms.ModelForm):
    class Meta:
        model = AgentsUsers
        exclude = ['created_on', 'agent_shop_id', 'location','agen_user_id']
        # fields = ['first_name']
        # labels = {
        #     'first_name': ('Writer'),
        # }
        # exclude = ('updated', 'created')

    def __init__(self, *args, **kwargs):
        super(ALogin, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs \
            .update({
            'placeholder': 'First Name',
            # 'class': 'input-calss_name'
        })
        self.fields['last_name'].widget.attrs \
            .update({
            'placeholder': 'Last Name',
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
            'placeholder': '+91 Phone Number',
        })
        self.fields['agent_shop_name'].widget.attrs \
            .update({
            'placeholder': 'Shop Name',
        })




