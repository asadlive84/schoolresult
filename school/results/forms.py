from django import forms



class ProfileSearchForm(forms.Form):
    std_class = forms.CharField(required=False)
